"""
Esquemas para operaciones con almacenamiento de imágenes
"""

from pydantic import BaseModel, Field
from typing import Optional


class ImageUploadResponse(BaseModel):
    """Respuesta al subir una imagen a Supabase."""

    success: bool = Field(..., description="Si la operación fue exitosa")
    path: str = Field(..., description="Ruta del archivo en el bucket")
    bucket: str = Field(..., description="Nombre del bucket")
    public_url: Optional[str] = Field(None, description="URL pública de la imagen")
    message: Optional[str] = Field(None, description="Mensaje adicional o error")

    model_config = {
        "json_schema_extra": {
            "example": {
                "success": True,
                "path": "foto/perfil/123.jpg",
                "bucket": "images",
                "public_url": "https://tu-proyecto.supabase.co/storage/v1/object/public/images/foto/perfil/123.jpg",
                "message": "Foto de perfil subida exitosamente"
            }
        }
    }

