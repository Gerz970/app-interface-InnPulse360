"""
Schemas para módulo de email
Contiene schemas Pydantic para validación de datos de email
"""

from .email_basic_schemas import EmailSendBasic, EmailResponseBasic

__all__ = [
    "EmailSendBasic", 
    "EmailResponseBasic"
]
