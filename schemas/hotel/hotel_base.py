from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional


class HotelBase(BaseModel):
    """
    Schema base para Hotel con campos comunes
    Contiene todos los campos que son comunes entre Create, Update y Response
    """
    nombre: str = Field(
        ..., # Los tres puntos significan que el campo es requerido
        min_length=1, 
        max_length=150,
        description="Nombre del hotel",
        example="Hotel Plaza Madrid"
    )
    
    direccion: str = Field(
        ..., # Los tres puntos significan que el campo es requerido
        min_length=1, 
        max_length=200,
        description="Dirección física del hotel",
        example="Calle Gran Vía, 123"
    )
    
    id_pais: int = Field(
        ..., # Los tres puntos significan que el campo es requerido
        gt=0,
        description="ID del país donde se encuentra el hotel",
        example=1
    )
    
    id_estado: Optional[int] = Field(
        None, # None significa que el campo es opcional
        gt=0,
        description="ID del estado/provincia del hotel",
        example=15
    )
    
    codigo_postal: Optional[str] = Field(
        None, # None significa que el campo es opcional
        max_length=20,
        description="Código postal del hotel",
        example="28013"
    )
    
    telefono: Optional[str] = Field(
        None, # None significa que el campo es opcional
        max_length=30,
        description="Teléfono de contacto del hotel",
        example="+34 91 123 45 67"
    )
    
    email_contacto: Optional[str] = Field(
        None, # None significa que el campo es opcional
        max_length=150,
        description="Email de contacto del hotel",
        example="reservas@hotelplaza.com"
    )
    
    numero_estrellas: Optional[int] = Field(
        None, # None significa que el campo es opcional
        ge=1, 
        le=5,
        description="Número de estrellas del hotel (1-5)",
        example=4
    )
    
    @validator('email_contacto')
    def validate_email(cls, v):
        # v es el valor del campo email_contacto
        # cls es la clase HotelBase
        # El validator es una función que se ejecuta cuando se valida el campo email_contacto
        if v and '@' not in v:
            raise ValueError('El email debe tener un formato válido')
        return v
    
    @validator('telefono')
    def validate_phone(cls, v):
        # v es el valor del campo telefono
        # cls es la clase HotelBase
        # El validator es una función que se ejecuta cuando se valida el campo telefono
        if v and not v.replace('+', '').replace(' ', '').replace('-', '').replace('(', '').replace(')', '').isdigit():
            raise ValueError('El teléfono debe contener solo números y caracteres permitidos')
        return v
