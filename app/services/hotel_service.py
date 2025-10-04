"""
Servicio de Hotel
Contiene la lógica de negocio para las operaciones relacionadas con hoteles
Actúa como intermediario entre las rutas (API) y el DAO (acceso a datos)
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from dao.dao_hotel import HotelDAO
from schemas.hotel import HotelCreate, HotelUpdate, HotelResponse
from models.hotel.hotel_model import Hotel


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
        self.dao = HotelDAO(db_session)
    
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
            
            # Convertir a schema de respuesta
            return HotelResponse.model_validate(hotel_creado)
            
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
            
            return HotelResponse.model_validate(hotel)
            
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
            
            # Convertir cada hotel a schema de respuesta
            return [HotelResponse.model_validate(hotel) for hotel in hoteles]
            
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
            
            return HotelResponse.model_validate(hotel_actualizado)
            
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
            return [HotelResponse.model_validate(hotel) for hotel in hoteles]
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
            return [HotelResponse.model_validate(hotel) for hotel in hoteles]
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
            return [HotelResponse.model_validate(hotel) for hotel in hoteles]
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Error al obtener hoteles por estrellas: {str(e)}")

