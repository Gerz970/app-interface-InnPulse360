"""
Servicio especializado para almacenamiento de imágenes de mantenimiento en Supabase Storage
Maneja galería de imágenes por mantenimiento
"""

import logging
import uuid
from typing import Optional
from supabase import Client
from services.storage.base_storage_service import SupabaseStorageService
from core.config import SupabaseSettings
from utils.rutas_imagenes import RutasImagenes

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Tipos MIME permitidos para imágenes
ALLOWED_IMAGE_TYPES = ("image/jpeg", "image/png", "image/webp")

# Extensiones permitidas
ALLOWED_IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp")


class MantenimientoStorageService(SupabaseStorageService):
    """
    Servicio especializado para almacenamiento de imágenes de mantenimiento
    Valida rutas y proporciona métodos específicos para galería
    """
    
    def __init__(self, client: Optional[Client] = None):
        """
        Inicializa el servicio de almacenamiento de imágenes de mantenimiento
        
        Args:
            client (Optional[Client]): Cliente de Supabase (opcional)
        """
        settings = SupabaseSettings()
        super().__init__(bucket=settings.bucket_images, client=client)
        self.rutas_imagenes = RutasImagenes()
    
    def _validate_mantenimiento_path(self, file_path: str, id_mantenimiento: int) -> bool:
        """
        Valida que la ruta pertenezca al mantenimiento especificado
        
        Args:
            file_path (str): Ruta del archivo
            id_mantenimiento (int): ID del mantenimiento
            
        Returns:
            bool: True si la ruta es válida para el mantenimiento
        """
        expected_prefix = f"mantenimiento/{id_mantenimiento}/"
        return file_path.startswith(expected_prefix)
    
    def upload_galeria(
        self,
        id_mantenimiento: int,
        file_bytes: bytes,
        file_extension: str,
        content_type: Optional[str] = None
    ) -> dict:
        """
        Sube una imagen a la galería del mantenimiento
        
        Las imágenes se guardan en: mantenimiento/{id_mantenimiento}/img_{id_mantenimiento}_item{identificador}.{extension}
        El nombre se genera automáticamente con formato: img_<id_mantenimiento>_item<uuid>
        
        Args:
            id_mantenimiento (int): ID del mantenimiento
            file_bytes (bytes): Contenido de la imagen en bytes
            file_extension (str): Extensión del archivo (ej: ".jpg")
            content_type (Optional[str]): Tipo MIME de la imagen
            
        Returns:
            dict: Resultado de la operación
        """
        # Validar extensión
        if file_extension.lower() not in ALLOWED_IMAGE_EXTENSIONS:
            return {
                "success": False,
                "message": f"Extensión no permitida. Extensiones permitidas: {', '.join(ALLOWED_IMAGE_EXTENSIONS)}"
            }
        
        # Generar nombre único automáticamente con formato: img_<id_mantenimiento>_item<uuid>
        # Usamos los primeros 8 caracteres del UUID para mantener nombres más cortos
        identificador = str(uuid.uuid4()).replace("-", "")[:8]
        nombre_archivo = f"img_{id_mantenimiento}_item{identificador}"
        
        # Construir ruta de galería
        ruta_galeria = self.rutas_imagenes.get_ruta_galeria_mantenimiento(id_mantenimiento)
        file_path = f"{ruta_galeria}/{nombre_archivo}{file_extension}"
        
        # Detectar content type si no se proporciona
        if not content_type:
            content_type_map = {
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".png": "image/png",
                ".webp": "image/webp"
            }
            content_type = content_type_map.get(file_extension.lower(), "image/jpeg")
        
        # Validar tipo MIME
        if content_type not in ALLOWED_IMAGE_TYPES:
            return {
                "success": False,
                "message": f"Tipo MIME no permitido. Tipos permitidos: {', '.join(ALLOWED_IMAGE_TYPES)}"
            }
        
        # Subir imagen
        return self.upload(
            file_path=file_path,
            file_bytes=file_bytes,
            content_type=content_type,
            upsert=False
        )
    
    def list_galeria(self, id_mantenimiento: int) -> dict:
        """
        Lista todas las imágenes de la galería de un mantenimiento
        
        Args:
            id_mantenimiento (int): ID del mantenimiento
            
        Returns:
            dict: Resultado con lista de imágenes
        """
        try:
            ruta_galeria = self.rutas_imagenes.get_ruta_galeria_mantenimiento(id_mantenimiento)
            
            # Listar archivos en la carpeta de galería
            response = self._client.storage.from_(self._bucket).list(path=ruta_galeria)
            
            # Filtrar solo imágenes válidas
            imagenes = []
            if response:
                for item in response:
                    # La respuesta puede ser una lista de diccionarios o objetos
                    if isinstance(item, dict):
                        nombre = item.get("name", "")
                    else:
                        # Si es un objeto, intentar acceder al atributo name
                        nombre = getattr(item, "name", "")
                    
                    # Verificar que sea una imagen válida
                    if nombre and any(nombre.lower().endswith(ext) for ext in ALLOWED_IMAGE_EXTENSIONS):
                        ruta_completa = f"{ruta_galeria}/{nombre}"
                        url_publica = self.build_public_url(ruta_completa)
                        
                        # Obtener tamaño si está disponible
                        tamaño = 0
                        if isinstance(item, dict):
                            tamaño = item.get("metadata", {}).get("size", 0) if item.get("metadata") else 0
                        else:
                            tamaño = getattr(item, "size", 0) if hasattr(item, "size") else 0
                        
                        imagenes.append({
                            "nombre": nombre,
                            "ruta": ruta_completa,
                            "url_publica": url_publica,
                            "tamaño": tamaño
                        })
            
            return {
                "success": True,
                "imagenes": imagenes,
                "total": len(imagenes)
            }
            
        except Exception as exc:
            error_msg = f"Error al listar galería: {str(exc)}"
            logger.error(error_msg, exc_info=exc)
            return {
                "success": False,
                "imagenes": [],
                "total": 0,
                "message": error_msg
            }
    
    def delete_galeria(self, id_mantenimiento: int, nombre_archivo: str) -> dict:
        """
        Elimina una imagen de la galería del mantenimiento
        
        Args:
            id_mantenimiento (int): ID del mantenimiento
            nombre_archivo (str): Nombre del archivo a eliminar
            
        Returns:
            dict: Resultado de la operación
        """
        ruta_galeria = self.rutas_imagenes.get_ruta_galeria_mantenimiento(id_mantenimiento)
        file_path = f"{ruta_galeria}/{nombre_archivo}"
        
        # Validar que la ruta pertenezca al mantenimiento
        if not self._validate_mantenimiento_path(file_path, id_mantenimiento):
            return {
                "success": False,
                "message": "Ruta de archivo inválida para este mantenimiento"
            }
        
        return self.delete(file_path)

