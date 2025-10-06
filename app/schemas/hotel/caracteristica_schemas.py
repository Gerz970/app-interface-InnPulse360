from pydantic import BaseModel, Field
from typing import Optional


class CaracteristicaCreate(BaseModel):
    """
    Schema para crear una nueva característica
    """
    caracteristica: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Nombre de la característica",
        example="WiFi"
    )
    
    descripcion: Optional[str] = Field(
        None,
        max_length=500,
        description="Descripción de la característica",
        example="Conexión inalámbrica a internet"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "caracteristica": "WiFi",
                "descripcion": "Conexión inalámbrica a internet"
            }
        }


class CaracteristicaUpdate(BaseModel):
    """
    Schema para actualizar una característica existente
    """
    caracteristica: Optional[str] = Field(
        None,
        min_length=1,
        max_length=50,
        description="Nombre de la característica",
        example="WiFi Actualizado"
    )
    
    descripcion: Optional[str] = Field(
        None,
        max_length=500,
        description="Descripción de la característica",
        example="Conexión inalámbrica a internet de alta velocidad"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "caracteristica": "WiFi Actualizado",
                "descripcion": "Conexión inalámbrica a internet de alta velocidad"
            }
        }


class CaracteristicaResponse(BaseModel):
    """
    Schema para respuesta de característica
    """
    id_caracteristica: int = Field(
        ...,
        description="ID único de la característica",
        example=1
    )
    
    caracteristica: str = Field(
        ...,
        description="Nombre de la característica",
        example="WiFi"
    )
    
    descripcion: Optional[str] = Field(
        None,
        description="Descripción de la característica",
        example="Conexión inalámbrica a internet"
    )
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id_caracteristica": 1,
                "caracteristica": "WiFi",
                "descripcion": "Conexión inalámbrica a internet"
            }
        }
