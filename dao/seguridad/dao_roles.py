"""
DAO (Data Access Object) para operaciones CRUD de Roles
Maneja todas las interacciones con la base de datos para la entidad Roles
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.seguridad.roles_model import Roles
from schemas.seguridad.roles_create import RolesCreate
from schemas.seguridad.roles_update import RolesUpdate


class RolesDAO:
    """
    Clase DAO para manejar operaciones CRUD de Roles en la base de datos
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
    
    def create(self, roles_data: RolesCreate) -> Roles:
        """
        Crea un nuevo rol en la base de datos
        
        Args:
            roles_data (RolesCreate): Datos del rol a crear
            
        Returns:
            Roles: Objeto Roles creado con ID asignado
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            # Crear objeto Roles desde los datos del schema
            db_roles = Roles(
                rol=roles_data.rol,
                descripcion=roles_data.descripcion,
                estatus_id=roles_data.estatus_id or self.__status_active__
            )
            
            # Agregar a la sesión y hacer commit
            self.db.add(db_roles)
            self.db.commit()
            self.db.refresh(db_roles)
            
            return db_roles
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def get_by_id(self, id_rol: int) -> Optional[Roles]:
        """
        Obtiene un rol por su ID
        
        Args:
            id_rol (int): ID del rol a buscar
            
        Returns:
            Optional[Roles]: Rol encontrado o None si no existe
        """
        try:
            return self.db.query(Roles).filter(
                Roles.id_rol == id_rol
            ).first()
        except SQLAlchemyError as e:
            raise e
    
    def get_by_rol(self, rol: str) -> Optional[Roles]:
        """
        Obtiene un rol por su nombre
        
        Args:
            rol (str): Nombre del rol a buscar
            
        Returns:
            Optional[Roles]: Rol encontrado o None si no existe
        """
        try:
            return self.db.query(Roles).filter(
                Roles.rol == rol
            ).first()
        except SQLAlchemyError as e:
            raise e
    
    def get_by_nombre(self, nombre: str) -> Optional[Roles]:
        """
        Alias de get_by_rol para mantener consistencia con otros DAOs
        
        Args:
            nombre (str): Nombre del rol a buscar
            
        Returns:
            Optional[Roles]: Rol encontrado o None si no existe
        """
        return self.get_by_rol(nombre)
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Roles]:
        """
        Obtiene una lista de roles con paginación
        
        Args:
            skip (int): Número de registros a saltar
            limit (int): Número máximo de registros a retornar
            
        Returns:
            List[Roles]: Lista de roles
        """
        try:
            return (
                self.db.query(Roles)
                .order_by(Roles.id_rol.desc())  # Ordena los registros por id_rol de forma descendente
                .offset(skip)  # Número de registros a saltar
                .limit(limit)  # Número máximo de registros a retornar
                .all()  # Retorna todos los registros
            )
        except SQLAlchemyError as e:
            raise e
    
    def get_active_roles(self, skip: int = 0, limit: int = 100) -> List[Roles]:
        """
        Obtiene una lista de roles activos con paginación
        
        Args:
            skip (int): Número de registros a saltar
            limit (int): Número máximo de registros a retornar
            
        Returns:
            List[Roles]: Lista de roles activos
        """
        try:
            return (
                self.db.query(Roles)
                .filter(Roles.estatus_id == self.__status_active__)
                .order_by(Roles.id_rol.desc())  # Ordena los registros por id_rol de forma descendente
                .offset(skip)  # Número de registros a saltar
                .limit(limit)  # Número máximo de registros a retornar
                .all()  # Retorna todos los registros
            )
        except SQLAlchemyError as e:
            raise e
    
    def update(self, id_rol: int, roles_data: RolesUpdate) -> Optional[Roles]:
        """
        Actualiza un rol existente
        
        Args:
            id_rol (int): ID del rol a actualizar
            roles_data (RolesUpdate): Datos actualizados del rol
            
        Returns:
            Optional[Roles]: Rol actualizado o None si no existe
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            # Buscar el rol existente
            db_roles = self.get_by_id(id_rol)
            if not db_roles:
                return None
            
            # Actualizar solo los campos proporcionados
            update_data = roles_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_roles, field, value)
            
            # Hacer commit de los cambios
            self.db.commit()
            self.db.refresh(db_roles)
            
            return db_roles
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def delete_logical(self, id_rol: int) -> bool:
        """
        Eliminación lógica de un rol (cambia estatus a inactivo)
        
        Args:
            id_rol (int): ID del rol a eliminar lógicamente
            
        Returns:
            bool: True si se eliminó correctamente, False si no existe
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            # Buscar el rol existente
            db_roles = self.get_by_id(id_rol)
            if not db_roles:
                return False
            
            # Cambiar estatus a inactivo
            db_roles.estatus_id = self.__status_inactive__
            
            # Hacer commit de los cambios
            self.db.commit()
            
            return True
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def reactivate(self, id_rol: int) -> bool:
        """
        Reactiva un rol (cambia estatus a activo)
        
        Args:
            id_rol (int): ID del rol a reactivar
            
        Returns:
            bool: True si se reactivó correctamente, False si no existe
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            # Buscar el rol existente
            db_roles = self.get_by_id(id_rol)
            if not db_roles:
                return False
            
            # Cambiar estatus a activo
            db_roles.estatus_id = self.__status_active__
            
            # Hacer commit de los cambios
            self.db.commit()
            
            return True
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def exists_by_rol(self, rol: str, exclude_id: Optional[int] = None) -> bool:
        """
        Verifica si existe un rol con el nombre especificado
        
        Args:
            rol (str): Nombre del rol a verificar
            exclude_id (Optional[int]): ID a excluir de la búsqueda (para updates)
            
        Returns:
            bool: True si existe, False si no
        """
        try:
            query = self.db.query(Roles).filter(Roles.rol == rol)
            
            if exclude_id:
                query = query.filter(Roles.id_rol != exclude_id)
            
            return query.first() is not None
        except SQLAlchemyError as e:
            raise e
