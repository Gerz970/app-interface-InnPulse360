from pydantic import BaseModel, Field
from typing import Optional


class ModulosBase(BaseModel):
    """
    Schema base para módulos
    Contiene los campos comunes para crear y actualizar
    """
    nombre: str = Field(
        ...,
        min_length=1,
        max_length=25,
        description="Nombre del módulo",
        example="Dashboard"
    )
    
    descripcion: Optional[str] = Field(
        None,
        max_length=100,
        description="Descripción del módulo",
        example="Panel principal del sistema"
    )
    
    icono: Optional[str] = Field(
        None,
        max_length=25,
        description="Icono del módulo (clase CSS o nombre)",
        example="fas fa-dashboard"
    )
    
    ruta: Optional[str] = Field(
        None,
        max_length=250,
        description="Ruta del módulo en la aplicación",
        example="/dashboard"
    )
    
    id_estatus: int = Field(
        ...,
        gt=0,
        description="Estatus del módulo (1=Activo, 0=Inactivo)",
        example=1
    )
    
    movil: Optional[int] = Field(
        0,
        description="Indica si el módulo pertenece a móvil (1=móvil, 0=web). Por defecto es 0 (web)",
        example=0
    )
    
    class Config:
        from_attributes = True
