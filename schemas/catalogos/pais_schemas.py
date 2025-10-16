from pydantic import BaseModel, Field
from typing import Optional, List


class PaisCreate(BaseModel):
    """
    Schema para crear un nuevo país
    """
    nombre: str = Field(
        ...,
        min_length=1,
        max_length=250,
        description="Nombre del país",
        example="México"
    )
    
    id_estatus: Optional[int] = Field(
        1,  # Valor por defecto activo
        gt=0,
        description="Estatus del país (1=Activo por defecto)",
        example=1
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "nombre": "México",
                "id_estatus": 1
            }
        }


class PaisUpdate(BaseModel):
    """
    Schema para actualizar un país existente
    """
    nombre: Optional[str] = Field(
        None,
        min_length=1,
        max_length=250,
        description="Nombre del país",
        example="México Actualizado"
    )
    
    id_estatus: Optional[int] = Field(
        None,
        gt=0,
        description="Estatus del país",
        example=1
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "nombre": "México Actualizado",
                "id_estatus": 1
            }
        }


class PaisResponse(BaseModel):
    """
    Schema para respuesta de país
    """
    id_pais: int = Field(
        ...,
        description="ID único del país",
        example=1
    )
    
    nombre: str = Field(
        ...,
        description="Nombre del país",
        example="México"
    )
    
    id_estatus: int = Field(
        ...,
        description="Estatus del país",
        example=1
    )
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id_pais": 1,
                "nombre": "México",
                "id_estatus": 1
            }
        }
