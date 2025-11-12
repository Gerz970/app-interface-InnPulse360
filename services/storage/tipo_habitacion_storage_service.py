"""
Servicio especializado para almacenamiento de imágenes de tipos de habitación en Supabase Storage
Maneja foto de perfil y galería de imágenes por tipo de habitación
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

# Tipos MIME permitidos para imágenes de tipos de habitación
ALLOWED_IMAGE_TYPES = ("image/jpeg", "image/png", "image/webp")

# Extensiones permitidas
ALLOWED_IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp")


class TipoHabitacionStorageService(SupabaseStorageService):
    """
    Servicio especializado para almacenamiento de imágenes de tipos de habitación
    Valida rutas y proporciona métodos específicos para foto de perfil y galería
    """
    
    def __init__(self, client: Optional[Client] = None):
        """
        Inicializa el servicio de almacenamiento de imágenes de tipos de habitación
        
        Args:
            client (Optional[Client]): Cliente de Supabase (opcional)
        """
        settings = SupabaseSettings()
        super().__init__(bucket=settings.bucket_images, client=client)
        self.rutas_imagenes = RutasImagenes()
    
    def _validate_tipo_habitacion_path(self, file_path: str, id_tipoHabitacion: int) -> bool:
        """
        Valida que la ruta pertenezca al tipo de habitación especificado
        
        Args:
            file_path (str): Ruta del archivo
            id_tipoHabitacion (int): ID del tipo de habitación
            
        Returns:
            bool: True si la ruta es válida para el tipo de habitación
        """
        expected_prefix = f"tipo_habitacion/{id_tipoHabitacion}/"
        return file_path.startswith(expected_prefix)
    
    def upload_foto_perfil(
        self,
        id_tipoHabitacion: int,
        file_bytes: bytes,
        file_extension: str,
        content_type: Optional[str] = None
    ) -> dict:
        """
        Sube o actualiza la foto de perfil de un tipo de habitación
        
        La foto de perfil se guarda como: tipo_habitacion/{id_tipoHabitacion}/{id_tipoHabitacion}.{extension}
        
        Args:
            id_tipoHabitacion (int): ID del tipo de habitación
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
        ruta_base = self.rutas_imagenes.get_ruta_foto_perfil_tipo_habitacion(id_tipoHabitacion)
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
    
    def delete_foto_perfil(self, id_tipoHabitacion: int) -> dict:
        """
        Elimina la foto de perfil de un tipo de habitación
        
        Args:
            id_tipoHabitacion (int): ID del tipo de habitación
            
        Returns:
            dict: Resultado de la operación
        """
        ruta_base = self.rutas_imagenes.get_ruta_foto_perfil_tipo_habitacion(id_tipoHabitacion)
        
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
        id_tipoHabitacion: int,
        file_bytes: bytes,
        file_extension: str,
        content_type: Optional[str] = None
    ) -> dict:
        """
        Sube una imagen a la galería del tipo de habitación
        
        Las imágenes se guardan en: tipo_habitacion/{id_tipoHabitacion}/galeria/img_{id_tipoHabitacion}_item{identificador}.{extension}
        El nombre se genera automáticamente con formato: img_<id_tipoHabitacion>_item<uuid>
        
        Args:
            id_tipoHabitacion (int): ID del tipo de habitación
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
        
        # Generar nombre único automáticamente con formato: img_<id_tipoHabitacion>_item<uuid>
        # Usamos los primeros 8 caracteres del UUID para mantener nombres más cortos
        identificador = str(uuid.uuid4()).replace("-", "")[:8]
        nombre_archivo = f"img_{id_tipoHabitacion}_item{identificador}"
        
        # Construir ruta de galería
        ruta_galeria = self.rutas_imagenes.get_ruta_galeria_tipo_habitacion(id_tipoHabitacion)
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
    
    def list_galeria(self, id_tipoHabitacion: int) -> dict:
        """
        Lista todas las imágenes de la galería de un tipo de habitación
        
        Args:
            id_tipoHabitacion (int): ID del tipo de habitación
            
        Returns:
            dict: Resultado con lista de imágenes
        """
        try:
            ruta_galeria = self.rutas_imagenes.get_ruta_galeria_tipo_habitacion(id_tipoHabitacion)
            
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
    
    def delete_galeria(self, id_tipoHabitacion: int, nombre_archivo: str) -> dict:
        """
        Elimina una imagen de la galería del tipo de habitación
        
        Args:
            id_tipoHabitacion (int): ID del tipo de habitación
            nombre_archivo (str): Nombre del archivo a eliminar
            
        Returns:
            dict: Resultado de la operación
        """
        ruta_galeria = self.rutas_imagenes.get_ruta_galeria_tipo_habitacion(id_tipoHabitacion)
        file_path = f"{ruta_galeria}/{nombre_archivo}"
        
        # Validar que la ruta pertenezca al tipo de habitación
        if not self._validate_tipo_habitacion_path(file_path, id_tipoHabitacion):
            return {
                "success": False,
                "message": "Ruta de archivo inválida para este tipo de habitación"
            }
        
        return self.delete(file_path)

