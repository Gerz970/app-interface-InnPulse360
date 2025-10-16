from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class EmpleadoUpdate(BaseModel):
    clave_empleado: Optional[str] = Field(
        None,
        min_length=1,
        max_length=25,
        description="Clave del empleado",
        example="0001"
    )

    nombre: Optional[str] = Field(
        None,
        min_length=1,
        max_length=150,
        description="Nombre del empleado",
        example="Juan"
    )

    apellido_paterno: Optional[str] = Field(
        None,
        min_length=1,
        max_length=50,
        description="Apellido paterno del empleado",
        example="Pérez"
    )

    apellido_materno: Optional[str] = Field(
        None,
        min_length=1,
        max_length=50,
        description="Apellido materno del empleado",
        example="López"
    )

    fecha_nacimiento: Optional[date] = Field(
        None,
        description="Fecha de nacimiento del empleado",
        example="1990-05-15"
    )

    rfc: Optional[str] = Field(
        None,
        min_length=12,
        max_length=13,
        description="RFC del empleado",
        example="MOGF780404S36"
    )

    curp: Optional[str] = Field(
        None,
        min_length=18,
        max_length=18,
        description="CURP del empleado",
        example="MABG851202HZTWMG9"
    )

    class Config: 
        json_schema_extra = {
            "example" : {
                "clave_empleado": "001",
                "nombre": "Maria",
                "rfc": "MOGF780404S36",
                "curp": "MABG851202HZTWMG9"
            }
        }


