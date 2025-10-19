from pydantic import BaseModel, Field
from typing import Optional


class RolesUpdate(BaseModel):
    """
    Schema para actualizar un rol existente
    Todos los campos son opcionales para permitir actualizaciones parciales
    """
    rol: Optional[str] = Field(
        None,
        min_length=1, 
        max_length=50,
        description="Nombre del rol",
        example="Administrador_Actualizado"
    )
    
    descripcion: Optional[str] = Field(
        None,
        min_length=1, 
        max_length=250,
        description="Descripción del rol",
        example="Rol con permisos completos del sistema - Actualizado"
    )
    
    estatus_id: Optional[int] = Field(
        None,
        gt=0,
        description="Estatus del rol",
        example=1
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "rol": "Administrador_Actualizado",
                "descripcion": "Rol con permisos completos del sistema - Actualizado",
                "estatus_id": 1
            }
        }
