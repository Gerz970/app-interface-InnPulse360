"""
Servicio especializado para almacenamiento de imágenes de limpieza en Supabase Storage
Maneja galería de imágenes por limpieza
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


class LimpiezaStorageService(SupabaseStorageService):
    """
    Servicio especializado para almacenamiento de imágenes de limpieza
    Valida rutas y proporciona métodos específicos para galería
    """
    
    def __init__(self, client: Optional[Client] = None):
        """
        Inicializa el servicio de almacenamiento de imágenes de limpieza
        
        Args:
            client (Optional[Client]): Cliente de Supabase (opcional)
        """
        settings = SupabaseSettings()
        super().__init__(bucket=settings.bucket_images, client=client)
        self.rutas_imagenes = RutasImagenes()
    
    def _validate_limpieza_path(self, file_path: str, id_limpieza: int) -> bool:
        """
        Valida que la ruta pertenezca a la limpieza especificada
        
        Args:
            file_path (str): Ruta del archivo
            id_limpieza (int): ID de la limpieza
            
        Returns:
            bool: True si la ruta es válida para la limpieza
        """
        expected_prefix = f"limpieza/{id_limpieza}/"
        return file_path.startswith(expected_prefix)
    
    def upload_galeria(
        self,
        id_limpieza: int,
        file_bytes: bytes,
        file_extension: str,
        content_type: Optional[str] = None
    ) -> dict:
        """
        Sube una imagen a la galería de la limpieza
        
        Las imágenes se guardan en: limpieza/{id_limpieza}/img_{id_limpieza}_item{identificador}.{extension}
        El nombre se genera automáticamente con formato: img_<id_limpieza>_item<uuid>
        
        Args:
            id_limpieza (int): ID de la limpieza
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
        
        # Generar nombre único automáticamente con formato: img_<id_limpieza>_item<uuid>
        # Usamos los primeros 8 caracteres del UUID para mantener nombres más cortos
        identificador = str(uuid.uuid4()).replace("-", "")[:8]
        nombre_archivo = f"img_{id_limpieza}_item{identificador}"
        
        # Construir ruta de galería
        ruta_galeria = self.rutas_imagenes.get_ruta_galeria_limpieza(id_limpieza)
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
    
    def list_galeria(self, id_limpieza: int) -> dict:
        """
        Lista todas las imágenes de la galería de una limpieza
        
        Args:
            id_limpieza (int): ID de la limpieza
            
        Returns:
            dict: Resultado con lista de imágenes
        """
        try:
            ruta_galeria = self.rutas_imagenes.get_ruta_galeria_limpieza(id_limpieza)
            
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
    
    def delete_galeria(self, id_limpieza: int, nombre_archivo: str) -> dict:
        """
        Elimina una imagen de la galería de la limpieza
        
        Args:
            id_limpieza (int): ID de la limpieza
            nombre_archivo (str): Nombre del archivo a eliminar
            
        Returns:
            dict: Resultado de la operación
        """
        ruta_galeria = self.rutas_imagenes.get_ruta_galeria_limpieza(id_limpieza)
        file_path = f"{ruta_galeria}/{nombre_archivo}"
        
        # Validar que la ruta pertenezca a la limpieza
        if not self._validate_limpieza_path(file_path, id_limpieza):
            return {
                "success": False,
                "message": "Ruta de archivo inválida para esta limpieza"
            }
        
        return self.delete(file_path)

