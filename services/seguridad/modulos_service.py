"""
Servicio de Módulos
Maneja la lógica de negocio para módulos y sus asociaciones con roles
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from dao.seguridad.dao_modulos import ModulosDAO
from dao.seguridad.dao_modulo_rol import ModuloRolDAO
from dao.seguridad.dao_roles import RolesDAO
from models.seguridad.modulos_model import Modulos
from schemas.seguridad.modulos_create import ModulosCreate
from schemas.seguridad.modulos_update import ModulosUpdate
from schemas.seguridad.modulos_response import ModulosResponse
from schemas.seguridad.modulo_rol_schemas import ModuloRolAsignacion, ModuloRolAsignacionMultiple, ModuloRolResponse


class ModulosService:
    """
    Servicio para manejar la lógica de negocio de módulos
    Incluye gestión de módulos y sus asociaciones con roles
    """
    
    def __init__(self, db_session: Session):
        """
        Inicializa el servicio con una sesión de base de datos
        
        Args:
            db_session (Session): Sesión de SQLAlchemy
        """
        self.db = db_session
        self.modulos_dao = ModulosDAO(db_session)
        self.modulo_rol_dao = ModuloRolDAO(db_session)
        self.roles_dao = RolesDAO(db_session)
    
    def create_modulo(self, modulo_data: ModulosCreate) -> ModulosResponse:
        """
        Crea un nuevo módulo
        
        Args:
            modulo_data (ModulosCreate): Datos del módulo a crear
            
        Returns:
            ModulosResponse: Módulo creado
            
        Raises:
            HTTPException: Si hay errores de validación o base de datos
        """
        try:
            # Verificar que no existe un módulo con el mismo nombre
            if self.modulos_dao.exists_by_nombre(modulo_data.nombre):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ya existe un módulo con el nombre '{modulo_data.nombre}'"
                )
            
            # Crear el módulo
            db_modulo = self.modulos_dao.create(modulo_data)
            
            # Convertir a response
            return self._modulo_to_response(db_modulo)
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al crear el módulo: {str(e)}"
            )
    
    def get_modulo_by_id(self, id_modulo: int) -> ModulosResponse:
        """
        Obtiene un módulo por su ID
        
        Args:
            id_modulo (int): ID del módulo
            
        Returns:
            ModulosResponse: Módulo encontrado
            
        Raises:
            HTTPException: Si el módulo no existe
        """
        try:
            db_modulo = self.modulos_dao.get_by_id(id_modulo)
            if not db_modulo:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Módulo con ID {id_modulo} no encontrado"
                )
            
            return self._modulo_to_response(db_modulo)
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener el módulo: {str(e)}"
            )
    
    def get_all_modulos(self, skip: int = 0, limit: int = 100, activos_only: bool = False, movil_only: Optional[int] = None) -> List[ModulosResponse]:
        """
        Obtiene todos los módulos
        
        Args:
            skip (int): Número de registros a omitir
            limit (int): Número máximo de registros
            activos_only (bool): Si solo obtener módulos activos
            movil_only (Optional[int]): Si es 1, solo obtener módulos para movil. Si es 0, solo web. Si es None, por defecto trae los móviles
        Returns:
            List[ModulosResponse]: Lista de módulos
        """
        try:
            if activos_only:
                db_modulos = self.modulos_dao.get_active(skip, limit)
            else:
                db_modulos = self.modulos_dao.get_all(skip, limit)
            
            if movil_only == 1:
                # Si se pasa el parámetro y es 1, traer solo los móviles
                db_modulos = [modulo for modulo in db_modulos if modulo.movil == 1]
            elif movil_only == 0:
                # Si se pasa el parámetro y es 0, traer solo los web
                db_modulos = [modulo for modulo in db_modulos if modulo.movil == 0]
            # Si movil_only es None, no se filtra (pero en el endpoint se convierte a 1 por defecto)
            
            return [self._modulo_to_response(modulo) for modulo in db_modulos]
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener los módulos: {str(e)}"
            )
    
    def update_modulo(self, id_modulo: int, modulo_data: ModulosUpdate) -> ModulosResponse:
        """
        Actualiza un módulo existente
        
        Args:
            id_modulo (int): ID del módulo a actualizar
            modulo_data (ModulosUpdate): Datos a actualizar
            
        Returns:
            ModulosResponse: Módulo actualizado
            
        Raises:
            HTTPException: Si el módulo no existe o hay errores de validación
        """
        try:
            # Verificar que el módulo existe
            existing_modulo = self.modulos_dao.get_by_id(id_modulo)
            if not existing_modulo:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Módulo con ID {id_modulo} no encontrado"
                )
            
            # Si se está cambiando el nombre, verificar que no existe otro con el mismo nombre
            if modulo_data.nombre and modulo_data.nombre != existing_modulo.nombre:
                if self.modulos_dao.exists_by_nombre(modulo_data.nombre, exclude_id=id_modulo):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Ya existe un módulo con el nombre '{modulo_data.nombre}'"
                    )
            
            # Actualizar el módulo
            db_modulo = self.modulos_dao.update(id_modulo, modulo_data)
            if not db_modulo:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Módulo con ID {id_modulo} no encontrado"
                )
            
            return self._modulo_to_response(db_modulo)
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al actualizar el módulo: {str(e)}"
            )
    
    def delete_modulo(self, id_modulo: int) -> bool:
        """
        Elimina un módulo (soft delete)
        
        Args:
            id_modulo (int): ID del módulo a eliminar
            
        Returns:
            bool: True si se eliminó correctamente
            
        Raises:
            HTTPException: Si el módulo no existe
        """
        try:
            # Verificar que el módulo existe
            existing_modulo = self.modulos_dao.get_by_id(id_modulo)
            if not existing_modulo:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Módulo con ID {id_modulo} no encontrado"
                )
            
            # Eliminar el módulo
            success = self.modulos_dao.delete(id_modulo)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Módulo con ID {id_modulo} no encontrado"
                )
            
            return True
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al eliminar el módulo: {str(e)}"
            )
    
    def asignar_modulo_a_rol(self, modulo_id: int, rol_id: int) -> bool:
        """
        Asigna un módulo a un rol
        
        Args:
            modulo_id (int): ID del módulo
            rol_id (int): ID del rol
            
        Returns:
            bool: True si se asignó correctamente
            
        Raises:
            HTTPException: Si hay errores de validación
        """
        try:
            # Verificar que el módulo existe
            modulo = self.modulos_dao.get_by_id(modulo_id)
            if not modulo:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Módulo con ID {modulo_id} no encontrado"
                )
            
            # Verificar que el rol existe
            rol = self.roles_dao.get_by_id(rol_id)
            if not rol:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Rol con ID {rol_id} no encontrado"
                )
            
            # Asignar el módulo al rol
            success = self.modulo_rol_dao.asignar_modulo_a_rol(modulo_id, rol_id)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se pudo asignar el módulo al rol"
                )
            
            return True
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al asignar módulo al rol: {str(e)}"
            )
    
    def desasignar_modulo_de_rol(self, modulo_id: int, rol_id: int) -> bool:
        """
        Desasigna un módulo de un rol
        
        Args:
            modulo_id (int): ID del módulo
            rol_id (int): ID del rol
            
        Returns:
            bool: True si se desasignó correctamente
            
        Raises:
            HTTPException: Si hay errores de validación
        """
        try:
            # Verificar que el módulo existe
            modulo = self.modulos_dao.get_by_id(modulo_id)
            if not modulo:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Módulo con ID {modulo_id} no encontrado"
                )
            
            # Verificar que el rol existe
            rol = self.roles_dao.get_by_id(rol_id)
            if not rol:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Rol con ID {rol_id} no encontrado"
                )
            
            # Desasignar el módulo del rol
            success = self.modulo_rol_dao.desasignar_modulo_de_rol(modulo_id, rol_id)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se pudo desasignar el módulo del rol"
                )
            
            return True
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al desasignar módulo del rol: {str(e)}"
            )
    
    def asignar_multiples_modulos_a_rol(self, rol_id: int, modulos_ids: List[int]) -> bool:
        """
        Asigna múltiples módulos a un rol
        
        Args:
            rol_id (int): ID del rol
            modulos_ids (List[int]): Lista de IDs de módulos
            
        Returns:
            bool: True si se asignaron correctamente
            
        Raises:
            HTTPException: Si hay errores de validación
        """
        try:
            # Verificar que el rol existe
            rol = self.roles_dao.get_by_id(rol_id)
            if not rol:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Rol con ID {rol_id} no encontrado"
                )
            
            # Verificar que todos los módulos existen
            for modulo_id in modulos_ids:
                modulo = self.modulos_dao.get_by_id(modulo_id)
                if not modulo:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Módulo con ID {modulo_id} no encontrado"
                    )
            
            # Asignar los módulos al rol
            success = self.modulo_rol_dao.asignar_multiples_modulos_a_rol(rol_id, modulos_ids)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se pudieron asignar los módulos al rol"
                )
            
            return True
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al asignar múltiples módulos al rol: {str(e)}"
            )
    
    def get_modulos_por_rol(self, rol_id: int) -> List[ModulosResponse]:
        """
        Obtiene todos los módulos asignados a un rol
        
        Args:
            rol_id (int): ID del rol
            
        Returns:
            List[ModulosResponse]: Lista de módulos asignados al rol
            
        Raises:
            HTTPException: Si el rol no existe
        """
        try:
            # Verificar que el rol existe
            rol = self.roles_dao.get_by_id(rol_id)
            if not rol:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Rol con ID {rol_id} no encontrado"
                )
            
            # Obtener los módulos del rol
            db_modulos = self.modulo_rol_dao.get_modulos_por_rol(rol_id)
            
            return [self._modulo_to_response(modulo) for modulo in db_modulos]
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener módulos del rol: {str(e)}"
            )
    
    def _modulo_to_response(self, modulo: Modulos) -> ModulosResponse:
        """
        Convierte un objeto Modulos a ModulosResponse
        
        Args:
            modulo (Modulos): Objeto módulo de la base de datos
            
        Returns:
            ModulosResponse: Objeto de respuesta
        """
        # Obtener los roles del módulo
        roles = self.modulo_rol_dao.get_roles_por_modulo(modulo.id_modulo)
        
        return ModulosResponse(
            id_modulo=modulo.id_modulo,
            nombre=modulo.nombre,
            descripcion=modulo.descripcion,
            icono=modulo.icono,
            ruta=modulo.ruta,
            id_estatus=modulo.id_estatus,
            movil=modulo.movil,
            roles=roles
        )
