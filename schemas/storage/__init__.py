"""
Paquete para esquemas relacionados con almacenamiento en Supabase.
"""

from .image_schemas import ImageUploadResponse
from .hotel_image_schemas import (
    HotelFotoPerfilResponse,
    GaleriaImageResponse,
    GaleriaListResponse
)

__all__ = [
    "ImageUploadResponse",
    "HotelFotoPerfilResponse",
    "GaleriaImageResponse",
    "GaleriaListResponse"
]

