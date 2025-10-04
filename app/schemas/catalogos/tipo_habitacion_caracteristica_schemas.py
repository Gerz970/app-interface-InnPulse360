from pydantic import BaseModel, Field
from typing import List


class TipoHabitacionCaracteristicaAssign(BaseModel):
    """
    Schema para asignar una característica a un tipo de habitación
    """
    tipo_habitacion_id: int = Field(
        ...,
        description="ID del tipo de habitación",
        example=1
    )
    
    caracteristica_id: int = Field(
        ...,
        description="ID de la característica",
        example=1
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "tipo_habitacion_id": 1,
                "caracteristica_id": 1
            }
        }


class TipoHabitacionCaracteristicaBulkAssign(BaseModel):
    """
    Schema para asignación masiva de características a un tipo de habitación
    """
    caracteristicas_ids: List[int] = Field(
        ...,
        description="Lista de IDs de características a asignar",
        example=[1, 2, 3]
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "caracteristicas_ids": [1, 2, 3]
            }
        }


class TipoHabitacionCaracteristicaResponse(BaseModel):
    """
    Schema para respuesta de asignación tipo de habitación - característica
    """
    tipo_habitacion_id: int = Field(
        ...,
        description="ID del tipo de habitación",
        example=1
    )
    
    caracteristica_id: int = Field(
        ...,
        description="ID de la característica",
        example=1
    )
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "tipo_habitacion_id": 1,
                "caracteristica_id": 1
            }
        }
