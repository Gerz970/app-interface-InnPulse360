from pydantic import BaseModel, Field
from typing import Optional

class PuestoCreate(BaseModel):
    puesto: str = Field(
        min_length=1,
        max_length=250,
        description="Nombre del puesto a registrar",
        example="Recepcionista"
    )

    descripcion: str = Field(
        min_length=1,
        max_length=250,
        description="Descripción del puesto a registrar",
        example="Responsable de agendar reservaciones, recibir a clientes, etc."
    )

    estatus_id: Optional[int] = Field(
        1,  # Valor por defecto activo
        gt=0,
        description="Estatus del puesto (1=Activo por defecto)",
        example=1
    )

    class Config:
        json_schema_extra = {
            "example": {
                "puesto": "Recepcionista",
                "descripcion": "Responsable de agendar reservaciones, recibir a clientes, etc.",
                "estatus_id": 1
            }
        }

class PuestoUpdate(BaseModel):
    puesto: Optional[str] = Field(
        None,
        min_length=1,
        max_length=250,
        description="Nombre del puesto a registrar",
        example="Recepcionista"
    )

    descripcion: Optional[str] = Field(
        None,
        min_length=1,
        max_length=250,
        description="Descripción del puesto a registrar",
        example="Responsable de agendar reservaciones, recibir a clientes, etc."
    )

    estatus_id: Optional[int] = Field(
        None,
        gt=0,
        description="Estatus del puesto (1=Activo por defecto)",
        example=1
    )

    class Config:
        json_schema_extra = {
            "example": {
                "puesto": "Recepcionista",
                "descripcion": "Responsable de agendar reservaciones, recibir a clientes, etc.",
                "estatus_id": 1
            }
        }


class PuestoResponse(BaseModel):
    id_puesto: int = Field(
        ...,
        description="ID único del puesto",
        example=1
    )

    puesto: Optional[str] = Field(
        None,
        min_length=1,
        max_length=250,
        description="Nombre del puesto a registrar",
        example="Recepcionista"
    )

    descripcion: Optional[str] = Field(
        None,
        min_length=1,
        max_length=250,
        description="Descripción del puesto a registrar",
        example="Responsable de agendar reservaciones, recibir a clientes, etc."
    )

    estatus_id: Optional[int] = Field(
        ...,
        ge=0,
        description="Estatus del puesto (1=Activo por defecto)",
        example=1
    )

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "puesto": "Recepcionista",
                "descripcion": "Responsable de agendar reservaciones, recibir a clientes, etc.",
                "estatus_id": 1
            }
        }