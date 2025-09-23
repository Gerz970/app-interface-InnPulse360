"""
Módulo del modelo de datos de Usuario.

Este módulo define el modelo User de SQLAlchemy para la base de datos.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core import Base


class User(Base):
    """
    Modelo de base de datos para Usuario.

    Representa una entidad de usuario en la base de datos con información básica.
    Usa el estilo SQLAlchemy 2.0 con tipos Mapped para anotaciones de tipo.

    Atributos:
        id (int): Clave primaria, identificador único de usuario auto-incremental
        name (str): Nombre completo del usuario
        email (str): Dirección de email del usuario, debe ser única
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)