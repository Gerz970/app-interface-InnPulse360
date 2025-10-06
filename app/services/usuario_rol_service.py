"""
Servicio para gestión de asignación de roles a usuarios
Maneja la lógica de negocio para la relación Usuario-Roles
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from dao.dao_rol_usuario import RolUsuarioDAO
from dao.dao_usuario import UsuarioDAO
from dao.dao_roles import RolesDAO
from models.seguridad.usuario_model import Usuario
from models.seguridad.roles_model import Roles
from schemas.seguridad.usuario_rol_schemas import UsuarioRolAssign, UsuarioRolBulkAssign, RolSimpleResponse
from schemas.seguridad.usuario_response import UsuarioResponse


class UsuarioRolService:
    """
    Servicio para manejar la lógica de negocio de asignación de roles
    """
    
    def __init__(self, db_session: Session):
        """
        Inicializa el servicio con una sesión de base de datos
        
        Args:
            db_session (Session): Sesión de SQLAlchemy
        """
        self.db = db_session
        self.rol_usuario_dao = RolUsuarioDAO(db_session)
        self.usuario_dao = UsuarioDAO(db_session)
        self.roles_dao = RolesDAO(db_session)
    
    def assign_rol_to_usuario(self, usuario_id: int, rol_id: int) -> bool:
        """
        Asigna un rol a un usuario
        
        Args:
            usuario_id (int): ID del usuario
            rol_id (int): ID del rol
            
        Returns:
            bool: True si se asignó correctamente
            
        Raises:
            HTTPException: Si el usuario o rol no existen, o ya está asignado
        """
        # Verificar que el usuario existe y está activo
        usuario = self.usuario_dao.get_by_id(usuario_id)
        if not usuario or usuario.estatus_id != 1:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado o inactivo"
            )
        
        # Verificar que el rol existe y está activo
        rol = self.roles_dao.get_by_id(rol_id)
        if not rol or rol.estatus_id != 1:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rol no encontrado o inactivo"
            )
        
        # Asignar el rol
        success = self.rol_usuario_dao.assign_role_to_user(usuario_id, rol_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario ya tiene asignado este rol"
            )
        
        return True
    
    def remove_rol_from_usuario(self, usuario_id: int, rol_id: int) -> bool:
        """
        Remueve un rol de un usuario
        
        Args:
            usuario_id (int): ID del usuario
            rol_id (int): ID del rol
            
        Returns:
            bool: True si se removió correctamente
            
        Raises:
            HTTPException: Si el usuario o rol no existen, o no está asignado
        """
        # Verificar que el usuario existe
        usuario = self.usuario_dao.get_by_id(usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        # Verificar que el rol existe
        rol = self.roles_dao.get_by_id(rol_id)
        if not rol:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rol no encontrado"
            )
        
        # Remover el rol
        success = self.rol_usuario_dao.remove_role_from_user(usuario_id, rol_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario no tiene asignado este rol"
            )
        
        return True
    
    def get_usuario_roles(self, usuario_id: int) -> List[RolSimpleResponse]:
        """
        Obtiene los roles de un usuario
        
        Args:
            usuario_id (int): ID del usuario
            
        Returns:
            List[RolSimpleResponse]: Lista de roles del usuario
            
        Raises:
            HTTPException: Si el usuario no existe
        """
        # Verificar que el usuario existe
        usuario = self.usuario_dao.get_by_id(usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        # Obtener roles
        roles = self.rol_usuario_dao.get_user_roles(usuario_id)
        
        return [
            RolSimpleResponse(
                id_rol=rol.id_rol,
                rol=rol.rol
            )
            for rol in roles
        ]
    
    def get_rol_usuarios(self, rol_id: int) -> List[UsuarioResponse]:
        """
        Obtiene los usuarios que tienen un rol específico
        
        Args:
            rol_id (int): ID del rol
            
        Returns:
            List[UsuarioResponse]: Lista de usuarios con el rol
            
        Raises:
            HTTPException: Si el rol no existe
        """
        # Verificar que el rol existe
        rol = self.roles_dao.get_by_id(rol_id)
        if not rol:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rol no encontrado"
            )
        
        # Obtener usuarios
        usuarios = self.rol_usuario_dao.get_role_users(rol_id)
        
        return [
            UsuarioResponse(
                id_usuario=usuario.id_usuario,
                login=usuario.login,
                correo_electronico=usuario.correo_electronico,
                estatus_id=usuario.estatus_id,
                roles=[]  # No incluimos roles para evitar recursión
            )
            for usuario in usuarios
        ]
    
    def bulk_assign_roles_to_usuario(self, usuario_id: int, roles_ids: List[int]) -> int:
        """
        Asigna múltiples roles a un usuario
        
        Args:
            usuario_id (int): ID del usuario
            roles_ids (List[int]): Lista de IDs de roles
            
        Returns:
            int: Número de roles asignados exitosamente
            
        Raises:
            HTTPException: Si el usuario no existe o algún rol no existe
        """
        # Verificar que el usuario existe y está activo
        usuario = self.usuario_dao.get_by_id(usuario_id)
        if not usuario or usuario.estatus_id != 1:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado o inactivo"
            )
        
        # Verificar que todos los roles existen y están activos
        for rol_id in roles_ids:
            rol = self.roles_dao.get_by_id(rol_id)
            if not rol or rol.estatus_id != 1:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Rol con ID {rol_id} no encontrado o inactivo"
                )
        
        # Asignar roles
        assigned_count = self.rol_usuario_dao.assign_multiple_roles_to_user(usuario_id, roles_ids)
        
        return assigned_count
    
    def bulk_remove_roles_from_usuario(self, usuario_id: int, roles_ids: List[int]) -> int:
        """
        Remueve múltiples roles de un usuario
        
        Args:
            usuario_id (int): ID del usuario
            roles_ids (List[int]): Lista de IDs de roles
            
        Returns:
            int: Número de roles removidos exitosamente
            
        Raises:
            HTTPException: Si el usuario no existe
        """
        # Verificar que el usuario existe
        usuario = self.usuario_dao.get_by_id(usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        # Remover roles
        removed_count = self.rol_usuario_dao.remove_multiple_roles_from_user(usuario_id, roles_ids)
        
        return removed_count
    
    def get_usuario_with_roles(self, usuario_id: int) -> UsuarioResponse:
        """
        Obtiene un usuario con sus roles
        
        Args:
            usuario_id (int): ID del usuario
            
        Returns:
            UsuarioResponse: Usuario con sus roles
            
        Raises:
            HTTPException: Si el usuario no existe
        """
        # Obtener usuario
        usuario = self.usuario_dao.get_by_id(usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        # Obtener roles
        roles = self.get_usuario_roles(usuario_id)
        
        return UsuarioResponse(
            id_usuario=usuario.id_usuario,
            login=usuario.login,
            correo_electronico=usuario.correo_electronico,
            estatus_id=usuario.estatus_id,
            roles=roles
        )
