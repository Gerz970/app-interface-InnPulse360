from pydantic import BaseModel, Field
from typing import Optional


class ModulosUpdate(BaseModel):
    """
    Schema para actualizar un módulo existente
    Todos los campos son opcionales para permitir actualizaciones parciales
    """
    nombre: Optional[str] = Field(
        None,
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
    
    id_estatus: Optional[int] = Field(
        None,
        gt=0,
        description="Estatus del módulo (1=Activo, 0=Inactivo)",
        example=1
    )
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "nombre": "Dashboard Actualizado",
                "descripcion": "Panel principal actualizado",
                "icono": "fas fa-chart-line",
                "ruta": "/dashboard-v2",
                "id_estatus": 1
            }
        }
