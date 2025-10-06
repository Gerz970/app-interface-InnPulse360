# Configuración de la aplicación
from dotenv import load_dotenv
import os

# Cargar archivo .env según disponibilidad
if os.path.exists(".development.env"):
    # Cargar archivo .env de desarrollo
    load_dotenv(".development.env")
else:
    # Cargar archivo .env de producción
    load_dotenv(".production.env")


class Settings:
    port: int = int(os.getenv("PORT", "8000"))
    host: str = os.getenv("HOST", "127.0.0.1")
    api_version: str = os.getenv("API_VERSION", "/api/v1")

class DatabaseSettings:
    server: str = os.getenv("SERVER", "localhost")
    database: str = os.getenv("DATABASE", "InnPulse360")
    username: str = os.getenv("USER_DB", "sa")
    password: str = os.getenv("PASSWORD", "password")
    port: int = int(os.getenv("PORT_DB", "1433"))
    driver: str = os.getenv("DRIVER", "ODBC Driver 17 for SQL Server")
    trust_server_certificate: bool = os.getenv("TRUST_SERVER_CERTIFICATE", "true") == "true"

class AuthSettings:
    secret_key: str = os.getenv("SECRET_KEY", "tu_clave_secreta_muy_segura_aqui_cambiar_en_produccion")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

class EmailSettings:
    """
    Configuración para el servicio de email
    """
    # Configuración SMTP
    smtp_server: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port: int = int(os.getenv("SMTP_PORT", "587"))
    smtp_username: str = os.getenv("SMTP_USERNAME", "")
    smtp_password: str = os.getenv("SMTP_PASSWORD", "")
    use_tls: bool = os.getenv("SMTP_USE_TLS", "true").lower() == "true"
    use_ssl: bool = os.getenv("SMTP_USE_SSL", "false").lower() == "true"
    
    # Configuración del remitente
    from_email: str = os.getenv("FROM_EMAIL", "noreply@innpulse360.com")
    from_name: str = os.getenv("FROM_NAME", "InnPulse360")
    
    # Configuración de desarrollo
    debug_mode: bool = os.getenv("EMAIL_DEBUG", "false").lower() == "true"
    test_mode: bool = os.getenv("EMAIL_TEST_MODE", "false").lower() == "true"