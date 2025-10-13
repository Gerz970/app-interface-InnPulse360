from pydantic import BaseModel, Field
from .empleado_base import EmpleadoBase
from typing import Optional
from .domicilio_base import DomicilioBase

class EmpleadoResponse(EmpleadoBase):
    id_empleado: int=Field(
        ..., 
        description="ID único del empleado",
        example=1
    )
    
    domicilio: Optional[DomicilioBase] = None

    class Config: 
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id_empleado": 1,
                "clave_empleado": "001",
                "nombre": "Maria",
                "apellido_paterno": "Pérez",
                "apellido_materno": "López",
                "fecha_nacimiento": "1990-05-15",
                "rfc": "MOGF780404S36",
                "curp": "MABG851202HZTWMG9",
                "domicilio": {
                    "id_domicilio": 1,
                    "domicilio_completo": "Calle Falsa 123",
                    "codigo_postal": "01234",
                    "estatus_id": 1
                }
            }
        }