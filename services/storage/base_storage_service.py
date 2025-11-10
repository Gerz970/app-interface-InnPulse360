"""
Servicio base para operaciones con Supabase Storage
Proporciona funcionalidad común para subir, eliminar y obtener URLs de archivos
"""

import logging
from typing import Optional
from supabase import Client
from core.supabase_client import get_supabase_client
from core.config import SupabaseSettings

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SupabaseStorageService:
    """
    Servicio base para operaciones con Supabase Storage
    """
    
    def __init__(self, bucket: str, client: Optional[Client] = None):
        """
        Inicializa el servicio de almacenamiento
        
        Args:
            bucket (str): Nombre del bucket de Supabase
            client (Optional[Client]): Cliente de Supabase (opcional, se crea uno si no se proporciona)
        """
        self._client = client or get_supabase_client()
        self._bucket = bucket
        settings = SupabaseSettings()
        self._public_base_url = settings.public_base_url
        
        logger.info(f"SupabaseStorageService inicializado - Bucket: {self._bucket}")
    
    def upload(
        self,
        file_path: str,
        file_bytes: bytes,
        content_type: Optional[str] = None,
        upsert: bool = False
    ) -> dict:
        """
        Sube un archivo a Supabase Storage
        
        Args:
            file_path (str): Ruta donde se guardará el archivo en el bucket
            file_bytes (bytes): Contenido del archivo en bytes
            content_type (str): Tipo MIME del archivo
            upsert (bool): Si es True, sobrescribe el archivo si ya existe
            
        Returns:
            dict: Resultado de la operación con formato:
                {
                    "success": bool,
                    "path": str,
                    "bucket": str,
                    "public_url": Optional[str],
                    "response": dict,
                    "message": Optional[str]
                }
        """
        try:
            file_options = {
                "upsert": str(upsert).lower()
            }

            if content_type:
                file_options["contentType"] = content_type

            response = (
                self._client.storage
                .from_(self._bucket)
                .upload(
                    path=file_path,
                    file=file_bytes,
                    file_options=file_options
                )
            )
            
            public_url = self.build_public_url(file_path)
            
            logger.info(
                f"Archivo subido exitosamente - Bucket: {self._bucket}, Path: {file_path}"
            )
            
            return {
                "success": True,
                "path": file_path,
                "bucket": self._bucket,
                "public_url": public_url,
                "response": response
            }
            
        except Exception as exc:
            error_msg = f"Error al subir archivo: {str(exc)}"
            logger.error(
                error_msg,
                exc_info=exc,
                extra={"bucket": self._bucket, "path": file_path}
            )
            return {
                "success": False,
                "path": file_path,
                "bucket": self._bucket,
                "message": error_msg
            }
    
    def delete(self, file_path: str) -> dict:
        """
        Elimina un archivo de Supabase Storage
        
        Args:
            file_path (str): Ruta del archivo a eliminar
            
        Returns:
            dict: Resultado de la operación con formato:
                {
                    "success": bool,
                    "path": str,
                    "bucket": str,
                    "message": Optional[str]
                }
        """
        try:
            self._client.storage.from_(self._bucket).remove([file_path])
            
            logger.info(
                f"Archivo eliminado exitosamente - Bucket: {self._bucket}, Path: {file_path}"
            )
            
            return {
                "success": True,
                "path": file_path,
                "bucket": self._bucket
            }
            
        except Exception as exc:
            error_msg = f"Error al eliminar archivo: {str(exc)}"
            logger.error(
                error_msg,
                exc_info=exc,
                extra={"bucket": self._bucket, "path": file_path}
            )
            return {
                "success": False,
                "path": file_path,
                "bucket": self._bucket,
                "message": error_msg
            }
    
    def create_signed_url(self, file_path: str, expires_in: int = 3600) -> dict:
        """
        Crea una URL firmada temporal para acceder a un archivo
        
        Args:
            file_path (str): Ruta del archivo
            expires_in (int): Tiempo de expiración en segundos (por defecto 3600 = 1 hora)
            
        Returns:
            dict: Resultado de la operación con formato:
                {
                    "success": bool,
                    "signed_url": Optional[str],
                    "message": Optional[str]
                }
        """
        try:
            response = (
                self._client.storage
                .from_(self._bucket)
                .create_signed_url(path=file_path, expires_in=expires_in)
            )
            
            signed_url = response.get("signedURL")
            
            logger.info(
                f"URL firmada creada - Bucket: {self._bucket}, Path: {file_path}, Expires: {expires_in}s"
            )
            
            return {
                "success": True,
                "signed_url": signed_url
            }
            
        except Exception as exc:
            error_msg = f"Error al generar URL firmada: {str(exc)}"
            logger.error(
                error_msg,
                exc_info=exc,
                extra={"bucket": self._bucket, "path": file_path}
            )
            return {
                "success": False,
                "signed_url": None,
                "message": error_msg
            }
    
    def build_public_url(self, file_path: str) -> Optional[str]:
        """
        Construye la URL pública de un archivo
        
        Args:
            file_path (str): Ruta del archivo
            
        Returns:
            Optional[str]: URL pública del archivo o None si no está configurada
        """
        if not self._public_base_url:
            return None
        
        # Limpiar la URL base si termina con /
        base_url = self._public_base_url.rstrip('/')
        
        return f"{base_url}/storage/v1/object/public/{self._bucket}/{file_path}"

