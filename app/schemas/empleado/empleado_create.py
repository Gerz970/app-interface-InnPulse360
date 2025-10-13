from .empleado_base import EmpleadoBase

class EmpleadoCreate(EmpleadoBase):
    """
    Schema para crear un nuevo empleado
    Hereda todos los campos de EmpleadoBase
    No incluye el ID porque se genera automáticamente
    """

    class Config: 
        json_schema_extra = {
            "example" : {
                "clave_empleado": "001",
                "nombre": "Maria",
                "apellido_paterno": "Pérez",
                "apellido_materno": "López",
                "fecha_nacimiento": "1990-05-15",
                "rfc": "MOGF780404S36",
                "curp": "MABG851202HZTWMG9",
                "domicilio": {
                    "domicilio_completo": "Calle Los Olivos #123, Col. Centro, CDMX",
                    "codigo_postal": "06000"
                }
            }
        }