from pydantic import BaseModel, Field
from typing import Optional, List


class TipoHabitacionCreate(BaseModel):
    """
    Schema para crear un nuevo tipo de habitación
    """
    clave: Optional[str] = Field(
        None,
        max_length=10,
        description="Clave del tipo de habitación",
        example="SGL"
    )
    
    tipo_habitacion: str = Field(
        ...,
        min_length=1,
        max_length=25,
        description="Nombre del tipo de habitación",
        example="Individual"
    )
    
    estatus_id: Optional[int] = Field(
        1,  # Valor por defecto activo
        gt=0,
        description="Estatus del tipo de habitación (1=Activo por defecto)",
        example=1
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "clave": "SGL",
                "tipo_habitacion": "Individual",
                "estatus_id": 1
            }
        }


class TipoHabitacionUpdate(BaseModel):
    """
    Schema para actualizar un tipo de habitación existente
    """
    clave: Optional[str] = Field(
        None,
        max_length=10,
        description="Clave del tipo de habitación",
        example="SGL"
    )
    
    tipo_habitacion: Optional[str] = Field(
        None,
        min_length=1,
        max_length=25,
        description="Nombre del tipo de habitación",
        example="Individual Actualizado"
    )
    
    estatus_id: Optional[int] = Field(
        None,
        gt=0,
        description="Estatus del tipo de habitación",
        example=1
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "clave": "SGL",
                "tipo_habitacion": "Individual Actualizado",
                "estatus_id": 1
            }
        }


class TipoHabitacionResponse(BaseModel):
    """
    Schema para respuesta de tipo de habitación
    """
    id_tipoHabitacion: int = Field(
        ...,
        description="ID único del tipo de habitación",
        example=1
    )
    
    clave: Optional[str] = Field(
        None,
        description="Clave del tipo de habitación",
        example="SGL"
    )
    
    tipo_habitacion: str = Field(
        ...,
        description="Nombre del tipo de habitación",
        example="Individual"
    )
    
    estatus_id: int = Field(
        ...,
        description="Estatus del tipo de habitación",
        example=1
    )
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id_tipoHabitacion": 1,
                "clave": "SGL",
                "tipo_habitacion": "Individual",
                "estatus_id": 1
            }
        }
