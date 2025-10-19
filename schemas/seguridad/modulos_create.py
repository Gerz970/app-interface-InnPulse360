from pydantic import BaseModel, Field
from typing import Optional
from .modulos_base import ModulosBase


class ModulosCreate(ModulosBase):
    """
    Schema para crear un nuevo módulo
    Hereda todos los campos de ModulosBase
    """
    
    class Config:
        json_schema_extra = {
            "example": {
                "nombre": "Dashboard",
                "descripcion": "Panel principal del sistema",
                "icono": "fas fa-dashboard",
                "ruta": "/dashboard",
                "id_estatus": 1
            }
        }
