from pydantic import BaseModel, Field
from typing import Optional


class ClienteFormularioData(BaseModel):
    """
    Schema para datos del formulario de cliente
    Incluye todos los campos necesarios para crear/actualizar un cliente
    """
    tipo_persona: int = Field(..., description="Tipo de persona (1=Física, 2=Moral)")
    documento_identificacion: int = Field(..., description="Número de documento de identificación")
    nombre_razon_social: str = Field(..., description="Nombre o razón social")
    apellido_paterno: Optional[str] = Field(None, description="Apellido paterno")
    apellido_materno: Optional[str] = Field(None, description="Apellido materno")
    rfc: Optional[str] = Field(None, description="RFC")
    curp: Optional[str] = Field(None, description="CURP")
    telefono: Optional[str] = Field(None, description="Teléfono")
    direccion: Optional[str] = Field(None, description="Dirección")
    pais_id: int = Field(..., description="ID del país")
    estado_id: int = Field(..., description="ID del estado")
    correo_electronico: str = Field(..., description="Correo electrónico")
    representante: str = Field(..., description="Representante")
    id_estatus: int = Field(default=1, description="Estatus del cliente")
    
    class Config:
        from_attributes = True
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
