from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re


class ClienteUpdate(BaseModel):
    """
    Schema para actualizar un cliente existente
    Todos los campos son opcionales para permitir actualizaciones parciales
    """
    tipo_persona: Optional[int] = Field(
        None,
        ge=1,
        le=2,
        description="Tipo de persona: 1=Física, 2=Moral",
        example=1
    )
    
    documento_identificacion: Optional[int] = Field(
        None,
        gt=0,
        description="Número de documento de identificación",
        example=123456789
    )
    
    nombre_razon_social: Optional[str] = Field(
        None,
        min_length=1,
        max_length=250,
        description="Nombre completo o Razón Social",
        example="Juan Pérez González"
    )
    
    apellido_paterno: Optional[str] = Field(
        None,
        max_length=250,
        description="Apellido paterno",
        example="Pérez"
    )
    
    apellido_materno: Optional[str] = Field(
        None,
        max_length=250,
        description="Apellido materno",
        example="González"
    )
    
    rfc: Optional[str] = Field(
        None,
        min_length=12,
        max_length=13,
        description="RFC (12 o 13 caracteres)",
        example="PEGJ800101XXX"
    )
    
    curp: Optional[str] = Field(
        None,
        min_length=18,
        max_length=18,
        description="CURP (18 caracteres)",
        example="PEGJ800101HDFRRN01"
    )
    
    telefono: Optional[str] = Field(
        None,
        min_length=10,
        max_length=10,
        description="Teléfono (10 dígitos)",
        example="5512345678"
    )
    
    direccion: Optional[str] = Field(
        None,
        max_length=100,
        description="Dirección del cliente",
        example="Calle Principal 123, Col. Centro"
    )
    
    pais_id: Optional[int] = Field(
        None,
        gt=0,
        description="ID del país",
        example=1
    )
    
    estado_id: Optional[int] = Field(
        None,
        gt=0,
        description="ID del estado",
        example=1
    )
    
    correo_electronico: Optional[str] = Field(
        None,
        min_length=1,
        max_length=20,
        description="Correo electrónico del cliente",
        example="cliente@email.com"
    )
    
    representante: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="Nombre del representante",
        example="Juan Pérez"
    )
    
    id_estatus: Optional[int] = Field(
        None,
        gt=0,
        description="Estatus del cliente",
        example=1
    )
    
    @field_validator('rfc')
    @classmethod
    def validate_rfc(cls, v: Optional[str]) -> Optional[str]:
        """Valida el formato del RFC"""
        if v is not None:
            v = v.upper().strip()
            if not re.match(r'^[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3}$', v):
                raise ValueError('Formato de RFC inválido')
        return v
    
    @field_validator('curp')
    @classmethod
    def validate_curp(cls, v: Optional[str]) -> Optional[str]:
        """Valida el formato del CURP"""
        if v is not None:
            v = v.upper().strip()
            if not re.match(r'^[A-Z]{4}\d{6}[HM][A-Z]{5}[A-Z0-9]\d$', v):
                raise ValueError('Formato de CURP inválido')
        return v
    
    @field_validator('telefono')
    @classmethod
    def validate_telefono(cls, v: Optional[str]) -> Optional[str]:
        """Valida que el teléfono contenga solo dígitos"""
        if v is not None:
            if not v.isdigit():
                raise ValueError('El teléfono debe contener solo dígitos')
        return v
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "nombre_razon_social": "Juan Pérez González Actualizado",
                "telefono": "5598765432",
                "direccion": "Nueva Dirección 456",
                "id_estatus": 1
            }
        }
