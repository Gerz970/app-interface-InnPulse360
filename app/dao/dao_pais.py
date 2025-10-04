"""
DAO (Data Access Object) para operaciones CRUD de País
Maneja todas las interacciones con la base de datos para la entidad País
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.catalogos.models import Pais
from schemas.catalogos.pais_schemas import PaisCreate, PaisUpdate


class PaisDAO:
    """
    Clase DAO para manejar operaciones CRUD de País en la base de datos
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
    
    def create(self, pais_data: PaisCreate) -> Pais:
        """
        Crea un nuevo país en la base de datos
        
        Args:
            pais_data (PaisCreate): Datos del país a crear
            
        Returns:
            Pais: Objeto País creado con ID asignado
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            # Crear objeto País desde los datos del schema
            db_pais = Pais(
                nombre=pais_data.nombre,
                id_estatus=pais_data.id_estatus or self.__status_active__
            )
            
            # Agregar a la sesión y hacer commit
            self.db.add(db_pais)
            self.db.commit()
            self.db.refresh(db_pais)
            
            return db_pais
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def get_by_id(self, id_pais: int) -> Optional[Pais]:
        """
        Obtiene un país por su ID
        
        Args:
            id_pais (int): ID del país a buscar
            
        Returns:
            Optional[Pais]: País encontrado o None si no existe
        """
        try:
            return self.db.query(Pais).filter(
                Pais.id_pais == id_pais
            ).first()
        except SQLAlchemyError as e:
            raise e
    
    def get_by_nombre(self, nombre: str) -> Optional[Pais]:
        """
        Obtiene un país por su nombre
        
        Args:
            nombre (str): Nombre del país a buscar
            
        Returns:
            Optional[Pais]: País encontrado o None si no existe
        """
        try:
            return self.db.query(Pais).filter(
                Pais.nombre == nombre
            ).first()
        except SQLAlchemyError as e:
            raise e
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Pais]:
        """
        Obtiene una lista de países con paginación
        
        Args:
            skip (int): Número de registros a saltar
            limit (int): Número máximo de registros a retornar
            
        Returns:
            List[Pais]: Lista de países
        """
        try:
            return (
                self.db.query(Pais)
                .order_by(Pais.id_pais.desc())  # Ordena los registros por id_pais de forma descendente
                .offset(skip)  # Número de registros a saltar
                .limit(limit)  # Número máximo de registros a retornar
                .all()  # Retorna todos los registros
            )
        except SQLAlchemyError as e:
            raise e
    
    def get_active_paises(self, skip: int = 0, limit: int = 100) -> List[Pais]:
        """
        Obtiene una lista de países activos con paginación
        
        Args:
            skip (int): Número de registros a saltar
            limit (int): Número máximo de registros a retornar
            
        Returns:
            List[Pais]: Lista de países activos
        """
        try:
            return (
                self.db.query(Pais)
                .filter(Pais.id_estatus == self.__status_active__)
                .order_by(Pais.id_pais.desc())  # Ordena los registros por id_pais de forma descendente
                .offset(skip)  # Número de registros a saltar
                .limit(limit)  # Número máximo de registros a retornar
                .all()  # Retorna todos los registros
            )
        except SQLAlchemyError as e:
            raise e
    
    def update(self, id_pais: int, pais_data: PaisUpdate) -> Optional[Pais]:
        """
        Actualiza un país existente
        
        Args:
            id_pais (int): ID del país a actualizar
            pais_data (PaisUpdate): Datos actualizados del país
            
        Returns:
            Optional[Pais]: País actualizado o None si no existe
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            # Buscar el país existente
            db_pais = self.get_by_id(id_pais)
            if not db_pais:
                return None
            
            # Actualizar solo los campos proporcionados
            update_data = pais_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_pais, field, value)
            
            # Hacer commit de los cambios
            self.db.commit()
            self.db.refresh(db_pais)
            
            return db_pais
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def delete_logical(self, id_pais: int) -> bool:
        """
        Eliminación lógica de un país (cambia estatus a inactivo)
        
        Args:
            id_pais (int): ID del país a eliminar lógicamente
            
        Returns:
            bool: True si se eliminó correctamente, False si no existe
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            # Buscar el país existente
            db_pais = self.get_by_id(id_pais)
            if not db_pais:
                return False
            
            # Cambiar estatus a inactivo
            db_pais.id_estatus = self.__status_inactive__
            
            # Hacer commit de los cambios
            self.db.commit()
            
            return True
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def reactivate(self, id_pais: int) -> bool:
        """
        Reactiva un país (cambia estatus a activo)
        
        Args:
            id_pais (int): ID del país a reactivar
            
        Returns:
            bool: True si se reactivó correctamente, False si no existe
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            # Buscar el país existente
            db_pais = self.get_by_id(id_pais)
            if not db_pais:
                return False
            
            # Cambiar estatus a activo
            db_pais.id_estatus = self.__status_active__
            
            # Hacer commit de los cambios
            self.db.commit()
            
            return True
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def exists_by_nombre(self, nombre: str, exclude_id: Optional[int] = None) -> bool:
        """
        Verifica si existe un país con el nombre especificado
        
        Args:
            nombre (str): Nombre del país a verificar
            exclude_id (Optional[int]): ID a excluir de la búsqueda (para updates)
            
        Returns:
            bool: True si existe, False si no
        """
        try:
            query = self.db.query(Pais).filter(Pais.nombre == nombre)
            
            if exclude_id:
                query = query.filter(Pais.id_pais != exclude_id)
            
            return query.first() is not None
        except SQLAlchemyError as e:
            raise e
