"""
DAO (Data Access Object) para operaciones CRUD de Usuario
Maneja todas las interacciones con la base de datos para la entidad Usuario
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.seguridad.usuario_model import Usuario
from schemas.seguridad.usuario_create import UsuarioCreate
from schemas.seguridad.usuario_update import UsuarioUpdate


class UsuarioDAO:
    """
    Clase DAO para manejar operaciones CRUD de Usuario en la base de datos
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
    
    def create(self, usuario_data: UsuarioCreate) -> Usuario:
        """
        Crea un nuevo usuario en la base de datos
        
        Args:
            usuario_data (UsuarioCreate): Datos del usuario a crear
            
        Returns:
            Usuario: Objeto Usuario creado con ID asignado
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            # Crear objeto Usuario usando **data
            usuario_dict = usuario_data.model_dump()
            usuario_dict['estatus_id'] = usuario_dict.get('estatus_id') or self.__status_active__
            db_usuario = Usuario(**usuario_dict)
            
            # Agregar a la sesión y hacer commit
            self.db.add(db_usuario)
            self.db.commit()
            self.db.refresh(db_usuario)
            
            return db_usuario
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def get_by_id(self, id_usuario: int) -> Optional[Usuario]:
        """
        Obtiene un usuario por su ID
        
        Args:
            id_usuario (int): ID del usuario a buscar
            
        Returns:
            Optional[Usuario]: Usuario encontrado o None si no existe
        """
        try:
            return self.db.query(Usuario).filter(
                Usuario.id_usuario == id_usuario
            ).first()
        except SQLAlchemyError as e:
            raise e
    
    def get_by_login(self, login: str) -> Optional[Usuario]:
        """
        Obtiene un usuario por su login
        
        Args:
            login (str): Login del usuario a buscar
            
        Returns:
            Optional[Usuario]: Usuario encontrado o None si no existe
        """
        try:
            return self.db.query(Usuario).filter(
                Usuario.login == login
            ).first()
        except SQLAlchemyError as e:
            raise e
    
    def get_by_email(self, correo_electronico: str) -> Optional[Usuario]:
        """
        Obtiene un usuario por su correo electrónico
        
        Args:
            correo_electronico (str): Correo electrónico del usuario a buscar
            
        Returns:
            Optional[Usuario]: Usuario encontrado o None si no existe
        """
        try:
            return self.db.query(Usuario).filter(
                Usuario.correo_electronico == correo_electronico
            ).first()
        except SQLAlchemyError as e:
            raise e
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Usuario]:
        """
        Obtiene una lista de usuarios con paginación
        
        Args:
            skip (int): Número de registros a saltar
            limit (int): Número máximo de registros a retornar
            
        Returns:
            List[Usuario]: Lista de usuarios
        """
        try:
            return (
                self.db.query(Usuario)
                    .order_by(Usuario.id_usuario.desc()) # Ordena los registros por id_usuario de forma descendente
                    .offset(skip) # Número de registros a saltar
                    .limit(limit) # Número máximo de registros a retornar
                    .all() # Retorna todos los registros
            )
        except SQLAlchemyError as e:
            raise e
    
    def get_active_users(self, skip: int = 0, limit: int = 100) -> List[Usuario]:
        """
        Obtiene una lista de usuarios activos con paginación
        
        Args:
            skip (int): Número de registros a saltar
            limit (int): Número máximo de registros a retornar
            
        Returns:
            List[Usuario]: Lista de usuarios activos
        """
        try:
            return (
                self.db.query(Usuario).filter(
                Usuario.estatus_id == self.__status_active__
            ).order_by(Usuario.id_usuario.desc()) # Ordena los registros por id_usuario de forma descendente
            .offset(skip) # Número de registros a saltar
            .limit(limit) # Número máximo de registros a retornar
            .all() # Retorna todos los registros
        )
        except SQLAlchemyError as e:
            raise e
    
    def update(self, id_usuario: int, usuario_data: UsuarioUpdate) -> Optional[Usuario]:
        """
        Actualiza un usuario existente
        
        Args:
            id_usuario (int): ID del usuario a actualizar
            usuario_data (UsuarioUpdate): Datos actualizados del usuario
            
        Returns:
            Optional[Usuario]: Usuario actualizado o None si no existe
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            # Buscar el usuario existente
            db_usuario = self.get_by_id(id_usuario)
            if not db_usuario:
                return None
            
            # Actualizar solo los campos proporcionados
            update_data = usuario_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_usuario, field, value)
            
            # Hacer commit de los cambios
            self.db.commit()
            self.db.refresh(db_usuario)
            
            return db_usuario
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def delete_logical(self, id_usuario: int) -> bool:
        """
        Eliminación lógica de un usuario (cambia estatus a inactivo)
        
        Args:
            id_usuario (int): ID del usuario a eliminar lógicamente
            
        Returns:
            bool: True si se eliminó correctamente, False si no existe
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            # Buscar el usuario existente
            db_usuario = self.get_by_id(id_usuario)
            if not db_usuario:
                return False
            
            # Cambiar estatus a inactivo
            db_usuario.estatus_id = self.__status_inactive__
            
            # Hacer commit de los cambios
            self.db.commit()
            
            return True
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def reactivate(self, id_usuario: int) -> bool:
        """
        Reactiva un usuario (cambia estatus a activo)
        
        Args:
            id_usuario (int): ID del usuario a reactivar
            
        Returns:
            bool: True si se reactivó correctamente, False si no existe
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            # Buscar el usuario existente
            db_usuario = self.get_by_id(id_usuario)
            if not db_usuario:
                return False
            
            # Cambiar estatus a activo
            db_usuario.estatus_id = self.__status_active__
            
            # Hacer commit de los cambios
            self.db.commit()
            
            return True
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def exists_by_login(self, login: str, exclude_id: Optional[int] = None) -> bool:
        """
        Verifica si existe un usuario con el login especificado
        
        Args:
            login (str): Login a verificar
            exclude_id (Optional[int]): ID a excluir de la búsqueda (para updates)
            
        Returns:
            bool: True si existe, False si no
        """
        try:
            query = self.db.query(Usuario).filter(Usuario.login == login)
            
            if exclude_id:
                query = query.filter(Usuario.id_usuario != exclude_id)
            
            return query.first() is not None
        except SQLAlchemyError as e:
            raise e
    
    def exists_by_email(self, correo_electronico: str, exclude_id: Optional[int] = None) -> bool:
        """
        Verifica si existe un usuario con el correo electrónico especificado
        
        Args:
            correo_electronico (str): Correo electrónico a verificar
            exclude_id (Optional[int]): ID a excluir de la búsqueda (para updates)
            
        Returns:
            bool: True si existe, False si no
        """
        try:
            query = self.db.query(Usuario).filter(Usuario.correo_electronico == correo_electronico)
            
            if exclude_id:
                query = query.filter(Usuario.id_usuario != exclude_id)
            
            return query.first() is not None
        except SQLAlchemyError as e:
            raise e
