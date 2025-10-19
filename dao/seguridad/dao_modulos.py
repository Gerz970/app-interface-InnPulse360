"""
DAO (Data Access Object) para operaciones CRUD de Módulos
Maneja todas las interacciones con la base de datos para la entidad Módulos
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.seguridad.modulos_model import Modulos
from schemas.seguridad.modulos_create import ModulosCreate
from schemas.seguridad.modulos_update import ModulosUpdate


class ModulosDAO:
    """
    Clase DAO para manejar operaciones CRUD de Módulos en la base de datos
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
    
    def create(self, modulo_data: ModulosCreate) -> Modulos:
        """
        Crea un nuevo módulo en la base de datos
        
        Args:
            modulo_data (ModulosCreate): Datos del módulo a crear
            
        Returns:
            Modulos: Objeto Módulo creado con ID asignado
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            # Crear objeto Módulo desde los datos del schema
            db_modulo = Modulos(
                nombre=modulo_data.nombre,
                descripcion=modulo_data.descripcion,
                icono=modulo_data.icono,
                ruta=modulo_data.ruta,
                id_estatus=modulo_data.id_estatus
            )
            
            # Agregar a la sesión y hacer commit
            self.db.add(db_modulo)
            self.db.commit()
            self.db.refresh(db_modulo)
            
            return db_modulo
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def get_by_id(self, id_modulo: int) -> Optional[Modulos]:
        """
        Obtiene un módulo por su ID
        
        Args:
            id_modulo (int): ID del módulo a buscar
            
        Returns:
            Optional[Modulos]: Módulo encontrado o None si no existe
        """
        try:
            return self.db.query(Modulos).filter(Modulos.id_modulo == id_modulo).first()
        except SQLAlchemyError as e:
            raise e
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Modulos]:
        """
        Obtiene todos los módulos con paginación
        
        Args:
            skip (int): Número de registros a omitir
            limit (int): Número máximo de registros a retornar
            
        Returns:
            List[Modulos]: Lista de módulos
        """
        try:
            return (
                self.db.query(Modulos)
                .offset(skip)
                .limit(limit)
                .all()
            )
        except SQLAlchemyError as e:
            raise e
    
    def get_active(self, skip: int = 0, limit: int = 100) -> List[Modulos]:
        """
        Obtiene todos los módulos activos
        
        Args:
            skip (int): Número de registros a omitir
            limit (int): Número máximo de registros a retornar
            
        Returns:
            List[Modulos]: Lista de módulos activos
        """
        try:
            return (
                self.db.query(Modulos)
                .filter(Modulos.id_estatus == self.__status_active__)
                .offset(skip)
                .limit(limit)
                .all()
            )
        except SQLAlchemyError as e:
            raise e
    
    def get_by_nombre(self, nombre: str) -> Optional[Modulos]:
        """
        Obtiene un módulo por su nombre
        
        Args:
            nombre (str): Nombre del módulo a buscar
            
        Returns:
            Optional[Modulos]: Módulo encontrado o None si no existe
        """
        try:
            return self.db.query(Modulos).filter(Modulos.nombre == nombre).first()
        except SQLAlchemyError as e:
            raise e
    
    def update(self, id_modulo: int, modulo_data: ModulosUpdate) -> Optional[Modulos]:
        """
        Actualiza un módulo existente
        
        Args:
            id_modulo (int): ID del módulo a actualizar
            modulo_data (ModulosUpdate): Datos a actualizar
            
        Returns:
            Optional[Modulos]: Módulo actualizado o None si no existe
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            # Buscar el módulo existente
            db_modulo = self.get_by_id(id_modulo)
            if not db_modulo:
                return None
            
            # Actualizar solo los campos proporcionados
            update_data = modulo_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_modulo, field, value)
            
            # Hacer commit de los cambios
            self.db.commit()
            self.db.refresh(db_modulo)
            
            return db_modulo
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def delete(self, id_modulo: int) -> bool:
        """
        Elimina un módulo (soft delete cambiando estatus)
        
        Args:
            id_modulo (int): ID del módulo a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False si no existe
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            # Buscar el módulo existente
            db_modulo = self.get_by_id(id_modulo)
            if not db_modulo:
                return False
            
            # Soft delete: cambiar estatus a inactivo
            db_modulo.id_estatus = self.__status_inactive__
            
            # Hacer commit de los cambios
            self.db.commit()
            
            return True
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def hard_delete(self, id_modulo: int) -> bool:
        """
        Elimina físicamente un módulo de la base de datos
        
        Args:
            id_modulo (int): ID del módulo a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False si no existe
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            # Buscar el módulo existente
            db_modulo = self.get_by_id(id_modulo)
            if not db_modulo:
                return False
            
            # Eliminar físicamente
            self.db.delete(db_modulo)
            self.db.commit()
            
            return True
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def exists_by_nombre(self, nombre: str, exclude_id: Optional[int] = None) -> bool:
        """
        Verifica si existe un módulo con el nombre dado
        
        Args:
            nombre (str): Nombre a verificar
            exclude_id (Optional[int]): ID a excluir de la búsqueda (para updates)
            
        Returns:
            bool: True si existe, False si no
        """
        try:
            query = self.db.query(Modulos).filter(Modulos.nombre == nombre)
            
            if exclude_id:
                query = query.filter(Modulos.id_modulo != exclude_id)
            
            return query.first() is not None
            
        except SQLAlchemyError as e:
            raise e
