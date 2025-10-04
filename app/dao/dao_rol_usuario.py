"""
DAO (Data Access Object) para operaciones de asignación de roles a usuarios
Maneja la tabla intermedia entre Usuario y Roles
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_
from models.seguridad.rol_usuario_model import RolUsuario
from models.seguridad.usuario_model import Usuario
from models.seguridad.roles_model import Roles


class RolUsuarioDAO:
    """
    Clase DAO para manejar operaciones de asignación de roles a usuarios
    Utiliza SQLAlchemy ORM para las operaciones
    """
    
    def __init__(self, db_session: Session):
        """
        Inicializa el DAO con una sesión de base de datos
        
        Args:
            db_session (Session): Sesión de SQLAlchemy para operaciones de BD
        """
        self.db = db_session
    
    def assign_rol_to_usuario(self, usuario_id: int, rol_id: int) -> bool:
        """
        Asigna un rol a un usuario
        
        Args:
            usuario_id (int): ID del usuario
            rol_id (int): ID del rol
            
        Returns:
            bool: True si se asignó correctamente, False si ya existía
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            # Verificar si ya existe la asignación
            existing = self.db.query(RolUsuario).filter(
                and_(
                    RolUsuario.usuario_id == usuario_id,
                    RolUsuario.rol_id == rol_id
                )
            ).first()
            
            if existing:
                return False  # Ya existe la asignación
            
            # Crear nueva asignación
            rol_usuario = RolUsuario(
                usuario_id=usuario_id,
                rol_id=rol_id
            )
            
            self.db.add(rol_usuario)
            self.db.commit()
            
            return True
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def remove_rol_from_usuario(self, usuario_id: int, rol_id: int) -> bool:
        """
        Remueve un rol de un usuario
        
        Args:
            usuario_id (int): ID del usuario
            rol_id (int): ID del rol
            
        Returns:
            bool: True si se removió correctamente, False si no existía
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            # Buscar la asignación
            rol_usuario = self.db.query(RolUsuario).filter(
                and_(
                    RolUsuario.usuario_id == usuario_id,
                    RolUsuario.rol_id == rol_id
                )
            ).first()
            
            if not rol_usuario:
                return False  # No existe la asignación
            
            # Eliminar la asignación
            self.db.delete(rol_usuario)
            self.db.commit()
            
            return True
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def get_roles_by_usuario(self, usuario_id: int) -> List[Roles]:
        """
        Obtiene todos los roles asignados a un usuario
        
        Args:
            usuario_id (int): ID del usuario
            
        Returns:
            List[Roles]: Lista de roles asignados al usuario
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            return (
                self.db.query(Roles)
                .join(RolUsuario, Roles.id_rol == RolUsuario.rol_id)
                .filter(RolUsuario.usuario_id == usuario_id)
                .filter(Roles.estatus_id == 1)  # Solo roles activos
                .order_by(Roles.id_rol.asc())
                .all()
            )
        except SQLAlchemyError as e:
            raise e
    
    def get_usuarios_by_rol(self, rol_id: int) -> List[Usuario]:
        """
        Obtiene todos los usuarios que tienen un rol específico
        
        Args:
            rol_id (int): ID del rol
            
        Returns:
            List[Usuario]: Lista de usuarios con el rol
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            return (
                self.db.query(Usuario)
                .join(RolUsuario, Usuario.id_usuario == RolUsuario.usuario_id)
                .filter(RolUsuario.rol_id == rol_id)
                .filter(Usuario.estatus_id == 1)  # Solo usuarios activos
                .order_by(Usuario.id_usuario.asc())
                .all()
            )
        except SQLAlchemyError as e:
            raise e
    
    def get_all_assignments(self, skip: int = 0, limit: int = 100) -> List[RolUsuario]:
        """
        Obtiene todas las asignaciones de roles con paginación
        
        Args:
            skip (int): Número de registros a saltar
            limit (int): Número máximo de registros a retornar
            
        Returns:
            List[RolUsuario]: Lista de asignaciones
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            return (
                self.db.query(RolUsuario)
                .offset(skip)
                .limit(limit)
                .all()
            )
        except SQLAlchemyError as e:
            raise e
    
    def bulk_assign_roles_to_usuario(self, usuario_id: int, roles_ids: List[int]) -> int:
        """
        Asigna múltiples roles a un usuario (solo los que no estén ya asignados)
        
        Args:
            usuario_id (int): ID del usuario
            roles_ids (List[int]): Lista de IDs de roles
            
        Returns:
            int: Número de roles asignados exitosamente
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            assigned_count = 0
            
            for rol_id in roles_ids:
                # Verificar si ya existe la asignación
                existing = self.db.query(RolUsuario).filter(
                    and_(
                        RolUsuario.usuario_id == usuario_id,
                        RolUsuario.rol_id == rol_id
                    )
                ).first()
                
                if not existing:
                    # Crear nueva asignación
                    rol_usuario = RolUsuario(
                        usuario_id=usuario_id,
                        rol_id=rol_id
                    )
                    self.db.add(rol_usuario)
                    assigned_count += 1
            
            self.db.commit()
            return assigned_count
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def bulk_remove_roles_from_usuario(self, usuario_id: int, roles_ids: List[int]) -> int:
        """
        Remueve múltiples roles de un usuario
        
        Args:
            usuario_id (int): ID del usuario
            roles_ids (List[int]): Lista de IDs de roles
            
        Returns:
            int: Número de roles removidos exitosamente
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            removed_count = 0
            
            for rol_id in roles_ids:
                # Buscar la asignación
                rol_usuario = self.db.query(RolUsuario).filter(
                    and_(
                        RolUsuario.usuario_id == usuario_id,
                        RolUsuario.rol_id == rol_id
                    )
                ).first()
                
                if rol_usuario:
                    # Eliminar la asignación
                    self.db.delete(rol_usuario)
                    removed_count += 1
            
            self.db.commit()
            return removed_count
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def exists_assignment(self, usuario_id: int, rol_id: int) -> bool:
        """
        Verifica si existe una asignación entre usuario y rol
        
        Args:
            usuario_id (int): ID del usuario
            rol_id (int): ID del rol
            
        Returns:
            bool: True si existe la asignación, False si no
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            return (
                self.db.query(RolUsuario)
                .filter(
                    and_(
                        RolUsuario.usuario_id == usuario_id,
                        RolUsuario.rol_id == rol_id
                    )
                )
                .first() is not None
            )
        except SQLAlchemyError as e:
            raise e
