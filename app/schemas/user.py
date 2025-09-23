"""
Módulo de esquemas Pydantic para Usuario.

Este módulo define modelos Pydantic para validación de requests/responses de API
y serialización para entidades de Usuario.
"""

from pydantic import BaseModel


class UserBase(BaseModel):
    """
    Esquema base de usuario.

    Contiene los campos comunes para operaciones de usuario.
    Usado como clase base para otros esquemas de usuario.

    Atributos:
        name (str): Nombre completo del usuario
        email (str): Dirección de email del usuario
    """
    name: str
    email: str


class UserCreate(UserBase):
    """
    Esquema para crear nuevos usuarios.

    Hereda todos los campos de UserBase. Usado para requests POST
    para crear nuevos registros de usuario.
    """
    pass


class User(UserBase):
    """
    Esquema completo de usuario para responses.

    Incluye el campo ID para representación completa del usuario.
    Usado para responses de API y operaciones que retornan datos de usuario.

    Atributos:
        id (int): Identificador único de usuario
        name (str): Nombre completo del usuario (heredado)
        email (str): Dirección de email del usuario (heredado)
    """
    id: int

    class Config:
        """Configuración de Pydantic para permitir conversión de modelo ORM."""
        from_attributes = True