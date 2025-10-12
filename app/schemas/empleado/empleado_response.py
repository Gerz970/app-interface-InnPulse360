from pydantic import BaseModel, Field
from .empleado_base import EmpleadoBase

class EmpleadoResponse(EmpleadoBase):
    id_empleado: int=Field(
        ..., 
        description="ID único del empleado",
        example=1
    )

    class Config: 
        from_attributes = True
        json_schema_extra = {
            "example" : {
                "id_empleado": 1,
                "clave_empleado": "001",
                "nombre": "Maria",
                "apellido_paterno": "Pérez",
                "apellido_materno": "López",
                "fecha_nacimiento": "1990-05-15",
                "rfc": "MOGF780404S36",
                "curp": "MABG851202HZTWMG9"
            }
        }