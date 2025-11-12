"""
Schemas para respuestas de operaciones con imágenes de hoteles
"""

from pydantic import BaseModel, Field
from typing import Optional, List


class HotelFotoPerfilResponse(BaseModel):
    """
    Schema para respuesta de foto de perfil de hotel
    """
    success: bool = Field(
        ...,
        description="Si la operación fue exitosa"
    )
    
    path: str = Field(
        ...,
        description="Ruta del archivo en el bucket"
    )
    
    bucket: str = Field(
        ...,
        description="Nombre del bucket"
    )
    
    public_url: Optional[str] = Field(
        None,
        description="URL pública de la foto de perfil"
    )
    
    message: Optional[str] = Field(
        None,
        description="Mensaje adicional o error"
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "success": True,
                "path": "hotel/123/123.jpg",
                "bucket": "images",
                "public_url": "https://tu-proyecto.supabase.co/storage/v1/object/public/images/hotel/123/123.jpg",
                "message": "Foto de perfil actualizada exitosamente"
            }
        }
    }


class GaleriaImageResponse(BaseModel):
    """
    Schema para una imagen individual en la galería
    """
    nombre: str = Field(
        ...,
        description="Nombre del archivo"
    )
    
    ruta: str = Field(
        ...,
        description="Ruta completa del archivo en el bucket"
    )
    
    url_publica: Optional[str] = Field(
        None,
        description="URL pública de la imagen"
    )
    
    tamaño: int = Field(
        default=0,
        description="Tamaño del archivo en bytes"
    )
    
    tipo: Optional[str] = Field(
        None,
        description="Tipo de imagen: 'antes' o 'despues' (solo para mantenimientos)"
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "nombre": "1a2b3c.jpg",
                "ruta": "hotel/123/galeria/1a2b3c.jpg",
                "url_publica": "https://tu-proyecto.supabase.co/storage/v1/object/public/images/hotel/123/galeria/1a2b3c.jpg",
                "tamaño": 245678,
                "tipo": None
            }
        }
    }


class GaleriaListResponse(BaseModel):
    """
    Schema para respuesta de listado de galería
    """
    success: bool = Field(
        ...,
        description="Si la operación fue exitosa"
    )
    
    imagenes: List[GaleriaImageResponse] = Field(
        default_factory=list,
        description="Lista de imágenes en la galería"
    )
    
    total: int = Field(
        default=0,
        description="Total de imágenes en la galería"
    )
    
    message: Optional[str] = Field(
        None,
        description="Mensaje adicional o error"
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "success": True,
                "imagenes": [
                    {
                        "nombre": "1a2b3c.jpg",
                        "ruta": "hotel/123/galeria/1a2b3c.jpg",
                        "url_publica": "https://tu-proyecto.supabase.co/storage/v1/object/public/images/hotel/123/galeria/1a2b3c.jpg",
                        "tamaño": 245678
                    }
                ],
                "total": 1,
                "message": None
            }
        }
    }

