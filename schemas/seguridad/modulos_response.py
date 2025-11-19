from pydantic import BaseModel, Field
from typing import Optional, List
from .roles_base import RolesBase


class ModulosResponse(BaseModel):
    """
    Schema para respuesta de módulo
    Incluye todos los campos del módulo
    """
    id_modulo: int = Field(
        ...,
        description="ID único del módulo",
        example=1
    )
    
    nombre: str = Field(
        ...,
        description="Nombre del módulo",
        example="Dashboard"
    )
    
    descripcion: Optional[str] = Field(
        None,
        description="Descripción del módulo",
        example="Panel principal del sistema"
    )
    
    icono: Optional[str] = Field(
        None,
        description="Icono del módulo",
        example="fas fa-dashboard"
    )
    
    ruta: Optional[str] = Field(
        None,
        description="Ruta del módulo",
        example="/dashboard"
    )
    
    id_estatus: int = Field(
        ...,
        description="Estatus del módulo (1=Activo, 0=Inactivo)",
        example=1
    )
    
    movil: Optional[int] = Field(
        None,
        description="Indica si el módulo pertenece a móvil (1=móvil, 0=web)",
        example=0
    )
    
    roles: List[RolesBase] = Field(
        default_factory=list,
        description="Lista de roles que tienen acceso a este módulo"
    )
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id_modulo": 1,
                "nombre": "Dashboard",
                "descripcion": "Panel principal del sistema",
                "icono": "fas fa-dashboard",
                "ruta": "/dashboard",
                "id_estatus": 1,
                "roles": [
                    {"id_rol": 1, "rol": "Administrador", "descripcion": "Rol de administrador"},
                    {"id_rol": 2, "rol": "Usuario", "descripcion": "Rol de usuario"}
                ]
            }
        }
