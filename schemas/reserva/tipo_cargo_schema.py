from pydantic import BaseModel, Field
from typing import Optional


class TipoCargoBase(BaseModel):
    """
    Atributos base compartidos por los esquemas de TipoCargo
    """
    nombre_cargo: str = Field(
        ...,
        max_length=25,
        description="Nombre del tipo de cargo"
    )
    descripcion: str = Field(
        ...,
        max_length=100,
        description="Descripción del cargo"
    )
    id_estatus: int = Field(
        ...,
        description="Identificador del estatus del cargo"
    )


class TipoCargoCreate(TipoCargoBase):
    """
    Schema para crear un nuevo registro de TipoCargo
    """
    pass


class TipoCargoUpdate(BaseModel):
    """
    Schema para actualizar parcialmente un registro de TipoCargo
    """
    nombre_cargo: Optional[str] = Field(None, max_length=25)
    descripcion: Optional[str] = Field(None, max_length=100)
    id_estatus: Optional[int] = Field(None)


class TipoCargoResponse(TipoCargoBase):
    """
    Schema de respuesta para devolver un registro completo de TipoCargo
    """
    id_tipo: int = Field(..., description="Identificador único del tipo de cargo")

    class Config:
        from_attributes = True
