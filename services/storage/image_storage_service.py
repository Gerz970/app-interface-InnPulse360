"""
Servicio especializado para almacenamiento de imágenes en Supabase Storage
Soporta formatos: JPG, PNG, GIF
"""

import mimetypes
from typing import Optional, Sequence
from supabase import Client
from services.storage.base_storage_service import SupabaseStorageService
from core.config import SupabaseSettings

# Tipos MIME permitidos para imágenes
ALLOWED_IMAGE_TYPES: Sequence[str] = ("image/jpeg", "image/png", "image/gif")

# Extensiones permitidas para imágenes
ALLOWED_IMAGE_EXTENSIONS: Sequence[str] = (".jpg", ".jpeg", ".png", ".gif")


class SupabaseImageStorageService(SupabaseStorageService):
    """
    Servicio especializado para almacenamiento de imágenes
    Valida que los archivos sean de tipo imagen (JPG, PNG, GIF)
    """
    
    def __init__(self, client: Optional[Client] = None):
        """
        Inicializa el servicio de almacenamiento de imágenes
        
        Args:
            client (Optional[Client]): Cliente de Supabase (opcional)
        """
        settings = SupabaseSettings()
        super().__init__(bucket=settings.bucket_images, client=client)
    
    def upload_image(
        self,
        file_path: str,
        file_bytes: bytes,
        content_type: Optional[str] = None,
        upsert: bool = False
    ) -> dict:
        """
        Sube una imagen a Supabase Storage
        
        Valida que el archivo sea de tipo imagen permitido (JPG, PNG, GIF)
        
        Args:
            file_path (str): Ruta donde se guardará la imagen en el bucket
            file_bytes (bytes): Contenido de la imagen en bytes
            content_type (Optional[str]): Tipo MIME de la imagen (se detecta automáticamente si no se proporciona)
            upsert (bool): Si es True, sobrescribe la imagen si ya existe
            
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
        # Detectar el tipo MIME si no se proporciona
        detected_type = content_type
        if not detected_type:
            detected_type, _ = mimetypes.guess_type(file_path)
        
        # Validar tipo MIME
        if not detected_type or detected_type not in ALLOWED_IMAGE_TYPES:
            error_msg = (
                f"Tipo de archivo no permitido: {detected_type}. "
                f"Tipos permitidos: {', '.join(ALLOWED_IMAGE_TYPES)}"
            )
            return {
                "success": False,
                "path": file_path,
                "bucket": self._bucket,
                "message": error_msg
            }
        
        # Validar extensión del archivo
        file_path_lower = file_path.lower()
        if not any(file_path_lower.endswith(ext) for ext in ALLOWED_IMAGE_EXTENSIONS):
            error_msg = (
                f"Extensión de archivo no permitida. "
                f"Extensiones permitidas: {', '.join(ALLOWED_IMAGE_EXTENSIONS)}"
            )
            return {
                "success": False,
                "path": file_path,
                "bucket": self._bucket,
                "message": error_msg
            }
        
        # Usar el método base para subir el archivo
        return self.upload(
            file_path=file_path,
            file_bytes=file_bytes,
            content_type=detected_type,
            upsert=upsert
        )

