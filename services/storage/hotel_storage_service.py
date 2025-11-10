"""
Servicio especializado para almacenamiento de imágenes de hoteles en Supabase Storage
Maneja foto de perfil y galería de imágenes por hotel
"""

import logging
import uuid
from typing import Optional, List
from supabase import Client
from services.storage.base_storage_service import SupabaseStorageService
from core.config import SupabaseSettings
from utils.rutas_imagenes import RutasImagenes

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Tipos MIME permitidos para imágenes de hoteles
ALLOWED_IMAGE_TYPES = ("image/jpeg", "image/png", "image/webp")

# Extensiones permitidas
ALLOWED_IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp")


class HotelStorageService(SupabaseStorageService):
    """
    Servicio especializado para almacenamiento de imágenes de hoteles
    Valida rutas y proporciona métodos específicos para foto de perfil y galería
    """
    
    def __init__(self, client: Optional[Client] = None):
        """
        Inicializa el servicio de almacenamiento de imágenes de hoteles
        
        Args:
            client (Optional[Client]): Cliente de Supabase (opcional)
        """
        settings = SupabaseSettings()
        super().__init__(bucket=settings.bucket_images, client=client)
        self.rutas_imagenes = RutasImagenes()
    
    def _validate_hotel_path(self, file_path: str, id_hotel: int) -> bool:
        """
        Valida que la ruta pertenezca al hotel especificado
        
        Args:
            file_path (str): Ruta del archivo
            id_hotel (int): ID del hotel
            
        Returns:
            bool: True si la ruta es válida para el hotel
        """
        expected_prefix = f"hotel/{id_hotel}/"
        return file_path.startswith(expected_prefix)
    
    def upload_foto_perfil(
        self,
        id_hotel: int,
        file_bytes: bytes,
        file_extension: str,
        content_type: Optional[str] = None
    ) -> dict:
        """
        Sube o actualiza la foto de perfil de un hotel
        
        La foto de perfil se guarda como: hotel/{id_hotel}/{id_hotel}.{extension}
        
        Args:
            id_hotel (int): ID del hotel
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
        
        # Construir ruta de foto de perfil
        ruta_base = self.rutas_imagenes.get_ruta_foto_perfil_hotel(id_hotel)
        file_path = f"{ruta_base}{file_extension}"
        
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
        
        # Subir con upsert=True para reemplazar si existe
        return self.upload(
            file_path=file_path,
            file_bytes=file_bytes,
            content_type=content_type,
            upsert=True
        )
    
    def delete_foto_perfil(self, id_hotel: int) -> dict:
        """
        Elimina la foto de perfil de un hotel
        
        Args:
            id_hotel (int): ID del hotel
            
        Returns:
            dict: Resultado de la operación
        """
        ruta_base = self.rutas_imagenes.get_ruta_foto_perfil_hotel(id_hotel)
        
        # Intentar eliminar con diferentes extensiones
        for ext in ALLOWED_IMAGE_EXTENSIONS:
            file_path = f"{ruta_base}{ext}"
            result = self.delete(file_path)
            if result.get("success"):
                return result
        
        # Si no se encontró ninguna, retornar éxito de todas formas
        return {
            "success": True,
            "message": "Foto de perfil no encontrada o ya eliminada"
        }
    
    def upload_galeria(
        self,
        id_hotel: int,
        file_bytes: bytes,
        file_extension: str,
        content_type: Optional[str] = None
    ) -> dict:
        """
        Sube una imagen a la galería del hotel
        
        Las imágenes se guardan en: hotel/{id_hotel}/galeria/img_{id_hotel}_item{identificador}.{extension}
        El nombre se genera automáticamente con formato: img_<hotel_id>_item<uuid>
        
        Args:
            id_hotel (int): ID del hotel
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
        
        # Generar nombre único automáticamente con formato: img_<hotel_id>_item<uuid>
        # Usamos los primeros 8 caracteres del UUID para mantener nombres más cortos
        identificador = str(uuid.uuid4()).replace("-", "")[:8]
        nombre_archivo = f"img_{id_hotel}_item{identificador}"
        
        # Construir ruta de galería
        ruta_galeria = self.rutas_imagenes.get_ruta_galeria_hotel(id_hotel)
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
    
    def list_galeria(self, id_hotel: int) -> dict:
        """
        Lista todas las imágenes de la galería de un hotel
        
        Args:
            id_hotel (int): ID del hotel
            
        Returns:
            dict: Resultado con lista de imágenes
        """
        try:
            ruta_galeria = self.rutas_imagenes.get_ruta_galeria_hotel(id_hotel)
            
            # Listar archivos en la carpeta de galería
            response = self._client.storage.from_(self._bucket).list(path=ruta_galeria)
            
            # Filtrar solo imágenes válidas
            imagenes = []
            for item in response:
                if isinstance(item, dict):
                    nombre = item.get("name", "")
                    # Verificar que sea una imagen válida
                    if any(nombre.lower().endswith(ext) for ext in ALLOWED_IMAGE_EXTENSIONS):
                        ruta_completa = f"{ruta_galeria}/{nombre}"
                        url_publica = self.build_public_url(ruta_completa)
                        imagenes.append({
                            "nombre": nombre,
                            "ruta": ruta_completa,
                            "url_publica": url_publica,
                            "tamaño": item.get("metadata", {}).get("size", 0)
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
    
    def delete_galeria(self, id_hotel: int, nombre_archivo: str) -> dict:
        """
        Elimina una imagen de la galería del hotel
        
        Args:
            id_hotel (int): ID del hotel
            nombre_archivo (str): Nombre del archivo a eliminar
            
        Returns:
            dict: Resultado de la operación
        """
        ruta_galeria = self.rutas_imagenes.get_ruta_galeria_hotel(id_hotel)
        file_path = f"{ruta_galeria}/{nombre_archivo}"
        
        # Validar que la ruta pertenezca al hotel
        if not self._validate_hotel_path(file_path, id_hotel):
            return {
                "success": False,
                "message": "Ruta de archivo inválida para este hotel"
            }
        
        return self.delete(file_path)
    
    def get_foto_perfil_url(self, id_hotel: int, ruta_storage: Optional[str] = None) -> Optional[str]:
        """
        Obtiene la URL pública de la foto de perfil del hotel
        
        Args:
            id_hotel (int): ID del hotel
            ruta_storage (Optional[str]): Ruta almacenada en BD (si no se proporciona, intenta construirla)
            
        Returns:
            Optional[str]: URL pública de la foto de perfil
        """
        if ruta_storage:
            return self.build_public_url(ruta_storage)
        
        # Intentar construir URL desde convención
        ruta_base = self.rutas_imagenes.get_ruta_foto_perfil_hotel(id_hotel)
        for ext in ALLOWED_IMAGE_EXTENSIONS:
            ruta_posible = f"{ruta_base}{ext}"
            url = self.build_public_url(ruta_posible)
            if url:
                return url
        
        # Si no se encuentra, retornar URL de default
        ruta_default = self.rutas_imagenes.get_ruta_default_hotel(id_hotel)
        return self.build_public_url(ruta_default)

