from pydantic import BaseModel, Field
from typing import Optional


class UsuarioUpdate(BaseModel):
    """
    Schema para actualizar un usuario existente
    Todos los campos son opcionales para permitir actualizaciones parciales
    """
    login: Optional[str] = Field(
        None,
        min_length=1, 
        max_length=25,
        description="Login del usuario",
        example="juan.perez.actualizado"
    )
    
    correo_electronico: Optional[str] = Field(
        None,
        min_length=1, 
        max_length=50,
        description="Correo electrónico del usuario",
        example="juan.perez.nuevo@gmail.com"
    )
    
    password: Optional[str] = Field(
        None,
        min_length=6,
        max_length=50,
        description="Nueva contraseña del usuario (mínimo 6 caracteres)",
        example="nueva123456"
    )
    
    estatus_id: Optional[int] = Field(
        None,
        gt=0,
        description="Estatus del usuario",
        example=1
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "login": "juan.perez.actualizado",
                "correo_electronico": "juan.perez.nuevo@gmail.com",
                "password": "nueva123456",
                "estatus_id": 1
            }
        }
