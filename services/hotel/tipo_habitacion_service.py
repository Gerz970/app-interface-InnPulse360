from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status

from dao.hotel.dao_tipo_habitacion import TipoHabitacionDAO
from models.hotel.tipo_habitacion_model import TipoHabitacion
from schemas.hotel.tipo_habitacion_schemas import (
    TipoHabitacionCreate,
    TipoHabitacionUpdate,
    TipoHabitacionResponse,
    PeriodicidadResponse
)
from core.config import SupabaseSettings
from utils.rutas_imagenes import RutasImagenes


class TipoHabitacionService:
    """
    Servicio para manejar la lógica de negocio de tipos de habitación
    """

    def __init__(self, db_session: Session):
        self.db = db_session
        self.dao = TipoHabitacionDAO(db_session)
        self.supabase_settings = SupabaseSettings()
        self.rutas_imagenes = RutasImagenes()
    
    def _build_foto_perfil_url(self, ruta_storage: Optional[str]) -> Optional[str]:
        """
        Construye la URL pública de una foto de perfil desde la ruta de storage
        
        Args:
            ruta_storage (Optional[str]): Ruta del archivo en storage (ej: "tipo_habitacion/123/123.jpg")
            
        Returns:
            Optional[str]: URL pública completa o None si no hay ruta o configuración
        """
        if not ruta_storage:
            return None
        
        if not self.supabase_settings.public_base_url:
            return None
        
        base_url = self.supabase_settings.public_base_url.rstrip('/')
        bucket = self.supabase_settings.bucket_images
        
        return f"{base_url}/storage/v1/object/public/{bucket}/{ruta_storage}"
    
    def _build_tipo_habitacion_response(self, tipo_habitacion: TipoHabitacion, incluir_galeria: bool = False) -> TipoHabitacionResponse:
        """
        Construye un TipoHabitacionResponse desde un modelo TipoHabitacion, incluyendo URL de foto de perfil y galería
        
        Args:
            tipo_habitacion (TipoHabitacion): Modelo de tipo de habitación
            incluir_galeria (bool): Si True, incluye la galería de imágenes
            
        Returns:
            TipoHabitacionResponse: Schema de respuesta con URL de foto construida
        """
        # Construir URL completa desde la ruta almacenada
        url_foto_completa = None
        if tipo_habitacion.url_foto_perfil:
            url_foto_completa = self._build_foto_perfil_url(tipo_habitacion.url_foto_perfil)
        
        # Obtener galería si se solicita
        galeria_urls = None
        if incluir_galeria:
            try:
                from services.storage.tipo_habitacion_storage_service import TipoHabitacionStorageService
                storage_service = TipoHabitacionStorageService()
                galeria_result = storage_service.list_galeria(tipo_habitacion.id_tipoHabitacion)
                if galeria_result.get("success") and galeria_result.get("imagenes"):
                    galeria_urls = [img.get("url_publica") for img in galeria_result["imagenes"] if img.get("url_publica")]
                else:
                    galeria_urls = []
            except Exception as e:
                print(f"Error al obtener galería para tipo {tipo_habitacion.id_tipoHabitacion}: {e}")
                galeria_urls = []
        
        # Construir diccionario con todos los campos
        tipo_dict = {
            "id_tipoHabitacion": tipo_habitacion.id_tipoHabitacion,
            "clave": tipo_habitacion.clave,
            "precio_unitario": tipo_habitacion.precio_unitario,
            "periodicidad_id": tipo_habitacion.periodicidad_id,
            "tipo_habitacion": tipo_habitacion.tipo_habitacion,
            "estatus_id": tipo_habitacion.estatus_id,
            "url_foto_perfil": url_foto_completa,
            "galeria_tipo_habitacion": galeria_urls
        }
        
        # Agregar periodicidad si está cargada
        if tipo_habitacion.periodicidad:
            from schemas.catalogos.periodicidad_schemas import PeriodicidadResponse
            tipo_dict["periodicidad"] = PeriodicidadResponse.model_validate(tipo_habitacion.periodicidad)
        else:
            tipo_dict["periodicidad"] = None
        
        return TipoHabitacionResponse(**tipo_dict)
    
    def actualizar_url_foto_perfil(self, id_tipoHabitacion: int, ruta_storage: str) -> bool:
        """
        Actualiza la URL de foto de perfil en la base de datos
        
        Args:
            id_tipoHabitacion (int): ID del tipo de habitación
            ruta_storage (str): Ruta relativa del archivo en storage
            
        Returns:
            bool: True si se actualizó correctamente
        """
        update_data = TipoHabitacionUpdate(url_foto_perfil=ruta_storage)
        db_tipo = self.dao.update(id_tipoHabitacion, update_data)
        return db_tipo is not None

    def create_tipo_habitacion(self, tipo_habitacion_data: TipoHabitacionCreate) -> TipoHabitacionResponse:
        # Verificar clave
        if tipo_habitacion_data.clave and self.dao.exists_by_clave(tipo_habitacion_data.clave):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="La clave del tipo de habitación ya está en uso")

        # Verificar nombre
        if self.dao.exists_by_nombre(tipo_habitacion_data.tipo_habitacion):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="El nombre del tipo de habitación ya está en uso")

        db_tipo = self.dao.create(tipo_habitacion_data)
        
        # Asignar foto de perfil por defecto si no se proporciona
        if not db_tipo.url_foto_perfil:
            ruta_default = self.rutas_imagenes.get_ruta_default_tipo_habitacion(db_tipo.id_tipoHabitacion)
            # Guardar solo la ruta relativa, no la URL completa
            update_data = TipoHabitacionUpdate(url_foto_perfil=ruta_default)
            self.dao.update(db_tipo.id_tipoHabitacion, update_data)
            # Refrescar el objeto para obtener la ruta actualizada
            self.db.refresh(db_tipo)

        return self._build_tipo_habitacion_response(db_tipo)

    def get_tipo_habitacion_by_id(self, id_tipoHabitacion: int) -> Optional[TipoHabitacionResponse]:
        # Cargar con la relación de periodicidad usando joinedload
        db_tipo = (
            self.db.query(TipoHabitacion)
            .options(joinedload(TipoHabitacion.periodicidad))
            .filter(TipoHabitacion.id_tipoHabitacion == id_tipoHabitacion)
            .first()
        )
        if not db_tipo:
            return None
        return self._build_tipo_habitacion_response(db_tipo, incluir_galeria=True)

    def get_tipo_habitacion_by_clave(self, clave: str) -> Optional[TipoHabitacionResponse]:
        db_tipo = self.dao.get_by_clave(clave)
        if not db_tipo:
            return None
        return self._build_tipo_habitacion_response(db_tipo)

    def get_tipo_habitacion_by_nombre(self, tipo_habitacion: str) -> Optional[TipoHabitacionResponse]:
        db_tipo = self.dao.get_by_nombre(tipo_habitacion)
        if not db_tipo:
            return None
        return self._build_tipo_habitacion_response(db_tipo)

    def get_all_tipos_habitacion(self, skip: int = 0, limit: int = 100) -> List[TipoHabitacionResponse]:
        db_tipos = (
            self.db.query(TipoHabitacion)
            .options(joinedload(TipoHabitacion.periodicidad))  # 👈 Cargar relación
            .filter(TipoHabitacion.estatus_id == 1)
            .order_by(TipoHabitacion.id_tipoHabitacion.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._build_tipo_habitacion_response(t) for t in db_tipos]

    def update_tipo_habitacion(self, id_tipoHabitacion: int, tipo_habitacion_data: TipoHabitacionUpdate) -> Optional[TipoHabitacionResponse]:
        existing_tipo = self.dao.get_by_id(id_tipoHabitacion)
        if not existing_tipo:
            return None

        # Validar conflictos de clave
        if tipo_habitacion_data.clave and tipo_habitacion_data.clave != existing_tipo.clave:
            if self.dao.exists_by_clave(tipo_habitacion_data.clave, exclude_id=id_tipoHabitacion):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="La clave del tipo de habitación ya está en uso")

        # Validar conflictos de nombre
        if tipo_habitacion_data.tipo_habitacion and tipo_habitacion_data.tipo_habitacion != existing_tipo.tipo_habitacion:
            if self.dao.exists_by_nombre(tipo_habitacion_data.tipo_habitacion, exclude_id=id_tipoHabitacion):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="El nombre del tipo de habitación ya está en uso")

        db_tipo = self.dao.update(id_tipoHabitacion, tipo_habitacion_data)
        if not db_tipo:
            return None

        return self._build_tipo_habitacion_response(db_tipo)

    def delete_tipo_habitacion(self, id_tipoHabitacion: int) -> bool:
        return self.dao.delete_logical(id_tipoHabitacion)

    def reactivate_tipo_habitacion(self, id_tipoHabitacion: int) -> bool:
        return self.dao.reactivate(id_tipoHabitacion)
