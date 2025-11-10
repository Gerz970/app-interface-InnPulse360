"""
Servicio de Hotel
Contiene la lógica de negocio para las operaciones relacionadas con hoteles
Actúa como intermediario entre las rutas (API) y el DAO (acceso a datos)
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from dao.hotel.dao_hotel import HotelDAO
from schemas.hotel import HotelCreate, HotelUpdate, HotelResponse
from models.hotel.hotel_model import Hotel
from core.config import SupabaseSettings
from utils.rutas_imagenes import RutasImagenes


class HotelService:
    """
    Servicio que encapsula la lógica de negocio para operaciones de Hotel
    """
    
    def __init__(self, db_session: Session):
        """
        Inicializa el servicio con una sesión de base de datos
        
        Args:
            db_session (Session): Sesión de SQLAlchemy
        """
        self.db = db_session
        self.dao = HotelDAO(db_session)
        self.supabase_settings = SupabaseSettings()
        self.rutas_imagenes = RutasImagenes()
    
    def _build_foto_perfil_url(self, ruta_storage: Optional[str]) -> Optional[str]:
        """
        Construye la URL pública de una foto de perfil desde la ruta de storage
        
        Args:
            ruta_storage (Optional[str]): Ruta del archivo en storage (ej: "hotel/123/123.jpg")
            
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
    
    def _build_hotel_response(self, hotel: Hotel) -> HotelResponse:
        """
        Construye un HotelResponse desde un modelo Hotel, incluyendo URL de foto de perfil
        
        Args:
            hotel (Hotel): Modelo de hotel
            
        Returns:
            HotelResponse: Schema de respuesta con URL de foto construida
        """
        # Construir URL completa desde la ruta almacenada
        url_foto_completa = None
        if hotel.url_foto_perfil:
            url_foto_completa = self._build_foto_perfil_url(hotel.url_foto_perfil)
        
        hotel_dict = {
            "id_hotel": hotel.id_hotel,
            "nombre": hotel.nombre,
            "direccion": hotel.direccion,
            "id_estado": hotel.id_estado,
            "id_pais": hotel.id_pais,
            "codigo_postal": hotel.codigo_postal,
            "telefono": hotel.telefono,
            "email_contacto": hotel.email_contacto,
            "numero_estrellas": hotel.numero_estrellas,
            "url_foto_perfil": url_foto_completa
        }
        
        return HotelResponse(**hotel_dict)
    
    def crear_hotel(self, hotel_data: HotelCreate) -> HotelResponse:
        """
        Crea un nuevo hotel
        
        Args:
            hotel_data (HotelCreate): Datos del hotel a crear
            
        Returns:
            HotelResponse: Hotel creado
            
        Raises:
            ValueError: Si hay un error de validación
            Exception: Si hay un error en la base de datos
        """
        try:
            # Aquí se pueden agregar validaciones de negocio adicionales
            # Por ejemplo, verificar que no exista otro hotel con el mismo nombre
            
            # Crear hotel usando el DAO
            hotel_creado = self.dao.create(hotel_data)
            
            # Asignar foto de perfil por defecto si no se proporciona
            if not hotel_creado.url_foto_perfil:
                ruta_default = self.rutas_imagenes.get_ruta_default_hotel(hotel_creado.id_hotel)
                # Guardar solo la ruta relativa, no la URL completa
                update_data = HotelUpdate(url_foto_perfil=ruta_default)
                self.dao.update(hotel_creado.id_hotel, update_data)
                # Refrescar el objeto para obtener la ruta actualizada
                self.db.refresh(hotel_creado)
            
            # Convertir a schema de respuesta con URL construida
            return self._build_hotel_response(hotel_creado)
            
        except SQLAlchemyError as e:
            raise Exception(f"Error al crear hotel en la base de datos: {str(e)}")
        except Exception as e:
            raise Exception(f"Error inesperado al crear hotel: {str(e)}")
    
    def obtener_hotel_por_id(self, hotel_id: int) -> Optional[HotelResponse]:
        """
        Obtiene un hotel por su ID
        
        Args:
            hotel_id (int): ID del hotel
            
        Returns:
            Optional[HotelResponse]: Hotel encontrado o None
            
        Raises:
            Exception: Si hay un error en la base de datos
        """
        try:
            hotel = self.dao.get_by_id(hotel_id)
            
            if not hotel:
                return None
            
            return self._build_hotel_response(hotel)
            
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener hotel de la base de datos: {str(e)}")
        except Exception as e:
            raise Exception(f"Error inesperado al obtener hotel: {str(e)}")
    
    def obtener_todos_los_hoteles(self, skip: int = 0, limit: int = 100) -> List[HotelResponse]:
        """
        Obtiene todos los hoteles con paginación
        
        Args:
            skip (int): Número de registros a saltar
            limit (int): Número máximo de registros
            
        Returns:
            List[HotelResponse]: Lista de hoteles
            
        Raises:
            Exception: Si hay un error en la base de datos
        """
        try:
            hoteles = self.dao.get_all(skip=skip, limit=limit)
            
            # Convertir cada hotel a schema de respuesta con URLs construidas
            return [self._build_hotel_response(hotel) for hotel in hoteles]
            
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener hoteles de la base de datos: {str(e)}")
        except Exception as e:
            raise Exception(f"Error inesperado al obtener hoteles: {str(e)}")
    
    def actualizar_hotel(self, hotel_id: int, hotel_update: HotelUpdate) -> Optional[HotelResponse]:
        """
        Actualiza un hotel existente
        
        Args:
            hotel_id (int): ID del hotel a actualizar
            hotel_update (HotelUpdate): Datos a actualizar
            
        Returns:
            Optional[HotelResponse]: Hotel actualizado o None si no existe
            
        Raises:
            Exception: Si hay un error en la base de datos
        """
        try:
            # Validar que al menos un campo esté presente para actualizar
            update_data = hotel_update.model_dump(exclude_unset=True)
            
            if not update_data:
                raise ValueError("Debe proporcionar al menos un campo para actualizar")
            
            # Actualizar usando el DAO
            hotel_actualizado = self.dao.update(hotel_id, hotel_update)
            
            if not hotel_actualizado:
                return None
            
            return self._build_hotel_response(hotel_actualizado)
            
        except ValueError as e:
            raise e
        except SQLAlchemyError as e:
            raise Exception(f"Error al actualizar hotel en la base de datos: {str(e)}")
        except Exception as e:
            raise Exception(f"Error inesperado al actualizar hotel: {str(e)}")
    
    def eliminar_hotel(self, hotel_id: int) -> bool:
        """
        Elimina un hotel
        
        Args:
            hotel_id (int): ID del hotel a eliminar
            
        Returns:
            bool: True si se eliminó, False si no existe
            
        Raises:
            Exception: Si hay un error en la base de datos
        """
        try:
            return self.dao.delete_logical(hotel_id)
            
        except SQLAlchemyError as e:
            raise Exception(f"Error al eliminar hotel de la base de datos: {str(e)}")
        except Exception as e:
            raise Exception(f"Error inesperado al eliminar hotel: {str(e)}")
    
    def buscar_por_nombre(self, nombre: str) -> List[HotelResponse]:
        """
        Busca hoteles por nombre
        
        Args:
            nombre (str): Nombre o parte del nombre
            
        Returns:
            List[HotelResponse]: Lista de hoteles encontrados
        """
        try:
            hoteles = self.dao.get_by_nombre(nombre)
            return [self._build_hotel_response(hotel) for hotel in hoteles]
        except Exception as e:
            raise Exception(f"Error al buscar hoteles por nombre: {str(e)}")
    
    def obtener_por_pais(self, id_pais: int) -> List[HotelResponse]:
        """
        Obtiene hoteles por país
        
        Args:
            id_pais (int): ID del país
            
        Returns:
            List[HotelResponse]: Lista de hoteles del país
        """
        try:
            hoteles = self.dao.get_by_pais(id_pais)
            return [self._build_hotel_response(hotel) for hotel in hoteles]
        except Exception as e:
            raise Exception(f"Error al obtener hoteles por país: {str(e)}")
    
    def obtener_por_estrellas(self, numero_estrellas: int) -> List[HotelResponse]:
        """
        Obtiene hoteles por número de estrellas
        
        Args:
            numero_estrellas (int): Número de estrellas (1-5)
            
        Returns:
            List[HotelResponse]: Lista de hoteles
        """
        try:
            if numero_estrellas < 1 or numero_estrellas > 5:
                raise ValueError("El número de estrellas debe estar entre 1 y 5")
            
            hoteles = self.dao.get_by_estrellas(numero_estrellas)
            return [self._build_hotel_response(hotel) for hotel in hoteles]
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Error al obtener hoteles por estrellas: {str(e)}")
    
    def actualizar_url_foto_perfil(self, id_hotel: int, ruta_storage: str) -> None:
        """
        Actualiza la ruta de foto de perfil de un hotel en la base de datos
        Guarda solo la ruta relativa al bucket, no la URL completa
        
        Args:
            id_hotel (int): ID del hotel
            ruta_storage (str): Ruta del archivo en storage (ej: "hotel/123/123.jpg")
            
        Raises:
            HTTPException: Si el hotel no existe
        """
        hotel = self.dao.get_by_id(id_hotel)
        if not hotel:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Hotel no encontrado"
            )
        
        # Guardar solo la ruta relativa al bucket, no la URL completa
        # Esto hace el sistema más flexible y portable
        update_data = HotelUpdate(url_foto_perfil=ruta_storage)
        self.dao.update(id_hotel, update_data)

