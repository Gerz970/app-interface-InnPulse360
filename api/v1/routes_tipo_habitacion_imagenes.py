"""
Rutas API para gestión de imágenes de tipos de habitación
Incluye endpoints para foto de perfil y galería de imágenes
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from typing import Optional
import os

from services.storage import TipoHabitacionStorageService
from schemas.storage import (
    HotelFotoPerfilResponse,
    GaleriaListResponse,
    GaleriaImageResponse
)
from sqlalchemy.orm import Session
from core.database_connection import get_database_session
from services.hotel.tipo_habitacion_service import TipoHabitacionService
from utils.rutas_imagenes import RutasImagenes
from core.supabase_client import get_supabase_client

# Configurar router
router = APIRouter(
    prefix="/tipo-habitacion",
    tags=["tipo-habitacion-imagenes"],
    responses={404: {"description": "Not found"}},
)

# Configurar seguridad
security = HTTPBearer()


def get_tipo_habitacion_storage_service() -> TipoHabitacionStorageService:
    """
    Dependency para obtener el servicio de almacenamiento de imágenes de tipos de habitación
    
    Returns:
        TipoHabitacionStorageService: Instancia del servicio
    """
    client = get_supabase_client()
    return TipoHabitacionStorageService(client=client)


def get_tipo_habitacion_service(db: Session = Depends(get_database_session)) -> TipoHabitacionService:
    """
    Dependency para obtener el servicio de tipo de habitación
    
    Args:
        db (Session): Sesión de base de datos
        
    Returns:
        TipoHabitacionService: Instancia del servicio
    """
    return TipoHabitacionService(db)


# Instancia de RutasImagenes para construir rutas consistentes
rutas_imagenes = RutasImagenes()


@router.put(
    "/{id_tipoHabitacion}/foto-perfil",
    response_model=HotelFotoPerfilResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar foto de perfil de tipo de habitación"
)
async def update_foto_perfil_tipo_habitacion(
    id_tipoHabitacion: int,
    file: UploadFile = File(..., description="Archivo de imagen (JPG, PNG, WebP)"),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    tipo_habitacion_storage_service: TipoHabitacionStorageService = Depends(get_tipo_habitacion_storage_service),
    tipo_habitacion_service: TipoHabitacionService = Depends(get_tipo_habitacion_service)
):
    """
    Actualiza o sube la foto de perfil de un tipo de habitación
    
    - **id_tipoHabitacion**: ID del tipo de habitación
    - **file**: Archivo de imagen (debe ser JPG, PNG o WebP)
    
    La imagen se guardará en la ruta: `tipo_habitacion/{id_tipoHabitacion}/{id_tipoHabitacion}.{extension}`
    Si ya existe una foto de perfil, será reemplazada automáticamente.
    Si no existe, se subirá la nueva imagen y se registrará en la base de datos.
    
    Requiere autenticación.
    """
    # Verificar que el tipo de habitación existe
    tipo_habitacion = tipo_habitacion_service.dao.get_by_id(id_tipoHabitacion)
    if not tipo_habitacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tipo de habitación con ID {id_tipoHabitacion} no encontrado"
        )
    
    # Obtener la extensión del archivo
    file_extension = os.path.splitext(file.filename or "")[1].lower()
    
    # Validar extensión
    allowed_extensions = [".jpg", ".jpeg", ".png", ".webp"]
    if not file_extension or file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Extensión de archivo no permitida. Extensiones permitidas: {', '.join(allowed_extensions)}"
        )
    
    # Leer el contenido del archivo
    try:
        file_bytes = await file.read()
        
        # Obtener el content type del archivo
        content_type = file.content_type
        
        # Subir la foto de perfil
        result = tipo_habitacion_storage_service.upload_foto_perfil(
            id_tipoHabitacion=id_tipoHabitacion,
            file_bytes=file_bytes,
            file_extension=file_extension,
            content_type=content_type
        )
        
        if not result.get("success"):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get("message", "Error al subir la imagen")
            )
        
        # Actualizar la ruta en la base de datos (solo guardamos la ruta relativa)
        tipo_habitacion_service.actualizar_url_foto_perfil(
            id_tipoHabitacion=id_tipoHabitacion,
            ruta_storage=result["path"]
        )
        
        return HotelFotoPerfilResponse(
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


@router.delete(
    "/{id_tipoHabitacion}/foto-perfil",
    status_code=status.HTTP_200_OK,
    summary="Restaurar foto de perfil por defecto"
)
async def delete_foto_perfil_tipo_habitacion(
    id_tipoHabitacion: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    tipo_habitacion_storage_service: TipoHabitacionStorageService = Depends(get_tipo_habitacion_storage_service),
    tipo_habitacion_service: TipoHabitacionService = Depends(get_tipo_habitacion_service)
):
    """
    Restaura la foto de perfil de un tipo de habitación a la imagen por defecto
    
    - **id_tipoHabitacion**: ID del tipo de habitación
    
    Este endpoint elimina la foto de perfil personalizada (si existe) y restaura
    la imagen por defecto en la base de datos. La imagen por defecto se encuentra
    en la ruta: `tipo_habitacion/{id_tipoHabitacion}/default.jpg`
    
    Requiere autenticación.
    """
    # Verificar que el tipo de habitación existe
    tipo_habitacion = tipo_habitacion_service.dao.get_by_id(id_tipoHabitacion)
    if not tipo_habitacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tipo de habitación con ID {id_tipoHabitacion} no encontrado"
        )
    
    # Eliminar foto de perfil si existe
    tipo_habitacion_storage_service.delete_foto_perfil(id_tipoHabitacion)
    
    # Restaurar foto por defecto en la base de datos
    ruta_default = rutas_imagenes.get_ruta_default_tipo_habitacion(id_tipoHabitacion)
    tipo_habitacion_service.actualizar_url_foto_perfil(
        id_tipoHabitacion=id_tipoHabitacion,
        ruta_storage=ruta_default
    )
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": True,
            "message": "Foto de perfil restaurada al valor por defecto"
        }
    )


@router.post(
    "/{id_tipoHabitacion}/galeria",
    response_model=HotelFotoPerfilResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Subir imagen a galería del tipo de habitación"
)
async def upload_galeria_tipo_habitacion(
    id_tipoHabitacion: int,
    file: UploadFile = File(..., description="Archivo de imagen (JPG, PNG, WebP)"),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    tipo_habitacion_storage_service: TipoHabitacionStorageService = Depends(get_tipo_habitacion_storage_service),
    tipo_habitacion_service: TipoHabitacionService = Depends(get_tipo_habitacion_service)
):
    """
    Sube una imagen a la galería del tipo de habitación
    
    - **id_tipoHabitacion**: ID del tipo de habitación
    - **file**: Archivo de imagen (debe ser JPG, PNG o WebP)
    
    La imagen se guardará automáticamente con el nombre: `img_{id_tipoHabitacion}_item{identificador}.{extension}`
    El nombre se genera automáticamente, no es necesario proporcionarlo.
    
    Requiere autenticación.
    """
    # Verificar que el tipo de habitación existe
    tipo_habitacion = tipo_habitacion_service.dao.get_by_id(id_tipoHabitacion)
    if not tipo_habitacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tipo de habitación con ID {id_tipoHabitacion} no encontrado"
        )
    
    # Obtener la extensión del archivo
    file_extension = os.path.splitext(file.filename or "")[1].lower()
    
    # Validar extensión
    allowed_extensions = [".jpg", ".jpeg", ".png", ".webp"]
    if not file_extension or file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Extensión de archivo no permitida. Extensiones permitidas: {', '.join(allowed_extensions)}"
        )
    
    # Leer el contenido del archivo
    try:
        file_bytes = await file.read()
        
        # Obtener el content type del archivo
        content_type = file.content_type
        
        # Subir la imagen a la galería (el nombre se genera automáticamente)
        result = tipo_habitacion_storage_service.upload_galeria(
            id_tipoHabitacion=id_tipoHabitacion,
            file_bytes=file_bytes,
            file_extension=file_extension,
            content_type=content_type
        )
        
        if not result.get("success"):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get("message", "Error al subir la imagen")
            )
        
        return HotelFotoPerfilResponse(
            success=True,
            path=result["path"],
            bucket=result["bucket"],
            public_url=result.get("public_url"),
            message="Imagen agregada a la galería exitosamente"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar la imagen: {str(e)}"
        )


@router.get(
    "/{id_tipoHabitacion}/galeria",
    response_model=GaleriaListResponse,
    summary="Listar imágenes de la galería del tipo de habitación"
)
async def list_galeria_tipo_habitacion(
    id_tipoHabitacion: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    tipo_habitacion_storage_service: TipoHabitacionStorageService = Depends(get_tipo_habitacion_storage_service),
    tipo_habitacion_service: TipoHabitacionService = Depends(get_tipo_habitacion_service)
):
    """
    Lista todas las imágenes de la galería de un tipo de habitación
    
    - **id_tipoHabitacion**: ID del tipo de habitación
    
    Retorna una lista de todas las imágenes almacenadas en la carpeta
    `tipo_habitacion/{id_tipoHabitacion}/galeria/` con sus URLs públicas.
    
    Requiere autenticación.
    """
    # Verificar que el tipo de habitación existe
    tipo_habitacion = tipo_habitacion_service.dao.get_by_id(id_tipoHabitacion)
    if not tipo_habitacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tipo de habitación con ID {id_tipoHabitacion} no encontrado"
        )
    
    # Listar imágenes de la galería
    result = tipo_habitacion_storage_service.list_galeria(id_tipoHabitacion)
    
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.get("message", "Error al listar la galería")
        )
    
    # Convertir a schema de respuesta
    imagenes = [
        GaleriaImageResponse(**img) for img in result.get("imagenes", [])
    ]
    
    return GaleriaListResponse(
        success=True,
        imagenes=imagenes,
        total=result.get("total", 0),
        message=None
    )


@router.delete(
    "/{id_tipoHabitacion}/galeria/{nombre_archivo}",
    status_code=status.HTTP_200_OK,
    summary="Eliminar imagen de la galería del tipo de habitación"
)
async def delete_galeria_tipo_habitacion(
    id_tipoHabitacion: int,
    nombre_archivo: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    tipo_habitacion_storage_service: TipoHabitacionStorageService = Depends(get_tipo_habitacion_storage_service),
    tipo_habitacion_service: TipoHabitacionService = Depends(get_tipo_habitacion_service)
):
    """
    Elimina una imagen específica de la galería del tipo de habitación
    
    - **id_tipoHabitacion**: ID del tipo de habitación
    - **nombre_archivo**: Nombre del archivo a eliminar (ej: "img_1_item1a2b3c.jpg")
    
    Requiere autenticación.
    """
    # Verificar que el tipo de habitación existe
    tipo_habitacion = tipo_habitacion_service.dao.get_by_id(id_tipoHabitacion)
    if not tipo_habitacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tipo de habitación con ID {id_tipoHabitacion} no encontrado"
        )
    
    # Eliminar imagen de la galería
    result = tipo_habitacion_storage_service.delete_galeria(id_tipoHabitacion, nombre_archivo)
    
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.get("message", "Error al eliminar la imagen")
        )
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": True,
            "message": f"Imagen '{nombre_archivo}' eliminada exitosamente de la galería"
        }
    )

