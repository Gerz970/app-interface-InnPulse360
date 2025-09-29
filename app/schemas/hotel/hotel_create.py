from pydantic import BaseModel
from .hotel_base import HotelBase


class HotelCreate(HotelBase):
    """
    Schema para crear un nuevo hotel
    Hereda todos los campos de HotelBase
    No incluye el ID porque se genera automáticamente
    """
    
    class Config:
        json_schema_extra = {
            "example": {
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
