"""
Servicio especializado para almacenamiento de PDFs en Supabase Storage
"""

from typing import Optional
from supabase import Client
from services.storage.base_storage_service import SupabaseStorageService
from core.config import SupabaseSettings

# Tipo MIME para PDFs
PDF_MIME = "application/pdf"


class SupabasePDFStorageService(SupabaseStorageService):
    """
    Servicio especializado para almacenamiento de PDFs
    Valida que los archivos sean de tipo PDF
    """
    
    def __init__(self, client: Optional[Client] = None):
        """
        Inicializa el servicio de almacenamiento de PDFs
        
        Args:
            client (Optional[Client]): Cliente de Supabase (opcional)
        """
        settings = SupabaseSettings()
        super().__init__(bucket=settings.bucket_pdfs, client=client)
    
    def upload_pdf(
        self,
        file_path: str,
        file_bytes: bytes,
        upsert: bool = False
    ) -> dict:
        """
        Sube un PDF a Supabase Storage
        
        Valida que el archivo tenga extensión .pdf
        
        Args:
            file_path (str): Ruta donde se guardará el PDF en el bucket
            file_bytes (bytes): Contenido del PDF en bytes
            upsert (bool): Si es True, sobrescribe el PDF si ya existe
            
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
        # Validar extensión del archivo
        file_path_lower = file_path.lower()
        if not file_path_lower.endswith(".pdf"):
            error_msg = "El archivo debe tener extensión .pdf"
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
            content_type=PDF_MIME,
            upsert=upsert
        )

