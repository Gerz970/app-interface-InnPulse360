from pydantic import BaseModel, Field
from typing import List


class ModuloRolAsignacion(BaseModel):
    """
    Schema para asignar módulos a un rol
    """
    modulo_id: int = Field(
        ...,
        gt=0,
        description="ID del módulo a asignar",
        example=1
    )
    
    rol_id: int = Field(
        ...,
        gt=0,
        description="ID del rol al que se asigna el módulo",
        example=1
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "modulo_id": 1,
                "rol_id": 1
            }
        }


class ModuloRolAsignacionMultiple(BaseModel):
    """
    Schema para asignar múltiples módulos a un rol
    """
    rol_id: int = Field(
        ...,
        gt=0,
        description="ID del rol al que se asignan los módulos",
        example=1
    )
    
    modulos_ids: List[int] = Field(
        ...,
        min_items=1,
        description="Lista de IDs de módulos a asignar",
        example=[1, 2, 3]
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "rol_id": 1,
                "modulos_ids": [1, 2, 3]
            }
        }


class ModuloRolResponse(BaseModel):
    """
    Schema para respuesta de asignación módulo-rol
    """
    modulo_id: int = Field(
        ...,
        description="ID del módulo",
        example=1
    )
    
    rol_id: int = Field(
        ...,
        description="ID del rol",
        example=1
    )
    
    modulo_nombre: str = Field(
        ...,
        description="Nombre del módulo",
        example="Dashboard"
    )
    
    rol_nombre: str = Field(
        ...,
        description="Nombre del rol",
        example="Administrador"
    )
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "modulo_id": 1,
                "rol_id": 1,
                "modulo_nombre": "Dashboard",
                "rol_nombre": "Administrador"
            }
        }
