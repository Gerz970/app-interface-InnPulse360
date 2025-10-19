"""
DAO (Data Access Object) para operaciones CRUD de TipoHabitacion
Maneja todas las interacciones con la base de datos para la entidad TipoHabitacion
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.hotel.tipo_habitacion_model import TipoHabitacion
from schemas.hotel.tipo_habitacion_schemas import TipoHabitacionCreate, TipoHabitacionUpdate


class TipoHabitacionDAO:
    """
    Clase DAO para manejar operaciones CRUD de TipoHabitacion en la base de datos
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
    
    def create(self, tipo_habitacion_data: TipoHabitacionCreate) -> TipoHabitacion:
        """
        Crea un nuevo tipo de habitación en la base de datos
        
        Args:
            tipo_habitacion_data (TipoHabitacionCreate): Datos del tipo de habitación a crear
            
        Returns:
            TipoHabitacion: Objeto TipoHabitacion creado con ID asignado
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            # Crear objeto TipoHabitacion desde los datos del schema
            db_tipo_habitacion = TipoHabitacion(
                clave=tipo_habitacion_data.clave,
                tipo_habitacion=tipo_habitacion_data.tipo_habitacion,
                estatus_id=tipo_habitacion_data.estatus_id or self.__status_active__
            )
            
            # Agregar a la sesión y hacer commit
            self.db.add(db_tipo_habitacion)
            self.db.commit()
            self.db.refresh(db_tipo_habitacion)
            
            return db_tipo_habitacion
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def get_by_id(self, id_tipoHabitacion: int) -> Optional[TipoHabitacion]:
        """
        Obtiene un tipo de habitación por su ID
        
        Args:
            id_tipoHabitacion (int): ID del tipo de habitación a buscar
            
        Returns:
            Optional[TipoHabitacion]: TipoHabitacion encontrado o None si no existe
        """
        try:
            return self.db.query(TipoHabitacion).filter(
                TipoHabitacion.id_tipoHabitacion == id_tipoHabitacion
            ).first()
        except SQLAlchemyError as e:
            raise e
    
    def get_by_clave(self, clave: str) -> Optional[TipoHabitacion]:
        """
        Obtiene un tipo de habitación por su clave
        
        Args:
            clave (str): Clave del tipo de habitación a buscar
            
        Returns:
            Optional[TipoHabitacion]: TipoHabitacion encontrado o None si no existe
        """
        try:
            return self.db.query(TipoHabitacion).filter(
                TipoHabitacion.clave == clave
            ).first()
        except SQLAlchemyError as e:
            raise e
    
    def get_by_nombre(self, tipo_habitacion: str) -> Optional[TipoHabitacion]:
        """
        Obtiene un tipo de habitación por su nombre
        
        Args:
            tipo_habitacion (str): Nombre del tipo de habitación a buscar
            
        Returns:
            Optional[TipoHabitacion]: TipoHabitacion encontrado o None si no existe
        """
        try:
            return self.db.query(TipoHabitacion).filter(
                TipoHabitacion.tipo_habitacion == tipo_habitacion
            ).first()
        except SQLAlchemyError as e:
            raise e
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[TipoHabitacion]:
        """
        Obtiene una lista de tipos de habitación con paginación
        
        Args:
            skip (int): Número de registros a saltar
            limit (int): Número máximo de registros a retornar
            
        Returns:
            List[TipoHabitacion]: Lista de tipos de habitación
        """
        try:
            return (
                self.db.query(TipoHabitacion)
                .order_by(TipoHabitacion.id_tipoHabitacion.desc())  # Ordena los registros por id_tipoHabitacion de forma descendente
                .offset(skip)  # Número de registros a saltar
                .limit(limit)  # Número máximo de registros a retornar
                .all()  # Retorna todos los registros
            )
        except SQLAlchemyError as e:
            raise e
    
    def get_active_tipos_habitacion(self, skip: int = 0, limit: int = 100) -> List[TipoHabitacion]:
        """
        Obtiene una lista de tipos de habitación activos con paginación
        
        Args:
            skip (int): Número de registros a saltar
            limit (int): Número máximo de registros a retornar
            
        Returns:
            List[TipoHabitacion]: Lista de tipos de habitación activos
        """
        try:
            return (
                self.db.query(TipoHabitacion)
                .filter(TipoHabitacion.estatus_id == self.__status_active__)
                .order_by(TipoHabitacion.id_tipoHabitacion.desc())  # Ordena los registros por id_tipoHabitacion de forma descendente
                .offset(skip)  # Número de registros a saltar
                .limit(limit)  # Número máximo de registros a retornar
                .all()  # Retorna todos los registros
            )
        except SQLAlchemyError as e:
            raise e
    
    def update(self, id_tipoHabitacion: int, tipo_habitacion_data: TipoHabitacionUpdate) -> Optional[TipoHabitacion]:
        """
        Actualiza un tipo de habitación existente
        
        Args:
            id_tipoHabitacion (int): ID del tipo de habitación a actualizar
            tipo_habitacion_data (TipoHabitacionUpdate): Datos actualizados del tipo de habitación
            
        Returns:
            Optional[TipoHabitacion]: TipoHabitacion actualizado o None si no existe
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            # Buscar el tipo de habitación existente
            db_tipo_habitacion = self.get_by_id(id_tipoHabitacion)
            if not db_tipo_habitacion:
                return None
            
            # Actualizar solo los campos proporcionados
            update_data = tipo_habitacion_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_tipo_habitacion, field, value)
            
            # Hacer commit de los cambios
            self.db.commit()
            self.db.refresh(db_tipo_habitacion)
            
            return db_tipo_habitacion
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def delete_logical(self, id_tipoHabitacion: int) -> bool:
        """
        Eliminación lógica de un tipo de habitación (cambia estatus a inactivo)
        
        Args:
            id_tipoHabitacion (int): ID del tipo de habitación a eliminar lógicamente
            
        Returns:
            bool: True si se eliminó correctamente, False si no existe
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            # Buscar el tipo de habitación existente
            db_tipo_habitacion = self.get_by_id(id_tipoHabitacion)
            if not db_tipo_habitacion:
                return False
            
            # Cambiar estatus a inactivo
            db_tipo_habitacion.estatus_id = self.__status_inactive__
            
            # Hacer commit de los cambios
            self.db.commit()
            
            return True
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def reactivate(self, id_tipoHabitacion: int) -> bool:
        """
        Reactiva un tipo de habitación (cambia estatus a activo)
        
        Args:
            id_tipoHabitacion (int): ID del tipo de habitación a reactivar
            
        Returns:
            bool: True si se reactivó correctamente, False si no existe
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            # Buscar el tipo de habitación existente
            db_tipo_habitacion = self.get_by_id(id_tipoHabitacion)
            if not db_tipo_habitacion:
                return False
            
            # Cambiar estatus a activo
            db_tipo_habitacion.estatus_id = self.__status_active__
            
            # Hacer commit de los cambios
            self.db.commit()
            
            return True
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def exists_by_clave(self, clave: str, exclude_id: Optional[int] = None) -> bool:
        """
        Verifica si existe un tipo de habitación con la clave especificada
        
        Args:
            clave (str): Clave del tipo de habitación a verificar
            exclude_id (Optional[int]): ID a excluir de la búsqueda (para updates)
            
        Returns:
            bool: True si existe, False si no
        """
        try:
            query = self.db.query(TipoHabitacion).filter(TipoHabitacion.clave == clave)
            
            if exclude_id:
                query = query.filter(TipoHabitacion.id_tipoHabitacion != exclude_id)
            
            return query.first() is not None
        except SQLAlchemyError as e:
            raise e
    
    def exists_by_nombre(self, tipo_habitacion: str, exclude_id: Optional[int] = None) -> bool:
        """
        Verifica si existe un tipo de habitación con el nombre especificado
        
        Args:
            tipo_habitacion (str): Nombre del tipo de habitación a verificar
            exclude_id (Optional[int]): ID a excluir de la búsqueda (para updates)
            
        Returns:
            bool: True si existe, False si no
        """
        try:
            query = self.db.query(TipoHabitacion).filter(TipoHabitacion.tipo_habitacion == tipo_habitacion)
            
            if exclude_id:
                query = query.filter(TipoHabitacion.id_tipoHabitacion != exclude_id)
            
            return query.first() is not None
        except SQLAlchemyError as e:
            raise e
