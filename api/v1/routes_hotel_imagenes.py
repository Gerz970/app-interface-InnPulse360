"""
Rutas API para gestión de imágenes de hoteles
Incluye endpoints para foto de perfil y galería de imágenes
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from typing import Optional
import os

from services.storage import HotelStorageService
from schemas.storage import (
    HotelFotoPerfilResponse,
    GaleriaListResponse,
    GaleriaImageResponse
)
from sqlalchemy.orm import Session
from core.database_connection import get_database_session
from services.hotel.hotel_service import HotelService
from utils.rutas_imagenes import RutasImagenes

# Configurar router
router = APIRouter(
    prefix="/hotel",
    tags=["hotel-imagenes"],
    responses={404: {"description": "Not found"}},
)

# Configurar seguridad
security = HTTPBearer()


def get_hotel_storage_service() -> HotelStorageService:
    """
    Dependency para obtener el servicio de almacenamiento de imágenes de hoteles
    
    Returns:
        HotelStorageService: Instancia del servicio
    """
    return HotelStorageService()


def get_hotel_service(db: Session = Depends(get_database_session)) -> HotelService:
    """
    Dependency para obtener el servicio de hotel
    
    Args:
        db (Session): Sesión de base de datos
        
    Returns:
        HotelService: Instancia del servicio
    """
    return HotelService(db)


# Instancia de RutasImagenes para construir rutas consistentes
rutas_imagenes = RutasImagenes()


@router.put(
    "/{id_hotel}/foto-perfil",
    response_model=HotelFotoPerfilResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar foto de perfil de hotel"
)
async def update_foto_perfil_hotel(
    id_hotel: int,
    file: UploadFile = File(..., description="Archivo de imagen (JPG, PNG, WebP)"),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    hotel_storage_service: HotelStorageService = Depends(get_hotel_storage_service),
    hotel_service: HotelService = Depends(get_hotel_service)
):
    """
    Actualiza o sube la foto de perfil de un hotel
    
    - **id_hotel**: ID del hotel
    - **file**: Archivo de imagen (debe ser JPG, PNG o WebP)
    
    La imagen se guardará en la ruta: `hotel/{id_hotel}/{id_hotel}.{extension}`
    Si ya existe una foto de perfil, será reemplazada automáticamente.
    Si no existe, se subirá la nueva imagen y se registrará en la base de datos.
    
    Requiere autenticación.
    """
    # Verificar que el hotel existe
    hotel = hotel_service.dao.get_by_id(id_hotel)
    if not hotel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hotel con ID {id_hotel} no encontrado"
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
        result = hotel_storage_service.upload_foto_perfil(
            id_hotel=id_hotel,
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
        hotel_service.actualizar_url_foto_perfil(
            id_hotel=id_hotel,
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
    "/{id_hotel}/foto-perfil",
    status_code=status.HTTP_200_OK,
    summary="Restaurar foto de perfil por defecto"
)
async def delete_foto_perfil_hotel(
    id_hotel: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    hotel_storage_service: HotelStorageService = Depends(get_hotel_storage_service),
    hotel_service: HotelService = Depends(get_hotel_service)
):
    """
    Restaura la foto de perfil de un hotel a la imagen por defecto
    
    - **id_hotel**: ID del hotel
    
    Este endpoint elimina la foto de perfil personalizada (si existe) y restaura
    la imagen por defecto en la base de datos. La imagen por defecto se encuentra
    en la ruta: `hotel/{id_hotel}/default.jpg`
    
    Requiere autenticación.
    """
    # Verificar que el hotel existe
    hotel = hotel_service.dao.get_by_id(id_hotel)
    if not hotel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hotel con ID {id_hotel} no encontrado"
        )
    
    # Eliminar foto de perfil si existe
    hotel_storage_service.delete_foto_perfil(id_hotel)
    
    # Restaurar foto por defecto en la base de datos
    ruta_default = rutas_imagenes.get_ruta_default_hotel(id_hotel)
    hotel_service.actualizar_url_foto_perfil(
        id_hotel=id_hotel,
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
    "/{id_hotel}/galeria",
    response_model=HotelFotoPerfilResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Subir imagen a galería del hotel"
)
async def upload_galeria_hotel(
    id_hotel: int,
    file: UploadFile = File(..., description="Archivo de imagen (JPG, PNG, WebP)"),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    hotel_storage_service: HotelStorageService = Depends(get_hotel_storage_service),
    hotel_service: HotelService = Depends(get_hotel_service)
):
    """
    Sube una imagen a la galería del hotel
    
    - **id_hotel**: ID del hotel
    - **file**: Archivo de imagen (debe ser JPG, PNG o WebP)
    
    La imagen se guardará automáticamente con el nombre: `img_{id_hotel}_item{identificador}.{extension}`
    El nombre se genera automáticamente, no es necesario proporcionarlo.
    
    Requiere autenticación.
    """
    # Verificar que el hotel existe
    hotel = hotel_service.dao.get_by_id(id_hotel)
    if not hotel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hotel con ID {id_hotel} no encontrado"
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
        result = hotel_storage_service.upload_galeria(
            id_hotel=id_hotel,
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
    "/{id_hotel}/galeria",
    response_model=GaleriaListResponse,
    summary="Listar imágenes de la galería del hotel"
)
async def list_galeria_hotel(
    id_hotel: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    hotel_storage_service: HotelStorageService = Depends(get_hotel_storage_service),
    hotel_service: HotelService = Depends(get_hotel_service)
):
    """
    Lista todas las imágenes de la galería de un hotel
    
    - **id_hotel**: ID del hotel
    
    Retorna una lista de todas las imágenes almacenadas en la carpeta
    `hotel/{id_hotel}/galeria/` con sus URLs públicas.
    
    Requiere autenticación.
    """
    # Verificar que el hotel existe
    hotel = hotel_service.dao.get_by_id(id_hotel)
    if not hotel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hotel con ID {id_hotel} no encontrado"
        )
    
    # Listar imágenes de la galería
    result = hotel_storage_service.list_galeria(id_hotel)
    
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
    "/{id_hotel}/galeria/{nombre_archivo}",
    status_code=status.HTTP_200_OK,
    summary="Eliminar imagen de la galería del hotel"
)
async def delete_galeria_hotel(
    id_hotel: int,
    nombre_archivo: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    hotel_storage_service: HotelStorageService = Depends(get_hotel_storage_service),
    hotel_service: HotelService = Depends(get_hotel_service)
):
    """
    Elimina una imagen específica de la galería del hotel
    
    - **id_hotel**: ID del hotel
    - **nombre_archivo**: Nombre del archivo a eliminar (ej: "1a2b3c.jpg")
    
    Requiere autenticación.
    """
    # Verificar que el hotel existe
    hotel = hotel_service.dao.get_by_id(id_hotel)
    if not hotel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hotel con ID {id_hotel} no encontrado"
        )
    
    # Eliminar imagen de la galería
    result = hotel_storage_service.delete_galeria(id_hotel, nombre_archivo)
    
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

