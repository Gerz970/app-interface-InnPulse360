from pydantic import BaseModel, Field
from typing import Optional, List


class UsuarioCreate(BaseModel):
    """
    Schema para crear un nuevo usuario
    Hereda de UsuariosBase pero sin id_usuario
    """
    login: str = Field(
        ...,
        min_length=1, 
        max_length=25,
        description="Login del usuario",
        example="juan.perez"
    )
    
    correo_electronico: str = Field(
        ...,
        min_length=1, 
        max_length=50,
        description="Correo electrónico del usuario",
        example="juan.perez@gmail.com"
    )
    
    password: str = Field(
        ...,
        min_length=6,  # Mínimo 6 caracteres para seguridad
        max_length=255,  # Máximo razonable para contraseñas
        description="Contraseña del usuario (mínimo 6 caracteres, sin límite superior)",
        example="123456"
    )
    
    estatus_id: Optional[int] = Field(
        1,  # Valor por defecto activo
        gt=0,
        description="Estatus del usuario (1=Activo por defecto)",
        example=1
    )
    
    roles_ids: Optional[List[int]] = Field(
        None,
        description="Lista de IDs de roles a asignar al usuario",
        example=[1, 2]
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "login": "juan.perez",
                "correo_electronico": "juan.perez@gmail.com",
                "password": "123456",
                "roles_ids": [1, 2]
            }
        }
