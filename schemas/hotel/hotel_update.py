from pydantic import BaseModel, Field
from typing import Optional


class HotelUpdate(BaseModel):
    """
    Schema para actualizar un hotel existente
    Todos los campos son opcionales para permitir actualizaciones parciales
    """
    nombre: Optional[str] = Field(
        None, 
        min_length=1, 
        max_length=150,
        description="Nombre del hotel",
        example="Hotel Plaza Madrid Centro"
    )
    
    direccion: Optional[str] = Field(
        None, 
        min_length=1, 
        max_length=200,
        description="Dirección física del hotel",
        example="Calle Gran Vía, 456, 28013 Madrid"
    )
    
    id_pais: Optional[int] = Field(
        None, 
        gt=0,
        description="ID del país donde se encuentra el hotel",
        example=1
    )
    
    id_estado: Optional[int] = Field(
        None, 
        gt=0,
        description="ID del estado/provincia del hotel",
        example=15
    )
    
    codigo_postal: Optional[str] = Field(
        None, 
        max_length=20,
        description="Código postal del hotel",
        example="28014"
    )
    
    telefono: Optional[str] = Field(
        None, 
        max_length=30,
        description="Teléfono de contacto del hotel",
        example="+34 91 987 65 43"
    )
    
    email_contacto: Optional[str] = Field(
        None, 
        max_length=150,
        description="Email de contacto del hotel",
        example="info@hotelplaza.com"
    )
    
    numero_estrellas: Optional[int] = Field(
        None, 
        ge=1, 
        le=5,
        description="Número de estrellas del hotel (1-5)",
        example=5
    )
    
    url_foto_perfil: Optional[str] = Field(
        None,
        max_length=500,
        description="Ruta relativa de la foto de perfil del hotel",
        example="hotel/123/123.jpg"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "nombre": "Hotel Plaza Madrid Centro",
                "telefono": "+34 91 987 65 43",
                "numero_estrellas": 5
            }
        }
