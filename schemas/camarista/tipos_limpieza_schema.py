from pydantic import BaseModel, Field
from typing import Optional

class TiposLimpiezaBase(BaseModel):
    nombre_tipo: str = Field(
        ...,
        min_length=1,
        max_length=25,
        description="Nombre del tipo de limpieza",
        example="Limpieza básica"
    )

    descripcion: str = Field(
        ..., # Los tres puntos significan que el campo es requerido
        min_length=1, 
        max_length=100,
        description="Descripción de la actividad",
        example="Tendido de camas, lavado de baño, etc"
    )

    id_estatus: int = Field(
        ..., 
        description="ID de estatus",
        example=1
    )

class TipoLimpiezaCreate(TiposLimpiezaBase):
    pass

class TipoLimpiezaUpdate(BaseModel):
    nombre_tipo: Optional[str] = Field(
        ...,
        min_length=1,
        max_length=25,
        description="Nombre del tipo de limpieza",
        example="Limpieza básica"
    )

    descripcion: Optional[str] = Field(
        ..., # Los tres puntos significan que el campo es requerido
        min_length=1, 
        max_length=100,
        description="Descripción de la actividad",
        example="Tendido de camas, lavado de baño, etc"
    )

    estatus_id: Optional[int] = Field(
        ..., 
        description="ID de estatus",
        example=1
    )

class TipoLimpiezaResponse(TiposLimpiezaBase):
    id_tipo_limpieza : int
    class Config:
        from_attributes = True