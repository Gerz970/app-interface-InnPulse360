"""
Rutas API para gestión de imágenes de mantenimiento
Incluye endpoints para galería de imágenes
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from typing import Optional
import os

from services.storage import MantenimientoStorageService
from schemas.storage import (
    HotelFotoPerfilResponse,
    GaleriaListResponse,
    GaleriaImageResponse
)
from sqlalchemy.orm import Session
from core.database_connection import get_database_session
from services.mantenimiento.mantenimiento_service import MantenimientoService

# Configurar router
router = APIRouter(
    prefix="/mantenimientos",
    tags=["mantenimiento-imagenes"],
    responses={404: {"description": "Not found"}},
)

# Configurar seguridad
security = HTTPBearer()


def get_mantenimiento_storage_service() -> MantenimientoStorageService:
    """
    Dependency para obtener el servicio de almacenamiento de imágenes de mantenimiento
    
    Returns:
        MantenimientoStorageService: Instancia del servicio
    """
    return MantenimientoStorageService()


def get_mantenimiento_service(db: Session = Depends(get_database_session)) -> MantenimientoService:
    """
    Dependency para obtener el servicio de mantenimiento
    
    Args:
        db (Session): Sesión de base de datos
        
    Returns:
        MantenimientoService: Instancia del servicio
    """
    return MantenimientoService()


@router.post(
    "/{id_mantenimiento}/galeria",
    response_model=HotelFotoPerfilResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Subir imagen a galería del mantenimiento"
)
async def upload_galeria_mantenimiento(
    id_mantenimiento: int,
    tipo: str = Query(..., description="Tipo de imagen: 'antes' o 'despues'", pattern="^(antes|despues)$"),
    file: UploadFile = File(..., description="Archivo de imagen (JPG, PNG, WebP)"),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    mantenimiento_storage_service: MantenimientoStorageService = Depends(get_mantenimiento_storage_service),
    mantenimiento_service: MantenimientoService = Depends(get_mantenimiento_service),
    db: Session = Depends(get_database_session)
):
    """
    Sube una imagen a la galería del mantenimiento
    
    - **id_mantenimiento**: ID del mantenimiento
    - **tipo**: Tipo de imagen ("antes" o "despues") - requerido
    - **file**: Archivo de imagen (debe ser JPG, PNG o WebP)
    
    La imagen se guardará automáticamente con el nombre: `img_{id_mantenimiento}_item{identificador}.{extension}`
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
    
    # Verificar que el mantenimiento existe
    mantenimiento = mantenimiento_service.obtener_por_id(db, id_mantenimiento)
    if not mantenimiento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mantenimiento con ID {id_mantenimiento} no encontrado"
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
        result = mantenimiento_storage_service.upload_galeria(
            id_mantenimiento=id_mantenimiento,
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
    "/{id_mantenimiento}/galeria",
    response_model=GaleriaListResponse,
    summary="Listar imágenes de la galería del mantenimiento"
)
async def list_galeria_mantenimiento(
    id_mantenimiento: int,
    tipo: Optional[str] = Query(None, description="Tipo de imagen a listar: 'antes', 'despues' o None para ambas"),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    mantenimiento_storage_service: MantenimientoStorageService = Depends(get_mantenimiento_storage_service),
    mantenimiento_service: MantenimientoService = Depends(get_mantenimiento_service),
    db: Session = Depends(get_database_session)
):
    """
    Lista las imágenes de la galería de un mantenimiento
    
    - **id_mantenimiento**: ID del mantenimiento
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
    
    # Verificar que el mantenimiento existe
    mantenimiento = mantenimiento_service.obtener_por_id(db, id_mantenimiento)
    if not mantenimiento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mantenimiento con ID {id_mantenimiento} no encontrado"
        )
    
    # Listar imágenes de la galería
    result = mantenimiento_storage_service.list_galeria(id_mantenimiento, tipo=tipo)
    
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
    "/{id_mantenimiento}/galeria/{nombre_archivo}",
    status_code=status.HTTP_200_OK,
    summary="Eliminar imagen de la galería del mantenimiento"
)
async def delete_galeria_mantenimiento(
    id_mantenimiento: int,
    nombre_archivo: str,
    tipo: str = Query(..., description="Tipo de imagen: 'antes' o 'despues'", pattern="^(antes|despues)$"),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    mantenimiento_storage_service: MantenimientoStorageService = Depends(get_mantenimiento_storage_service),
    mantenimiento_service: MantenimientoService = Depends(get_mantenimiento_service),
    db: Session = Depends(get_database_session)
):
    """
    Elimina una imagen específica de la galería del mantenimiento
    
    - **id_mantenimiento**: ID del mantenimiento
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
    
    # Verificar que el mantenimiento existe
    mantenimiento = mantenimiento_service.obtener_por_id(db, id_mantenimiento)
    if not mantenimiento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mantenimiento con ID {id_mantenimiento} no encontrado"
        )
    
    # Eliminar imagen de la galería
    result = mantenimiento_storage_service.delete_galeria(id_mantenimiento, nombre_archivo, tipo=tipo)
    
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

