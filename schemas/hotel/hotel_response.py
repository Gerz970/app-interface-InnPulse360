from pydantic import BaseModel, Field
from typing import Optional
from .hotel_base import HotelBase


class HotelResponse(HotelBase):
    """
    Schema para respuestas de la API
    Incluye el ID del hotel y hereda todos los campos de HotelBase
    """
    id_hotel: int = Field(
        ..., 
        description="ID único del hotel",
        example=1
    )
    
    url_foto_perfil: Optional[str] = Field(
        None,
        description="URL pública de la foto de perfil del hotel",
        example="https://innpulse360.supabase.co/storage/v1/object/public/images/hotel/123/123.jpg"
    )
    
    class Config:
        # Permite conversión desde SQLAlchemy models
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id_hotel": 1,
                "nombre": "Hotel Plaza Madrid",
                "direccion": "Calle Gran Vía, 123, 28013 Madrid",
                "id_pais": 1,
                "id_estado": 15,
                "codigo_postal": "28013",
                "telefono": "+34 91 123 45 67",
                "email_contacto": "reservas@hotelplaza.com",
                "numero_estrellas": 4
            }
        }
