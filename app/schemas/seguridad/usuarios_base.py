from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional


class UsuariosBase(BaseModel):
    """
    Schema base para Usuario con campos comunes
    Contiene todos los campos que son comunes entre Create, Update y Response
    """
    login: str = Field(
        ..., # Los tres puntos significan que el campo es requerido
        min_length=1, 
        max_length=25,
        description="Login del usuario",
        example="juan.perez"
    )
    
    correo_electronico: str = Field(
        ..., # Los tres puntos significan que el campo es requerido
        min_length=1, 
        max_length=50,
        description="Correo electrónico del usuario",
        example="juan.perez@gmail.com"
    )
    
    password: str = Field(
        ..., # Los tres puntos significan que el campo es requerido
        gt=0,
        description="Contraseña del usuario",
        example="123456"
    )
    
    estatus_id: Optional[int] = Field(
        None, # None significa que el campo es opcional
        gt=0,
        description="Estatus del usuario",
        example=1
    )
    