from pydantic import BaseModel, Field, condecimal
from typing import Optional, List
from decimal import Decimal
from ..catalogos.periodicidad_schemas import PeriodicidadResponse

Precio = condecimal(max_digits=6, decimal_places=2, ge=0, le=9999.99)

class TipoHabitacionBase(BaseModel):
    """Schema base con campos comunes"""
    clave: str = Field(..., max_length=10, description="Clave del tipo de habitación")
    precio_unitario: Decimal = Field(..., ge=0, decimal_places=2, description="Precio unitario")
    periodicidad_id: int = Field(..., gt=0, description="ID de periodicidad")
    tipo_habitacion: str = Field(..., max_length=25, description="Nombre del tipo de habitación")
    estatus_id: int = Field(..., gt=0, description="ID de estatus")

class TipoHabitacionCreate(TipoHabitacionBase):
    """Schema para crear un tipo de habitación"""
    pass

# Schema para actualizar
class TipoHabitacionUpdate(BaseModel):
    clave: Optional[str] = Field(None, max_length=10, example="SGL")
    tipo_habitacion: Optional[str] = Field(None, min_length=1, max_length=25, example="Individual Actualizado")
    precio_unitario: Optional[Decimal] = Field(None, gt=0, example=1200.50)
    periodicidad_id: Optional[int] = Field(None, example=2)
    estatus_id: Optional[int] = Field(None, gt=0, example=1)
    url_foto_perfil: Optional[str] = Field(None, max_length=500, description="Ruta relativa de la foto de perfil")

# Schema de respuesta
class TipoHabitacionResponse(TipoHabitacionBase):
    """Schema para respuestas (incluye el ID)"""
    id_tipoHabitacion: int = Field(..., description="ID único del tipo de habitación")
    periodicidad: Optional[PeriodicidadResponse]
    url_foto_perfil: Optional[str] = Field(None, description="URL pública de la foto de perfil")
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id_tipoHabitacion": 1,
                "clave": "SGL",
                "tipo_habitacion": "Individual",
                "precio_unitario": 1000,
                "periodicidad": {
                "id_periodicidad": 1,
                "periodicidad": "Temporal",
                "descripcion": "Tiempo indefinido",
                "id_estatus": 1
                },
                "estatus_id": 1,
                "url_foto_perfil": "https://tu-proyecto.supabase.co/storage/v1/object/public/images/tipo_habitacion/1/default.jpg"
            }
        }
