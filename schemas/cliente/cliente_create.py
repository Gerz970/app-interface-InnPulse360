from pydantic import BaseModel, Field
from .cliente_base import ClienteBase


class ClienteCreate(ClienteBase):
    """
    Schema para crear un nuevo cliente
    Hereda todos los campos de ClienteBase
    """
    
    class Config:
        json_schema_extra = {
            "example": {
                "tipo_persona": 1,
                "documento_identificacion": 123456789,
                "nombre_razon_social": "Juan Pérez González",
                "apellido_paterno": "Pérez",
                "apellido_materno": "González",
                "rfc": "PEGJ800101XXX",
                "curp": "PEGJ800101HDFRRN01",
                "telefono": "5512345678",
                "direccion": "Calle Principal 123, Col. Centro",
                "pais_id": 1,
                "estado_id": 15,
                "correo_electronico": "juan.perez@email.com",
                "representante": "Juan Pérez",
                "id_estatus": 1
            }
        }
