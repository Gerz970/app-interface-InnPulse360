from pydantic import BaseModel, Field
from typing import Optional


class ClienteResponse(BaseModel):
    """
    Schema para respuesta de cliente
    Incluye todos los campos del cliente
    """
    id_cliente: int = Field(
        ...,
        description="ID único del cliente",
        example=1
    )
    
    tipo_persona: int = Field(
        ...,
        description="Tipo de persona: 1=Física, 2=Moral",
        example=1
    )
    
    documento_identificacion: Optional[str] = Field(
        None,
        max_length=50,
        description="Número de documento de identificación",
        example="123456789"
    )
    
    nombre_razon_social: str = Field(
        ...,
        description="Nombre completo o Razón Social",
        example="Juan Pérez González"
    )
    
    apellido_paterno: Optional[str] = Field(
        None,
        description="Apellido paterno",
        example="Pérez"
    )
    
    apellido_materno: Optional[str] = Field(
        None,
        description="Apellido materno",
        example="González"
    )
    
    rfc: Optional[str] = Field(
        None,
        description="RFC del cliente",
        example="PEGJ800101XXX"
    )
    
    curp: Optional[str] = Field(
        None,
        description="CURP del cliente",
        example="PEGJ800101HDFRRN01"
    )
    
    telefono: Optional[str] = Field(
        None,
        description="Teléfono del cliente",
        example="5512345678"
    )
    
    direccion: Optional[str] = Field(
        None,
        description="Dirección del cliente",
        example="Calle Principal 123, Col. Centro"
    )
    
    pais_id: int = Field(
        ...,
        description="ID del país",
        example=1
    )
    
    estado_id: Optional[int] = Field(
        None,
        description="ID del estado (opcional)",
        example=15
    )
    
    correo_electronico: str = Field(
        ...,
        description="Correo electrónico del cliente",
        example="cliente@email.com"
    )
    
    representante: str = Field(
        ...,
        description="Nombre del representante",
        example="Juan Pérez"
    )
    
    id_estatus: int = Field(
        ...,
        description="Estatus del cliente (1=Activo, 0=Inactivo)",
        example=1
    )
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id_cliente": 1,
                "tipo_persona": 1,
                "documento_identificacion": "123456789",
                "nombre_razon_social": "Juan Pérez González",
                "apellido_paterno": "Pérez",
                "apellido_materno": "González",
                "rfc": "PEGJ800101XXX",
                "curp": "PEGJ800101HDFRRN01",
                "telefono": "5512345678",
                "direccion": "Calle Principal 123, Col. Centro",
                "pais_id": 1,
                "estado_id": 15,
                "correo_electronico": "cliente@email.com",
                "representante": "Juan Pérez",
                "id_estatus": 1
            }
        }
