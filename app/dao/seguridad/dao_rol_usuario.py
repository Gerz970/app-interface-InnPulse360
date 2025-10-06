"""
DAO (Data Access Object) para operaciones de asignación de roles a usuarios
Maneja la tabla intermedia entre Usuario y Roles usando SQL directo
"""

from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_, select, insert, delete
from models.seguridad.roles_model import rol_usuario
from models.seguridad.usuario_model import Usuario
from models.seguridad.roles_model import Roles
from schemas.seguridad.roles_asignacion_response import RolesAsignacionResponse


class RolUsuarioDAO:
    """
    Clase DAO para manejar operaciones de asignación de roles a usuarios
    Utiliza SQL directo para operaciones con la tabla de asociación
    """
    
    def __init__(self, db: Session):
        """
        Inicializa el DAO con una sesión de base de datos
        
        Args:
            db (Session): Sesión de SQLAlchemy
        """
        self.db = db
    
    def assign_role_to_user(self, usuario_id: int, rol_id: int) -> bool:
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
            existing = self.db.execute(
                select(rol_usuario).where(
                    and_(
                        rol_usuario.c.usuario_id == usuario_id,
                        rol_usuario.c.rol_id == rol_id
                    )
                )
            ).first()
            
            if existing:
                return False  # Ya existe la asignación
            
            # Crear nueva asignación
            self.db.execute(
                insert(rol_usuario).values(
                    usuario_id=usuario_id,
                    rol_id=rol_id
                )
            )
            self.db.commit()
            return True
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def remove_role_from_user(self, usuario_id: int, rol_id: int) -> bool:
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
            result = self.db.execute(
                delete(rol_usuario).where(
                    and_(
                        rol_usuario.c.usuario_id == usuario_id,
                        rol_usuario.c.rol_id == rol_id
                    )
                )
            )
            
            if result.rowcount > 0:
                self.db.commit()
                return True
            else:
                return False  # No existía la asignación
                
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def get_user_roles(self, usuario_id: int) -> List[Roles]:
        """
        Obtiene todos los roles asignados a un usuario
        
        Args:
            usuario_id (int): ID del usuario
            
        Returns:
            List[Roles]: Lista de roles del usuario
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            return (
                self.db.query(Roles)
                .join(rol_usuario, Roles.id_rol == rol_usuario.c.rol_id)
                .filter(rol_usuario.c.usuario_id == usuario_id)
                .filter(Roles.estatus_id == 1)  # Solo roles activos
                .order_by(Roles.id_rol.asc())
                .all()
            )
        except SQLAlchemyError as e:
            raise e
    
    def get_role_users(self, rol_id: int) -> List[Usuario]:
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
                .join(rol_usuario, Usuario.id_usuario == rol_usuario.c.usuario_id)
                .filter(rol_usuario.c.rol_id == rol_id)
                .filter(Usuario.estatus_id == 1)  # Solo usuarios activos
                .order_by(Usuario.id_usuario.asc())
                .all()
            )
        except SQLAlchemyError as e:
            raise e
    
    def get_all_assignments(self, skip: int = 0, limit: int = 100) -> List[RolesAsignacionResponse]:
        """
        Obtiene todas las asignaciones de roles con paginación
        
        Args:
            skip (int): Número de registros a saltar
            limit (int): Número máximo de registros a retornar
            
        Returns:
            List[RolesAsignacionResponse]: Lista de asignaciones con información de usuario y rol
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            assignments = (
                self.db.query(
                    rol_usuario.c.usuario_id,
                    rol_usuario.c.rol_id,
                    Usuario.login,
                    Usuario.correo_electronico,
                    Roles.rol,
                    Roles.descripcion
                )
                .join(Usuario, rol_usuario.c.usuario_id == Usuario.id_usuario)
                .join(Roles, rol_usuario.c.rol_id == Roles.id_rol)
                .offset(skip)
                .limit(limit)
                .all()
            )
            
            return [
                RolesAsignacionResponse(
                    usuario_id=assignment.id_usuario,
                    rol_id=assignment.rol_id,
                    usuario_login=assignment.login,
                    usuario_email=assignment.correo_electronico,
                    rol_nombre=assignment.rol,
                    rol_descripcion=assignment.descripcion
                )
                for assignment in assignments
            ]
        except SQLAlchemyError as e:
            raise e
    
    def assign_multiple_roles_to_user(self, usuario_id: int, roles_ids: List[int]) -> int:
        """
        Asigna múltiples roles a un usuario
        
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
                existing = self.db.execute(
                    select(rol_usuario).where(
                        and_(
                            rol_usuario.c.usuario_id == usuario_id,
                            rol_usuario.c.rol_id == rol_id
                        )
                    )
                ).first()
                
                if not existing:
                    # Crear nueva asignación
                    self.db.execute(
                        insert(rol_usuario).values(
                            usuario_id=usuario_id,
                            rol_id=rol_id
                        )
                    )
                    assigned_count += 1
            
            self.db.commit()
            return assigned_count
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def remove_multiple_roles_from_user(self, usuario_id: int, roles_ids: List[int]) -> int:
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
                result = self.db.execute(
                    delete(rol_usuario).where(
                        and_(
                            rol_usuario.c.usuario_id == usuario_id,
                            rol_usuario.c.rol_id == rol_id
                        )
                    )
                )
                if result.rowcount > 0:
                    removed_count += 1
            
            self.db.commit()
            return removed_count
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def has_role(self, usuario_id: int, rol_id: int) -> bool:
        """
        Verifica si un usuario tiene un rol específico
        
        Args:
            usuario_id (int): ID del usuario
            rol_id (int): ID del rol
            
        Returns:
            bool: True si el usuario tiene el rol, False en caso contrario
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            result = self.db.execute(
                select(rol_usuario).where(
                    and_(
                        rol_usuario.c.usuario_id == usuario_id,
                        rol_usuario.c.rol_id == rol_id
                    )
                )
            ).first()
            
            return result is not None
            
        except SQLAlchemyError as e:
            raise e
