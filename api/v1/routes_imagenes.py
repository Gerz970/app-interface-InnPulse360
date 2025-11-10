"""
Rutas API para gestión de imágenes
Incluye endpoints para subir imágenes, especialmente foto de perfil
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from typing import Optional
import os

from services.storage import SupabaseImageStorageService
from schemas.storage import ImageUploadResponse
from api.v1.routes_usuario import get_current_user
from schemas.seguridad.usuario_response import UsuarioResponse
from utils.rutas_imagenes import RutasImagenes
from sqlalchemy.orm import Session
from core.database_connection import get_database_session
from services.seguridad.usuario_service import UsuarioService

# Configurar router
router = APIRouter(
    prefix="/imagenes",
    tags=["imagenes"],
    responses={404: {"description": "Not found"}},
)

# Configurar seguridad
security = HTTPBearer()


def get_image_storage_service() -> SupabaseImageStorageService:
    """
    Dependency para obtener el servicio de almacenamiento de imágenes
    
    Returns:
        SupabaseImageStorageService: Instancia del servicio
    """
    return SupabaseImageStorageService()


def get_usuario_service(db: Session = Depends(get_database_session)) -> UsuarioService:
    """
    Dependency para obtener el servicio de usuario
    
    Args:
        db (Session): Sesión de base de datos
        
    Returns:
        UsuarioService: Instancia del servicio
    """
    return UsuarioService(db)


# Instancia de RutasImagenes para construir rutas consistentes
rutas_imagenes = RutasImagenes()


@router.put(
    "/foto/perfil/{id_usuario}",
    response_model=ImageUploadResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar foto de perfil de usuario"
)
async def update_foto_perfil(
    id_usuario: int,
    file: UploadFile = File(..., description="Archivo de imagen (JPG, PNG, GIF)"),
    current_user: UsuarioResponse = Depends(get_current_user),
    image_service: SupabaseImageStorageService = Depends(get_image_storage_service),
    usuario_service: UsuarioService = Depends(get_usuario_service)
):
    """
    Actualiza o sube la foto de perfil de un usuario
    
    - **id_usuario**: ID del usuario al que se le asignará la foto de perfil
    - **file**: Archivo de imagen (debe ser JPG, PNG o GIF)
    
    La imagen se guardará en la ruta: `usuarios/perfil/{id_usuario}.{extension}`
    Si ya existe una foto de perfil, será reemplazada automáticamente.
    Si no existe, se subirá la nueva imagen y se registrará en la base de datos.
    
    Requiere autenticación. Solo el usuario puede actualizar su propia foto de perfil.
    """
    # Validar que el usuario tenga permisos
    if current_user.id_usuario != id_usuario:
        # Aquí podrías agregar validación de roles si es necesario
        # Por ahora, solo permitimos que el usuario suba su propia foto
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para subir la foto de perfil de otro usuario"
        )
    
    # Obtener la extensión del archivo
    file_extension = os.path.splitext(file.filename or "")[1].lower()
    
    # Validar extensión
    allowed_extensions = [".jpg", ".jpeg", ".png", ".gif"]
    if not file_extension or file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Extensión de archivo no permitida. Extensiones permitidas: {', '.join(allowed_extensions)}"
        )
    
    # Construir la ruta del archivo usando RutasImagenes
    ruta_base = rutas_imagenes.get_ruta_imagenes_perfil(id_usuario)
    file_path = f"{ruta_base}{file_extension}"
    
    # Leer el contenido del archivo
    try:
        file_bytes = await file.read()
        
        # Obtener el content type del archivo
        content_type = file.content_type
        
        # Subir la imagen (usar upsert=True para sobrescribir si ya existe)
        result = image_service.upload_image(
            file_path=file_path,
            file_bytes=file_bytes,
            content_type=content_type,
            upsert=True
        )
        
        if not result.get("success"):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get("message", "Error al subir la imagen")
            )
        
        # Actualizar la ruta en la base de datos (solo guardamos la ruta relativa)
        usuario_service.actualizar_url_foto_perfil(
            id_usuario=id_usuario,
            url_publica=None,  # No se usa, solo guardamos la ruta relativa
            ruta_storage=file_path
        )
        
        return ImageUploadResponse(
            success=True,
            path=result["path"],
            bucket=result["bucket"],
            public_url=result.get("public_url"),
            message="Foto de perfil actualizada exitosamente"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar la imagen: {str(e)}"
        )


@router.post(
    "/upload",
    response_model=ImageUploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Subir imagen genérica"
)
async def upload_imagen(
    file: UploadFile = File(..., description="Archivo de imagen (JPG, PNG, GIF)"),
    path: Optional[str] = None,
    current_user: UsuarioResponse = Depends(get_current_user),
    image_service: SupabaseImageStorageService = Depends(get_image_storage_service)
):
    """
    Sube una imagen genérica a Supabase Storage
    
    - **file**: Archivo de imagen (debe ser JPG, PNG o GIF)
    - **path**: Ruta opcional donde guardar la imagen (si no se proporciona, se usa el nombre del archivo)
    
    Requiere autenticación.
    """
    # Obtener la extensión del archivo
    file_extension = os.path.splitext(file.filename or "")[1].lower()
    
    # Validar extensión
    allowed_extensions = [".jpg", ".jpeg", ".png", ".gif"]
    if not file_extension or file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Extensión de archivo no permitida. Extensiones permitidas: {', '.join(allowed_extensions)}"
        )
    
    # Construir la ruta del archivo
    if path:
        # Si se proporciona path, asegurarse de que tenga la extensión correcta
        if not path.lower().endswith(tuple(allowed_extensions)):
            file_path = f"{path}{file_extension}"
        else:
            file_path = path
    else:
        # Usar el nombre del archivo original
        file_path = file.filename or f"imagen{file_extension}"
    
    # Leer el contenido del archivo
    try:
        file_bytes = await file.read()
        
        # Obtener el content type del archivo
        content_type = file.content_type
        
        # Subir la imagen
        result = image_service.upload_image(
            file_path=file_path,
            file_bytes=file_bytes,
            content_type=content_type,
            upsert=False
        )
        
        if not result.get("success"):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get("message", "Error al subir la imagen")
            )
        
        return ImageUploadResponse(
            success=True,
            path=result["path"],
            bucket=result["bucket"],
            public_url=result.get("public_url"),
            message="Imagen subida exitosamente"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar la imagen: {str(e)}"
        )


@router.delete(
    "/foto/perfil/{id_usuario}",
    status_code=status.HTTP_200_OK,
    summary="Restaurar foto de perfil por defecto"
)
async def delete_foto_perfil(
    id_usuario: int,
    current_user: UsuarioResponse = Depends(get_current_user),
    image_service: SupabaseImageStorageService = Depends(get_image_storage_service),
    usuario_service: UsuarioService = Depends(get_usuario_service)
):
    """
    Restaura la foto de perfil de un usuario a la imagen por defecto
    
    - **id_usuario**: ID del usuario cuya foto de perfil se restaurará
    
    Este endpoint elimina la foto de perfil personalizada (si existe) y restaura
    la imagen por defecto en la base de datos. La imagen por defecto se encuentra
    en la ruta: `usuarios/perfil/default.jpg`
    
    Requiere autenticación. Solo el usuario puede restaurar su propia foto de perfil.
    """
    # Validar que el usuario tenga permisos
    if current_user.id_usuario != id_usuario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para restaurar la foto de perfil de otro usuario"
        )
    
    # Construir la ruta base usando RutasImagenes
    ruta_base = rutas_imagenes.get_ruta_imagenes_perfil(id_usuario)
    
    # Intentar eliminar con diferentes extensiones posibles (si existe)
    extensions = [".jpg", ".jpeg", ".png", ".gif"]
    deleted = False
    
    for ext in extensions:
        file_path = f"{ruta_base}{ext}"
        result = image_service.delete(file_path)
        
        if result.get("success"):
            deleted = True
            break
    
    # Restaurar foto por defecto en la base de datos (siempre, incluso si no había imagen)
    ruta_default = "usuarios/perfil/default.jpg"
    usuario_service.actualizar_url_foto_perfil(
        id_usuario=id_usuario,
        url_publica=None,  # No se usa, solo guardamos la ruta
        ruta_storage=ruta_default
    )
    
    # Retornar respuesta exitosa
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": True,
            "message": "Foto de perfil restaurada al valor por defecto"
        }
    )

