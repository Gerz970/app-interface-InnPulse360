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
    database: str = os.getenv("DATABASE", "innpulse360")
    username: str = os.getenv("USERNAME", "sa")
    password: str = os.getenv("PASSWORD", "123456")
    port: int = int(os.getenv("PORT_DB", "1433"))
    trust_server_certificate: bool = os.getenv("TRUST_SERVER_CERTIFICATE", "true") == "true"
    driver: str = os.getenv("DRIVER", "ODBC Driver 17 for SQL Server")
    trust_server_certificate: bool = os.getenv("TRUST_SERVER_CERTIFICATE", "true") == "true"
