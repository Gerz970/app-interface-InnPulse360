"""
DAO (Data Access Object) para operaciones CRUD de Caracteristica
Maneja todas las interacciones con la base de datos para la entidad Caracteristica
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.catalogos.models import Caracteristica
from schemas.catalogos.caracteristica_schemas import CaracteristicaCreate, CaracteristicaUpdate


class CaracteristicaDAO:
    """
    Clase DAO para manejar operaciones CRUD de Caracteristica en la base de datos
    Utiliza SQLAlchemy ORM para las operaciones
    """
    
    def __init__(self, db_session: Session):
        """
        Inicializa el DAO con una sesión de base de datos
        
        Args:
            db_session (Session): Sesión de SQLAlchemy para operaciones de BD
        """
        self.db = db_session
    
    def create(self, caracteristica_data: CaracteristicaCreate) -> Caracteristica:
        """
        Crea una nueva característica en la base de datos
        
        Args:
            caracteristica_data (CaracteristicaCreate): Datos de la característica a crear
            
        Returns:
            Caracteristica: Objeto Caracteristica creado con ID asignado
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            # Crear objeto Caracteristica desde los datos del schema
            db_caracteristica = Caracteristica(
                caracteristica=caracteristica_data.caracteristica,
                descripcion=caracteristica_data.descripcion
            )
            
            # Agregar a la sesión y hacer commit
            self.db.add(db_caracteristica)
            self.db.commit()
            self.db.refresh(db_caracteristica)
            
            return db_caracteristica
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def get_by_id(self, id_caracteristica: int) -> Optional[Caracteristica]:
        """
        Obtiene una característica por su ID
        
        Args:
            id_caracteristica (int): ID de la característica a buscar
            
        Returns:
            Optional[Caracteristica]: Caracteristica encontrada o None si no existe
        """
        try:
            return self.db.query(Caracteristica).filter(
                Caracteristica.id_caracteristica == id_caracteristica
            ).first()
        except SQLAlchemyError as e:
            raise e
    
    def get_by_nombre(self, caracteristica: str) -> Optional[Caracteristica]:
        """
        Obtiene una característica por su nombre
        
        Args:
            caracteristica (str): Nombre de la característica a buscar
            
        Returns:
            Optional[Caracteristica]: Caracteristica encontrada o None si no existe
        """
        try:
            return self.db.query(Caracteristica).filter(
                Caracteristica.caracteristica == caracteristica
            ).first()
        except SQLAlchemyError as e:
            raise e
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Caracteristica]:
        """
        Obtiene una lista de características con paginación
        
        Args:
            skip (int): Número de registros a saltar
            limit (int): Número máximo de registros a retornar
            
        Returns:
            List[Caracteristica]: Lista de características
        """
        try:
            return (
                self.db.query(Caracteristica)
                .order_by(Caracteristica.id_caracteristica.desc())  # Ordena los registros por id_caracteristica de forma descendente
                .offset(skip)  # Número de registros a saltar
                .limit(limit)  # Número máximo de registros a retornar
                .all()  # Retorna todos los registros
            )
        except SQLAlchemyError as e:
            raise e
    
    def update(self, id_caracteristica: int, caracteristica_data: CaracteristicaUpdate) -> Optional[Caracteristica]:
        """
        Actualiza una característica existente
        
        Args:
            id_caracteristica (int): ID de la característica a actualizar
            caracteristica_data (CaracteristicaUpdate): Datos actualizados de la característica
            
        Returns:
            Optional[Caracteristica]: Caracteristica actualizada o None si no existe
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            # Buscar la característica existente
            db_caracteristica = self.get_by_id(id_caracteristica)
            if not db_caracteristica:
                return None
            
            # Actualizar solo los campos proporcionados
            update_data = caracteristica_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_caracteristica, field, value)
            
            # Hacer commit de los cambios
            self.db.commit()
            self.db.refresh(db_caracteristica)
            
            return db_caracteristica
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def delete(self, id_caracteristica: int) -> bool:
        """
        Elimina una característica de la base de datos
        
        Args:
            id_caracteristica (int): ID de la característica a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False si no existe
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            # Buscar la característica existente
            db_caracteristica = self.get_by_id(id_caracteristica)
            if not db_caracteristica:
                return False
            
            # Eliminar la característica
            self.db.delete(db_caracteristica)
            self.db.commit()
            
            return True
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def exists_by_nombre(self, caracteristica: str, exclude_id: Optional[int] = None) -> bool:
        """
        Verifica si existe una característica con el nombre especificado
        
        Args:
            caracteristica (str): Nombre de la característica a verificar
            exclude_id (Optional[int]): ID a excluir de la búsqueda (para updates)
            
        Returns:
            bool: True si existe, False si no
        """
        try:
            query = self.db.query(Caracteristica).filter(Caracteristica.caracteristica == caracteristica)
            
            if exclude_id:
                query = query.filter(Caracteristica.id_caracteristica != exclude_id)
            
            return query.first() is not None
        except SQLAlchemyError as e:
            raise e
