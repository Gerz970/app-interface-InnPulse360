"""
DAO (Data Access Object) para operaciones CRUD de Estado
Maneja todas las interacciones con la base de datos para la entidad Estado
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.catalogos.models import Estado
from schemas.catalogos.estado_schemas import EstadoCreate, EstadoUpdate


class EstadoDAO:
    """
    Clase DAO para manejar operaciones CRUD de Estado en la base de datos
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
    
    def create(self, estado_data: EstadoCreate) -> Estado:
        """
        Crea un nuevo estado en la base de datos
        
        Args:
            estado_data (EstadoCreate): Datos del estado a crear
            
        Returns:
            Estado: Objeto Estado creado con ID asignado
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            # Crear objeto Estado usando **data
            estado_data_dict = estado_data.model_dump()
            estado_data_dict['id_estatus'] = estado_data_dict.get('id_estatus') or self.__status_active__
            db_estado = Estado(**estado_data_dict)
            
            # Agregar a la sesión y hacer commit
            self.db.add(db_estado)
            self.db.commit()
            self.db.refresh(db_estado)
            
            return db_estado
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def get_by_id(self, id_estado: int) -> Optional[Estado]:
        """
        Obtiene un estado por su ID
        
        Args:
            id_estado (int): ID del estado a buscar
            
        Returns:
            Optional[Estado]: Estado encontrado o None si no existe
        """
        try:
            return self.db.query(Estado).filter(
                Estado.id_estado == id_estado
            ).first()
        except SQLAlchemyError as e:
            raise e
    
    def get_by_nombre(self, nombre: str) -> Optional[Estado]:
        """
        Obtiene un estado por su nombre
        
        Args:
            nombre (str): Nombre del estado a buscar
            
        Returns:
            Optional[Estado]: Estado encontrado o None si no existe
        """
        try:
            return self.db.query(Estado).filter(
                Estado.nombre == nombre
            ).first()
        except SQLAlchemyError as e:
            raise e
    
    def get_by_pais(self, id_pais: int) -> List[Estado]:
        """
        Obtiene todos los estados de un país específico
        
        Args:
            id_pais (int): ID del país
            
        Returns:
            List[Estado]: Lista de estados del país
        """
        try:
            return (
                self.db.query(Estado)
                .filter(Estado.id_pais == id_pais)
                .order_by(Estado.id_estado.asc())
                .all()
            )
        except SQLAlchemyError as e:
            raise e
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Estado]:
        """
        Obtiene una lista de estados con paginación
        
        Args:
            skip (int): Número de registros a saltar
            limit (int): Número máximo de registros a retornar
            
        Returns:
            List[Estado]: Lista de estados
        """
        try:
            return (
                self.db.query(Estado)
                .order_by(Estado.id_estado.desc())  # Ordena los registros por id_estado de forma descendente
                .offset(skip)  # Número de registros a saltar
                .limit(limit)  # Número máximo de registros a retornar
                .all()  # Retorna todos los registros
            )
        except SQLAlchemyError as e:
            raise e
    
    def get_active_estados(self, skip: int = 0, limit: int = 100) -> List[Estado]:
        """
        Obtiene una lista de estados activos con paginación
        
        Args:
            skip (int): Número de registros a saltar
            limit (int): Número máximo de registros a retornar
            
        Returns:
            List[Estado]: Lista de estados activos
        """
        try:
            return (
                self.db.query(Estado)
                .filter(Estado.id_estatus == self.__status_active__)
                .order_by(Estado.id_estado.desc())  # Ordena los registros por id_estado de forma descendente
                .offset(skip)  # Número de registros a saltar
                .limit(limit)  # Número máximo de registros a retornar
                .all()  # Retorna todos los registros
            )
        except SQLAlchemyError as e:
            raise e
    
    def update(self, id_estado: int, estado_data: EstadoUpdate) -> Optional[Estado]:
        """
        Actualiza un estado existente
        
        Args:
            id_estado (int): ID del estado a actualizar
            estado_data (EstadoUpdate): Datos actualizados del estado
            
        Returns:
            Optional[Estado]: Estado actualizado o None si no existe
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            # Buscar el estado existente
            db_estado = self.get_by_id(id_estado)
            if not db_estado:
                return None
            
            # Actualizar solo los campos proporcionados
            update_data = estado_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_estado, field, value)
            
            # Hacer commit de los cambios
            self.db.commit()
            self.db.refresh(db_estado)
            
            return db_estado
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def delete_logical(self, id_estado: int) -> bool:
        """
        Eliminación lógica de un estado (cambia estatus a inactivo)
        
        Args:
            id_estado (int): ID del estado a eliminar lógicamente
            
        Returns:
            bool: True si se eliminó correctamente, False si no existe
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            # Buscar el estado existente
            db_estado = self.get_by_id(id_estado)
            if not db_estado:
                return False
            
            # Cambiar estatus a inactivo
            db_estado.id_estatus = self.__status_inactive__
            
            # Hacer commit de los cambios
            self.db.commit()
            
            return True
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def reactivate(self, id_estado: int) -> bool:
        """
        Reactiva un estado (cambia estatus a activo)
        
        Args:
            id_estado (int): ID del estado a reactivar
            
        Returns:
            bool: True si se reactivó correctamente, False si no existe
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            # Buscar el estado existente
            db_estado = self.get_by_id(id_estado)
            if not db_estado:
                return False
            
            # Cambiar estatus a activo
            db_estado.id_estatus = self.__status_active__
            
            # Hacer commit de los cambios
            self.db.commit()
            
            return True
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def exists_by_nombre_in_pais(self, nombre: str, id_pais: int, exclude_id: Optional[int] = None) -> bool:
        """
        Verifica si existe un estado con el nombre especificado en un país
        
        Args:
            nombre (str): Nombre del estado a verificar
            id_pais (int): ID del país
            exclude_id (Optional[int]): ID a excluir de la búsqueda (para updates)
            
        Returns:
            bool: True si existe, False si no
        """
        try:
            query = self.db.query(Estado).filter(
                Estado.nombre == nombre,
                Estado.id_pais == id_pais
            )
            
            if exclude_id:
                query = query.filter(Estado.id_estado != exclude_id)
            
            return query.first() is not None
        except SQLAlchemyError as e:
            raise e
