"""
DAO (Data Access Object) para operaciones CRUD de Hotel
Maneja todas las interacciones con la base de datos para la entidad Hotel
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.hotel.hotel_model import Hotel
from schemas.hotel import HotelCreate, HotelUpdate


class HotelDAO:
    """
    Clase DAO para manejar operaciones CRUD de Hotel en la base de datos
    Utiliza SQLAlchemy ORM para las operaciones
    """

    __status_active__ = 1
    __status_inactive__ = 0
    
    def __init__(self, db_session: Session):
        """
        Inicializa el DAO con una sesión de base de datos
        
        Args:
            db_session (Session): Sesión de SQLAlchemy para operaciones de BD
        """
        self.db = db_session
    
    def create(self, hotel_data: HotelCreate) -> Hotel:
        """
        Crea un nuevo hotel en la base de datos
        
        Args:
            hotel_data (HotelCreate): Datos del hotel a crear
            
        Returns:
            Hotel: Objeto Hotel creado con ID asignado
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            # Crear objeto Hotel desde los datos del schema
            db_hotel = Hotel(
                nombre=hotel_data.nombre,
                direccion=hotel_data.direccion,
                id_pais=hotel_data.id_pais,
                id_estado=hotel_data.id_estado,
                codigo_postal=hotel_data.codigo_postal,
                telefono=hotel_data.telefono,
                email_contacto=hotel_data.email_contacto,
                numero_estrellas=hotel_data.numero_estrellas,
                estatus_id=self.__status_active__
            )
            
            # Agregar a la sesión
            self.db.add(db_hotel)
            
            # Hacer commit para guardar en BD
            self.db.commit()
            
            # Refrescar para obtener el ID generado
            self.db.refresh(db_hotel)
            
            return db_hotel
            
        except SQLAlchemyError as e:
            # Revertir cambios en caso de error
            self.db.rollback()
            raise e
    
    def get_by_id(self, hotel_id: int) -> Optional[Hotel]:
        """
        Obtiene un hotel por su ID
        
        Args:
            hotel_id (int): ID del hotel a buscar
            
        Returns:
            Optional[Hotel]: Hotel encontrado o None si no existe
        """
        try:
            return self.db.query(Hotel).filter(Hotel.id_hotel == hotel_id).first()
        except SQLAlchemyError as e:
            raise e
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Hotel]:
        """
        Obtiene todos los hoteles con paginación
        
        Args:
            skip (int): Número de registros a saltar (para paginación)
            limit (int): Número máximo de registros a retornar
            
        Returns:
            List[Hotel]: Lista de hoteles
        """
        try:
            return (
                self.db.query(Hotel)
                .order_by(Hotel.id_hotel.desc())
                .offset(skip)
                .limit(limit)
                .all()
            )
        except SQLAlchemyError as e:
            raise e
    
    def update(self, hotel_id: int, hotel_update: HotelUpdate) -> Optional[Hotel]:
        """
        Actualiza un hotel existente (actualización parcial)
        
        Args:
            hotel_id (int): ID del hotel a actualizar
            hotel_update (HotelUpdate): Datos a actualizar
            
        Returns:
            Optional[Hotel]: Hotel actualizado o None si no existe
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            # Buscar el hotel
            db_hotel = self.get_by_id(hotel_id) # Busca el hotel por su id
            
            if not db_hotel:
                return None
            
            # Actualizar solo los campos que no son None
            update_data = hotel_update.model_dump(exclude_unset=True) # Excluye los campos que no son None
            
            for field, value in update_data.items():
                setattr(db_hotel, field, value) # Actualiza el campo con el valor
            
            # Guardar cambios
            self.db.commit()
            self.db.refresh(db_hotel) # Refresca el hotel
            
            return db_hotel
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def delete(self, hotel_id: int) -> bool:
        """
        Elimina un hotel de la base de datos, baja logicamente el hotel
        
        Args:
            hotel_id (int): ID del hotel a eliminar
            
        Returns:
            bool: True si se eliminó, False si no existe
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            # Buscar el hotel
            db_hotel = self.get_by_id(hotel_id) # Busca el hotel por su id
            
            if not db_hotel:
                return False
            
            # Baja lógica: cambiar estatus a inactivo
            (
                self.db.query(Hotel)
                .filter(Hotel.id_hotel == hotel_id) # Filtra el hotel por su id
                .update({"estatus_id": self.__status_inactive__}) # Actualiza el estatus a inactivo para baja lógica
            ) 
            self.db.commit() # Guarda los cambios   
            
            return True
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def exists(self, hotel_id: int) -> bool:
        """
        Verifica si un hotel existe
        
        Args:
            hotel_id (int): ID del hotel
            
        Returns:
            bool: True si existe, False si no
        """
        try:
            return self.db.query(Hotel).filter(Hotel.id_hotel == hotel_id).count() > 0 # Cuenta el número de hoteles que coinciden con el id
        except SQLAlchemyError as e:
            raise e
    
    def get_by_nombre(self, nombre: str) -> List[Hotel]:
        """
        Busca hoteles por nombre (búsqueda parcial)
        
        Args:
            nombre (str): Nombre o parte del nombre a buscar
            
        Returns:
            List[Hotel]: Lista de hoteles que coinciden
        """
        try:
            return self.db.query(Hotel).filter(
                Hotel.nombre.like(f"%{nombre}%") # Busca el hotel por nombre
            ).order_by(Hotel.id_hotel.asc()).all()
        except SQLAlchemyError as e:
            raise e
    
    def get_by_pais(self, id_pais: int) -> List[Hotel]:
        """
        Obtiene todos los hoteles de un país
        
        Args:
            id_pais (int): ID del país
            
        Returns:
            List[Hotel]: Lista de hoteles del país
        """
        try:
            return self.db.query(Hotel).filter(
                Hotel.id_pais == id_pais # Busca el hotel por país
            ).order_by(Hotel.id_hotel.asc()).all()
        except SQLAlchemyError as e:
            raise e
    
    def get_by_estrellas(self, numero_estrellas: int) -> List[Hotel]:
        """
        Obtiene hoteles por número de estrellas
        
        Args:
            numero_estrellas (int): Número de estrellas (1-5)
            
        Returns:
            List[Hotel]: Lista de hoteles con ese número de estrellas
        """
        try:
            return self.db.query(Hotel).filter(
                Hotel.numero_estrellas == numero_estrellas # Busca el hotel por número de estrellas
            ).order_by(Hotel.id_hotel.asc()).all()
        except SQLAlchemyError as e:
            raise e

