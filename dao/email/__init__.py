"""
DAO para módulo de email
Contiene DAOs para gestión de correos electrónicos
"""

from .dao_email_template import EmailTemplateDAO
from .dao_email_log import EmailLogDAO

__all__ = ["EmailTemplateDAO", "EmailLogDAO"]
