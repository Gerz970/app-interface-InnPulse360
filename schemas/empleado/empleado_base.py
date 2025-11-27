from pydantic import BaseModel, Field, EmailStr, field_validator
from datetime import date
from .domicilio_base import DomicilioBase

class EmpleadoBase(BaseModel):
    """
    Schema base para Empleado con campos comunes
    Contiene todos los campos que son comunes entre Create, Update y Response
    """
    clave_empleado: str = Field(
        min_length=1,
        max_length=25,
        description="Clave del empleado",
        example="0001"
    )

    nombre: str = Field(
        min_length=1,
        max_length=150,
        description="Nombre del empleado",
        example="Juan"
    )

    apellido_paterno: str = Field(
        min_length=1,
        max_length=50,
        description="Apellido paterno del empleado",
        example="Pérez"
    )

    apellido_materno: str = Field(
        min_length=1,
        max_length=50,
        description="Apellido materno del empleado",
        example="López"
    )

    fecha_nacimiento: date = Field(
        description="Fecha de nacimiento del empleado",
        example="1990-05-15"
    )

    rfc: str = Field(
        min_length=12,
        max_length=13,
        description="RFC del empleado",
        example="MOGF780404S36"
    )

    curp: str = Field(
        min_length=18,
        max_length=18,
        description="CURP del empleado",
        example="MABG851202HZTWMG91"
    )

    domicilio: DomicilioBase



