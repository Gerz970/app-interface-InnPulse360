from pydantic import BaseModel, Field
from typing import Optional
from .pais_schemas import PaisResponse


class EstadoCreate(BaseModel):
    """
    Schema para crear un nuevo estado
    """
    id_pais: int = Field(
        ...,
        description="ID del país al que pertenece el estado",
        example=1
    )
    
    nombre: str = Field(
        ...,
        min_length=1,
        max_length=250,
        description="Nombre del estado",
        example="Jalisco"
    )
    
    id_estatus: Optional[int] = Field(
        1,  # Valor por defecto activo
        gt=0,
        description="Estatus del estado (1=Activo por defecto)",
        example=1
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "id_pais": 1,
                "nombre": "Jalisco",
                "id_estatus": 1
            }
        }


class EstadoUpdate(BaseModel):
    """
    Schema para actualizar un estado existente
    """
    id_pais: Optional[int] = Field(
        None,
        description="ID del país al que pertenece el estado",
        example=1
    )
    
    nombre: Optional[str] = Field(
        None,
        min_length=1,
        max_length=250,
        description="Nombre del estado",
        example="Jalisco Actualizado"
    )
    
    id_estatus: Optional[int] = Field(
        None,
        gt=0,
        description="Estatus del estado",
        example=1
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "id_pais": 1,
                "nombre": "Jalisco Actualizado",
                "id_estatus": 1
            }
        }


class EstadoResponse(BaseModel):
    """
    Schema para respuesta de estado
    """
    id_estado: int = Field(
        ...,
        description="ID único del estado",
        example=1
    )
    
    id_pais: int = Field(
        ...,
        description="ID del país",
        example=1
    )
    
    nombre: str = Field(
        ...,
        description="Nombre del estado",
        example="Jalisco"
    )
    
    id_estatus: int = Field(
        ...,
        description="Estatus del estado",
        example=1
    )
    
    # Información del país (opcional)
    pais: Optional[PaisResponse] = Field(
        None,
        description="Información del país al que pertenece"
    )
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id_estado": 1,
                "id_pais": 1,
                "nombre": "Jalisco",
                "id_estatus": 1,
                "pais": {
                    "id_pais": 1,
                    "nombre": "México",
                    "id_estatus": 1
                }
            }
        }
