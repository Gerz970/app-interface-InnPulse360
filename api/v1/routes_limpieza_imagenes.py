"""
Rutas API para gestión de imágenes de limpieza
Incluye endpoints para galería de imágenes
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from typing import Optional
import os

from services.storage import LimpiezaStorageService
from schemas.storage import (
    HotelFotoPerfilResponse,
    GaleriaListResponse,
    GaleriaImageResponse
)
from sqlalchemy.orm import Session
from core.database_connection import get_database_session
from services.camarista.limpieza_service import LimpiezaService

# Configurar router
router = APIRouter(
    prefix="/limpiezas",
    tags=["limpieza-imagenes"],
    responses={404: {"description": "Not found"}},
)

# Configurar seguridad
security = HTTPBearer()


def get_limpieza_storage_service() -> LimpiezaStorageService:
    """
    Dependency para obtener el servicio de almacenamiento de imágenes de limpieza
    
    Returns:
        LimpiezaStorageService: Instancia del servicio
    """
    return LimpiezaStorageService()


def get_limpieza_service(db: Session = Depends(get_database_session)) -> LimpiezaService:
    """
    Dependency para obtener el servicio de limpieza
    
    Args:
        db (Session): Sesión de base de datos
        
    Returns:
        LimpiezaService: Instancia del servicio
    """
    return LimpiezaService()


@router.post(
    "/{id_limpieza}/galeria",
    response_model=HotelFotoPerfilResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Subir imagen a galería de la limpieza"
)
async def upload_galeria_limpieza(
    id_limpieza: int,
    tipo: str = Query(..., description="Tipo de imagen: 'antes' o 'despues'", pattern="^(antes|despues)$"),
    file: UploadFile = File(..., description="Archivo de imagen (JPG, PNG, WebP)"),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    limpieza_storage_service: LimpiezaStorageService = Depends(get_limpieza_storage_service),
    limpieza_service: LimpiezaService = Depends(get_limpieza_service),
    db: Session = Depends(get_database_session)
):
    """
    Sube una imagen a la galería de la limpieza
    
    - **id_limpieza**: ID de la limpieza
    - **tipo**: Tipo de imagen ("antes" o "despues") - requerido
    - **file**: Archivo de imagen (debe ser JPG, PNG o WebP)
    
    La imagen se guardará automáticamente con el nombre: `img_{id_limpieza}_item{identificador}.{extension}`
    en la subcarpeta correspondiente según el tipo especificado.
    
    Requiere autenticación.
    """
    # Validar tipo
    tipo = tipo.lower()
    if tipo not in ("antes", "despues"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo no permitido. Tipos permitidos: 'antes' o 'despues'"
        )
    
    # Verificar que la limpieza existe
    limpieza = limpieza_service.obtener_por_id(db, id_limpieza)
    if not limpieza:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Limpieza con ID {id_limpieza} no encontrada"
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
        result = limpieza_storage_service.upload_galeria(
            id_limpieza=id_limpieza,
            file_bytes=file_bytes,
            file_extension=file_extension,
            tipo=tipo,
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
    "/{id_limpieza}/galeria",
    response_model=GaleriaListResponse,
    summary="Listar imágenes de la galería de la limpieza"
)
async def list_galeria_limpieza(
    id_limpieza: int,
    tipo: Optional[str] = Query(None, description="Tipo de imagen a listar: 'antes', 'despues' o None para ambas"),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    limpieza_storage_service: LimpiezaStorageService = Depends(get_limpieza_storage_service),
    limpieza_service: LimpiezaService = Depends(get_limpieza_service),
    db: Session = Depends(get_database_session)
):
    """
    Lista las imágenes de la galería de una limpieza
    
    - **id_limpieza**: ID de la limpieza
    - **tipo**: Tipo de imagen a listar ("antes", "despues" o None para ambas) - opcional
    
    Si se especifica `tipo`, retorna solo las imágenes de esa categoría.
    Si no se especifica, retorna todas las imágenes (antes y despues) con el campo `tipo` indicando su categoría.
    
    Requiere autenticación.
    """
    # Validar tipo si se proporciona
    if tipo:
        tipo = tipo.lower()
        if tipo not in ("antes", "despues"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tipo no permitido. Tipos permitidos: 'antes' o 'despues'"
            )
    
    # Verificar que la limpieza existe
    limpieza = limpieza_service.obtener_por_id(db, id_limpieza)
    if not limpieza:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Limpieza con ID {id_limpieza} no encontrada"
        )
    
    # Listar imágenes de la galería
    result = limpieza_storage_service.list_galeria(id_limpieza, tipo=tipo)
    
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
    "/{id_limpieza}/galeria/{nombre_archivo}",
    status_code=status.HTTP_200_OK,
    summary="Eliminar imagen de la galería de la limpieza"
)
async def delete_galeria_limpieza(
    id_limpieza: int,
    nombre_archivo: str,
    tipo: str = Query(..., description="Tipo de imagen: 'antes' o 'despues'", pattern="^(antes|despues)$"),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    limpieza_storage_service: LimpiezaStorageService = Depends(get_limpieza_storage_service),
    limpieza_service: LimpiezaService = Depends(get_limpieza_service),
    db: Session = Depends(get_database_session)
):
    """
    Elimina una imagen específica de la galería de la limpieza
    
    - **id_limpieza**: ID de la limpieza
    - **nombre_archivo**: Nombre del archivo a eliminar (ej: "img_123_itema1b2c3d4.jpg")
    - **tipo**: Tipo de imagen ("antes" o "despues") - requerido
    
    Requiere autenticación.
    """
    # Validar tipo
    tipo = tipo.lower()
    if tipo not in ("antes", "despues"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo no permitido. Tipos permitidos: 'antes' o 'despues'"
        )
    
    # Verificar que la limpieza existe
    limpieza = limpieza_service.obtener_por_id(db, id_limpieza)
    if not limpieza:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Limpieza con ID {id_limpieza} no encontrada"
        )
    
    # Eliminar imagen de la galería
    result = limpieza_storage_service.delete_galeria(id_limpieza, nombre_archivo, tipo=tipo)
    
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

