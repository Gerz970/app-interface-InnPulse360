from .empleado_base import EmpleadoBase
from pydantic import Field

class EmpleadoCreate(EmpleadoBase):
    """
    Schema para crear un nuevo empleado
    Hereda todos los campos de EmpleadoBase
    No incluye el ID porque se genera automáticamente
    """

    puesto_id: int=Field(
        ...,
        description= "ID del puesto del empleado",
        example= 1
    )

    hotel_id: int=Field(
        ...,
        description= "ID del hotel al que pertenece el empleado",
        example= 1
    )

    class Config: 
        json_schema_extra = {
            "example" : {
                "clave_empleado": "001",
                "nombre": "Maria",
                "apellido_paterno": "Pérez",
                "apellido_materno": "López",
                "fecha_nacimiento": "1990-05-15",
                "rfc": "MOGF780404S36",
                "curp": "MABG851202HZTWMG91",
                "domicilio": {
                    "domicilio_completo": "Calle Los Olivos #123, Col. Centro, CDMX",
                    "codigo_postal": "06000"
                },
                "puesto_id" : 1,
                "hotel_id": 1
            }
        }