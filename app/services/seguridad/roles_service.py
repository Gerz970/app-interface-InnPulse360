"""
Servicio de Roles
Maneja la lógica de negocio para roles
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from dao.seguridad.dao_roles import RolesDAO
from models.seguridad.roles_model import Roles
from schemas.seguridad.roles_create import RolesCreate
from schemas.seguridad.roles_update import RolesUpdate
from schemas.seguridad.roles_response import RolesResponse


class RolesService:
    """
    Servicio para manejar la lógica de negocio de roles
    """
    
    def __init__(self, db_session: Session):
        """
        Inicializa el servicio con una sesión de base de datos
        
        Args:
            db_session (Session): Sesión de SQLAlchemy
        """
        self.db = db_session
        self.dao = RolesDAO(db_session)
    
    def create_rol(self, roles_data: RolesCreate) -> RolesResponse:
        """
        Crea un nuevo rol
        
        Args:
            roles_data (RolesCreate): Datos del rol
            
        Returns:
            RolesResponse: Rol creado
            
        Raises:
            HTTPException: Si el nombre del rol ya existe
        """
        # Verificar si el nombre del rol ya existe
        if self.dao.exists_by_rol(roles_data.rol):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre del rol ya está en uso"
            )
        
        # Crear el rol
        db_roles = self.dao.create(roles_data)
        
        # Retornar sin información sensible
        return RolesResponse(
            id_rol=db_roles.id_rol,
            rol=db_roles.rol,
            descripcion=db_roles.descripcion,
            estatus_id=db_roles.estatus_id
        )
    
    def get_rol_by_id(self, id_rol: int) -> Optional[RolesResponse]:
        """
        Obtiene un rol por ID
        
        Args:
            id_rol (int): ID del rol
            
        Returns:
            Optional[RolesResponse]: Rol encontrado o None
        """
        db_roles = self.dao.get_by_id(id_rol)
        if not db_roles:
            return None
        
        return RolesResponse(
            id_rol=db_roles.id_rol,
            rol=db_roles.rol,
            descripcion=db_roles.descripcion,
            estatus_id=db_roles.estatus_id
        )
    
    def get_rol_by_name(self, rol: str) -> Optional[RolesResponse]:
        """
        Obtiene un rol por nombre
        
        Args:
            rol (str): Nombre del rol
            
        Returns:
            Optional[RolesResponse]: Rol encontrado o None
        """
        db_roles = self.dao.get_by_rol(rol)
        if not db_roles:
            return None
        
        return RolesResponse(
            id_rol=db_roles.id_rol,
            rol=db_roles.rol,
            descripcion=db_roles.descripcion,
            estatus_id=db_roles.estatus_id
        )
    
    def get_all_roles(self, skip: int = 0, limit: int = 100) -> List[RolesResponse]:
        """
        Obtiene una lista de roles
        
        Args:
            skip (int): Registros a saltar
            limit (int): Límite de registros
            
        Returns:
            List[RolesResponse]: Lista de roles
        """
        db_roles = self.dao.get_active_roles(skip, limit)
        return [
            RolesResponse(
                id_rol=rol.id_rol,
                rol=rol.rol,
                descripcion=rol.descripcion,
                estatus_id=rol.estatus_id
            )
            for rol in db_roles
        ]
    
    def update_rol(self, id_rol: int, roles_data: RolesUpdate) -> Optional[RolesResponse]:
        """
        Actualiza un rol existente
        
        Args:
            id_rol (int): ID del rol
            roles_data (RolesUpdate): Datos a actualizar
            
        Returns:
            Optional[RolesResponse]: Rol actualizado o None
            
        Raises:
            HTTPException: Si hay conflictos de nombre
        """
        # Verificar si el rol existe
        existing_rol = self.dao.get_by_id(id_rol)
        if not existing_rol:
            return None
        
        # Verificar conflictos de nombre si se está actualizando
        if roles_data.rol and roles_data.rol != existing_rol.rol:
            if self.dao.exists_by_rol(roles_data.rol, exclude_id=id_rol):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El nombre del rol ya está en uso"
                )
        
        # Actualizar el rol
        db_roles = self.dao.update(id_rol, roles_data)
        if not db_roles:
            return None
        
        return RolesResponse(
            id_rol=db_roles.id_rol,
            rol=db_roles.rol,
            descripcion=db_roles.descripcion,
            estatus_id=db_roles.estatus_id
        )
    
    def delete_rol(self, id_rol: int) -> bool:
        """
        Eliminación lógica de un rol
        
        Args:
            id_rol (int): ID del rol
            
        Returns:
            bool: True si se eliminó correctamente
        """
        return self.dao.delete_logical(id_rol)
    
    def reactivate_rol(self, id_rol: int) -> bool:
        """
        Reactiva un rol
        
        Args:
            id_rol (int): ID del rol
            
        Returns:
            bool: True si se reactivó correctamente
        """
        return self.dao.reactivate(id_rol)
