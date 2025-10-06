"""
Modelos para módulo de email
Contiene modelos SQLAlchemy para gestión de correos electrónicos
"""

from .email_template_model import EmailTemplate
from .email_log_model import EmailLog

__all__ = ["EmailTemplate", "EmailLog"]
