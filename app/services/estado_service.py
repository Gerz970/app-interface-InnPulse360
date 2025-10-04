"""
Servicio de Estado
Maneja la lógica de negocio para estados
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from dao.dao_estado import EstadoDAO
from dao.dao_pais import PaisDAO
from models.catalogos.models import *
from schemas.catalogos.estado_schemas import EstadoCreate, EstadoUpdate, EstadoResponse
from schemas.catalogos.pais_schemas import PaisResponse


class EstadoService:
    """
    Servicio para manejar la lógica de negocio de estados
    """
    
    def __init__(self, db_session: Session):
        """
        Inicializa el servicio con una sesión de base de datos
        
        Args:
            db_session (Session): Sesión de SQLAlchemy
        """
        self.db = db_session
        self.dao = EstadoDAO(db_session)
        self.pais_dao = PaisDAO(db_session)
    
    def create_estado(self, estado_data: EstadoCreate) -> EstadoResponse:
        """
        Crea un nuevo estado
        
        Args:
            estado_data (EstadoCreate): Datos del estado
            
        Returns:
            EstadoResponse: Estado creado
            
        Raises:
            HTTPException: Si el país no existe o el nombre del estado ya existe
        """
        # Verificar que el país existe y está activo
        pais = self.pais_dao.get_by_id(estado_data.id_pais)
        if not pais or pais.id_estatus != 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El país especificado no existe o está inactivo"
            )
        
        # Verificar si el nombre del estado ya existe en ese país
        if self.dao.exists_by_nombre_in_pais(estado_data.nombre, estado_data.id_pais):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un estado con ese nombre en el país especificado"
            )
        
        # Crear el estado
        db_estado = self.dao.create(estado_data)
        
        return EstadoResponse(
            id_estado=db_estado.id_estado,
            id_pais=db_estado.id_pais,
            nombre=db_estado.nombre,
            id_estatus=db_estado.id_estatus,
            pais=PaisResponse(
                id_pais=pais.id_pais,
                nombre=pais.nombre,
                id_estatus=pais.id_estatus
            )
        )
    
    def get_estado_by_id(self, id_estado: int) -> Optional[EstadoResponse]:
        """
        Obtiene un estado por ID
        
        Args:
            id_estado (int): ID del estado
            
        Returns:
            Optional[EstadoResponse]: Estado encontrado o None
        """
        db_estado = self.dao.get_by_id(id_estado)
        if not db_estado:
            return None
        
        # Obtener información del país
        pais = self.pais_dao.get_by_id(db_estado.id_pais)
        pais_response = None
        if pais:
            pais_response = PaisResponse(
                id_pais=pais.id_pais,
                nombre=pais.nombre,
                id_estatus=pais.id_estatus
            )
        
        return EstadoResponse(
            id_estado=db_estado.id_estado,
            id_pais=db_estado.id_pais,
            nombre=db_estado.nombre,
            id_estatus=db_estado.id_estatus,
            pais=pais_response
        )
    
    def get_estado_by_nombre(self, nombre: str) -> Optional[EstadoResponse]:
        """
        Obtiene un estado por nombre
        
        Args:
            nombre (str): Nombre del estado
            
        Returns:
            Optional[EstadoResponse]: Estado encontrado o None
        """
        db_estado = self.dao.get_by_nombre(nombre)
        if not db_estado:
            return None
        
        # Obtener información del país
        pais = self.pais_dao.get_by_id(db_estado.id_pais)
        pais_response = None
        if pais:
            pais_response = PaisResponse(
                id_pais=pais.id_pais,
                nombre=pais.nombre,
                id_estatus=pais.id_estatus
            )
        
        return EstadoResponse(
            id_estado=db_estado.id_estado,
            id_pais=db_estado.id_pais,
            nombre=db_estado.nombre,
            id_estatus=db_estado.id_estatus,
            pais=pais_response
        )
    
    def get_estados_by_pais(self, id_pais: int) -> List[EstadoResponse]:
        """
        Obtiene todos los estados de un país
        
        Args:
            id_pais (int): ID del país
            
        Returns:
            List[EstadoResponse]: Lista de estados del país
        """
        db_estados = self.dao.get_by_pais(id_pais)
        
        # Obtener información del país
        pais = self.pais_dao.get_by_id(id_pais)
        pais_response = None
        if pais:
            pais_response = PaisResponse(
                id_pais=pais.id_pais,
                nombre=pais.nombre,
                id_estatus=pais.id_estatus
            )
        
        return [
            EstadoResponse(
                id_estado=estado.id_estado,
                id_pais=estado.id_pais,
                nombre=estado.nombre,
                id_estatus=estado.id_estatus,
                pais=pais_response
            )
            for estado in db_estados
        ]
    
    def get_all_estados(self, skip: int = 0, limit: int = 100) -> List[EstadoResponse]:
        """
        Obtiene una lista de estados
        
        Args:
            skip (int): Registros a saltar
            limit (int): Límite de registros
            
        Returns:
            List[EstadoResponse]: Lista de estados
        """
        db_estados = self.dao.get_active_estados(skip, limit)
        estados_response = []
        
        for estado in db_estados:
            # Obtener información del país
            pais = self.pais_dao.get_by_id(estado.id_pais)
            pais_response = None
            if pais:
                pais_response = PaisResponse(
                    id_pais=pais.id_pais,
                    nombre=pais.nombre,
                    id_estatus=pais.id_estatus
                )
            
            estados_response.append(EstadoResponse(
                id_estado=estado.id_estado,
                id_pais=estado.id_pais,
                nombre=estado.nombre,
                id_estatus=estado.id_estatus,
                pais=pais_response
            ))
        
        return estados_response
    
    def update_estado(self, id_estado: int, estado_data: EstadoUpdate) -> Optional[EstadoResponse]:
        """
        Actualiza un estado existente
        
        Args:
            id_estado (int): ID del estado
            estado_data (EstadoUpdate): Datos a actualizar
            
        Returns:
            Optional[EstadoResponse]: Estado actualizado o None
            
        Raises:
            HTTPException: Si hay conflictos de nombre o país
        """
        # Verificar si el estado existe
        existing_estado = self.dao.get_by_id(id_estado)
        if not existing_estado:
            return None
        
        # Verificar que el país existe si se está actualizando
        if estado_data.id_pais:
            pais = self.pais_dao.get_by_id(estado_data.id_pais)
            if not pais or pais.id_estatus != 1:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El país especificado no existe o está inactivo"
                )
        
        # Verificar conflictos de nombre si se está actualizando
        if estado_data.nombre:
            pais_id = estado_data.id_pais or existing_estado.id_pais
            if self.dao.exists_by_nombre_in_pais(estado_data.nombre, pais_id, exclude_id=id_estado):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ya existe un estado con ese nombre en el país especificado"
                )
        
        # Actualizar el estado
        db_estado = self.dao.update(id_estado, estado_data)
        if not db_estado:
            return None
        
        # Obtener información del país
        pais = self.pais_dao.get_by_id(db_estado.id_pais)
        pais_response = None
        if pais:
            pais_response = PaisResponse(
                id_pais=pais.id_pais,
                nombre=pais.nombre,
                id_estatus=pais.id_estatus
            )
        
        return EstadoResponse(
            id_estado=db_estado.id_estado,
            id_pais=db_estado.id_pais,
            nombre=db_estado.nombre,
            id_estatus=db_estado.id_estatus,
            pais=pais_response
        )
    
    def delete_estado(self, id_estado: int) -> bool:
        """
        Eliminación lógica de un estado
        
        Args:
            id_estado (int): ID del estado
            
        Returns:
            bool: True si se eliminó correctamente
        """
        return self.dao.delete_logical(id_estado)
    
    def reactivate_estado(self, id_estado: int) -> bool:
        """
        Reactiva un estado
        
        Args:
            id_estado (int): ID del estado
            
        Returns:
            bool: True si se reactivó correctamente
        """
        return self.dao.reactivate(id_estado)
