# Configuración de la aplicación
from dotenv import load_dotenv
import os
from pathlib import Path


# Cargar archivo .development.env desde la carpeta app/
load_dotenv()

class Settings:
    port: int = int(os.getenv("PORT", "8000"))
    host: str = os.getenv("HOST", "127.0.0.1")
    api_version: str = os.getenv("API_VERSION", "/api/v1")

class DatabaseSettings:
    server: str = os.getenv("SERVER", "localhost")
    database: str = os.getenv("DATABASE", "DBInnpulse360")
    username: str = os.getenv("USER_DB", "root")
    password: str = os.getenv("PASSWORD", "123456")
    port: int = int(os.getenv("PORT_DB", "3306"))
    driver: str = os.getenv("DRIVER", "ODBC Driver 17 for SQL Server")
    trust_server_certificate: bool = os.getenv("TRUST_SERVER_CERTIFICATE", "true") == "true"

class AuthSettings:
    secret_key: str = os.getenv("SECRET_KEY", "tu_clave_secreta_muy_segura_aqui_cambiar_en_produccion")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

class EmailSettings:
    """
    Configuración para el servicio de email usando SMTP
    """
    # Configuración SMTP
    smtp_server: str = os.getenv("SmtpServer", "smtp.gmail.com")
    smtp_port: int = int(os.getenv("SmtpPort", "587"))
    smtp_username: str = os.getenv("FromEmail", "")
    smtp_password: str = os.getenv("FromPassword", "")
    use_tls: bool = os.getenv("EnableSsl", "true").lower() == "true"
    
    # Configuración del remitente
    from_email: str = os.getenv("FromEmail", "noreply@innpulse360.com")
    from_name: str = os.getenv("FROM_NAME", "InnPulse360")

class SupabaseSettings:
    """
    Configuración para el servicio de Supabase Storage
    """
    url: str = os.getenv("SUPABASE_URL", "")
    anon_key: str = os.getenv("SUPABASE_ANON_KEY", "")
    service_key: str = os.getenv("SUPABASE_SERVICE_KEY", "")
    
    @property
    def default_service_key(self) -> str:
        """Retorna la service key si está disponible, sino la anon key"""
        return self.service_key if self.service_key else self.anon_key
    
    bucket_images: str = os.getenv("SUPABASE_BUCKET_IMAGES", "images")
    bucket_pdfs: str = os.getenv("SUPABASE_BUCKET_PDFS", "pdfs")
    public_base_url: str = os.getenv("SUPABASE_PUBLIC_BASE_URL", "")

class FCMSettings:
    """
    Configuración para Firebase Cloud Messaging (FCM)
    Usa variables de entorno separadas para mayor seguridad
    """
    # Variables de entorno para Service Account (desde .env)
    project_id: str = os.getenv("FCM_PROJECT_ID", "")
    private_key_id: str = os.getenv("FCM_PRIVATE_KEY_ID", "")
    private_key: str = os.getenv("FCM_PRIVATE_KEY", "").replace("\\n", "\n")  # Reemplazar \\n por saltos de línea reales
    client_email: str = os.getenv("FCM_CLIENT_EMAIL", "")
    client_id: str = os.getenv("FCM_CLIENT_ID", "")
    auth_uri: str = os.getenv("FCM_AUTH_URI", "https://accounts.google.com/o/oauth2/auth")
    token_uri: str = os.getenv("FCM_TOKEN_URI", "https://oauth2.googleapis.com/token")
    auth_provider_x509_cert_url: str = os.getenv("FCM_AUTH_PROVIDER_X509_CERT_URL", "https://www.googleapis.com/oauth2/v1/certs")
    client_x509_cert_url: str = os.getenv("FCM_CLIENT_X509_CERT_URL", "")
    
    # Fallback: Ruta al archivo Service Account JSON (solo para desarrollo local)
    service_account_path: str = os.getenv(
        "FCM_SERVICE_ACCOUNT_PATH", 
        str(Path(__file__).parent / "firebase_service_account.json")
    )
    
    # URL de la API HTTP v1 de FCM
    fcm_url: str = "https://fcm.googleapis.com/v1/projects/{project_id}/messages:send"
    
    @property
    def has_env_variables(self) -> bool:
        """Verifica si todas las variables de entorno necesarias están configuradas"""
        return all([
            self.project_id,
            self.private_key_id,
            self.private_key,
            self.client_email,
            self.client_id
        ])
    
    @property
    def service_account_file_exists(self) -> bool:
        """Verifica si existe el archivo Service Account (fallback)"""
        return Path(self.service_account_path).exists()
    
    def get_service_account_dict(self) -> dict:
        """
        Construye el diccionario de Service Account desde variables de entorno
        
        Returns:
            dict: Diccionario con la estructura del Service Account JSON
        """
        return {
            "type": "service_account",
            "project_id": self.project_id,
            "private_key_id": self.private_key_id,
            "private_key": self.private_key,
            "client_email": self.client_email,
            "client_id": self.client_id,
            "auth_uri": self.auth_uri,
            "token_uri": self.token_uri,
            "auth_provider_x509_cert_url": self.auth_provider_x509_cert_url,
            "client_x509_cert_url": self.client_x509_cert_url
        }


# Configuración de módulos permitidos por rol (movido al frontend)
# Esta configuración ya no se usa en el backend, el filtrado se hace en la app móvil
# Se mantiene comentada por si se necesita en el futuro
# ROL_MODULOS_PERMITIDOS = {
#     "Cliente": ["Reservaciones"]
# }