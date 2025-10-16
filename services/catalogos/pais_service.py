"""
Servicio de País
Maneja la lógica de negocio para países
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from dao.catalogos.dao_pais import PaisDAO
from models.catalogos.models import *
from schemas.catalogos.pais_schemas import PaisCreate, PaisUpdate, PaisResponse


class PaisService:
    """
    Servicio para manejar la lógica de negocio de países
    """
    
    def __init__(self, db_session: Session):
        """
        Inicializa el servicio con una sesión de base de datos
        
        Args:
            db_session (Session): Sesión de SQLAlchemy
        """
        self.db = db_session
        self.dao = PaisDAO(db_session)
    
    def create_pais(self, pais_data: PaisCreate) -> PaisResponse:
        """
        Crea un nuevo país
        
        Args:
            pais_data (PaisCreate): Datos del país
            
        Returns:
            PaisResponse: País creado
            
        Raises:
            HTTPException: Si el nombre del país ya existe
        """
        # Verificar si el nombre del país ya existe
        if self.dao.exists_by_nombre(pais_data.nombre):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre del país ya está en uso"
            )
        
        # Crear el país
        db_pais = self.dao.create(pais_data)
        
        return PaisResponse(
            id_pais=db_pais.id_pais,
            nombre=db_pais.nombre,
            id_estatus=db_pais.id_estatus
        )
    
    def get_pais_by_id(self, id_pais: int) -> Optional[PaisResponse]:
        """
        Obtiene un país por ID
        
        Args:
            id_pais (int): ID del país
            
        Returns:
            Optional[PaisResponse]: País encontrado o None
        """
        db_pais = self.dao.get_by_id(id_pais)
        if not db_pais:
            return None
        
        return PaisResponse(
            id_pais=db_pais.id_pais,
            nombre=db_pais.nombre,
            id_estatus=db_pais.id_estatus
        )
    
    def get_pais_by_nombre(self, nombre: str) -> Optional[PaisResponse]:
        """
        Obtiene un país por nombre
        
        Args:
            nombre (str): Nombre del país
            
        Returns:
            Optional[PaisResponse]: País encontrado o None
        """
        db_pais = self.dao.get_by_nombre(nombre)
        if not db_pais:
            return None
        
        return PaisResponse(
            id_pais=db_pais.id_pais,
            nombre=db_pais.nombre,
            id_estatus=db_pais.id_estatus
        )
    
    def get_all_paises(self, skip: int = 0, limit: int = 100) -> List[PaisResponse]:
        """
        Obtiene una lista de países
        
        Args:
            skip (int): Registros a saltar
            limit (int): Límite de registros
            
        Returns:
            List[PaisResponse]: Lista de países
        """
        db_paises = self.dao.get_active_paises(skip, limit)
        return [
            PaisResponse(
                id_pais=pais.id_pais,
                nombre=pais.nombre,
                id_estatus=pais.id_estatus
            )
            for pais in db_paises
        ]
    
    def update_pais(self, id_pais: int, pais_data: PaisUpdate) -> Optional[PaisResponse]:
        """
        Actualiza un país existente
        
        Args:
            id_pais (int): ID del país
            pais_data (PaisUpdate): Datos a actualizar
            
        Returns:
            Optional[PaisResponse]: País actualizado o None
            
        Raises:
            HTTPException: Si hay conflictos de nombre
        """
        # Verificar si el país existe
        existing_pais = self.dao.get_by_id(id_pais)
        if not existing_pais:
            return None
        
        # Verificar conflictos de nombre si se está actualizando
        if pais_data.nombre and pais_data.nombre != existing_pais.nombre:
            if self.dao.exists_by_nombre(pais_data.nombre, exclude_id=id_pais):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El nombre del país ya está en uso"
                )
        
        # Actualizar el país
        db_pais = self.dao.update(id_pais, pais_data)
        if not db_pais:
            return None
        
        return PaisResponse(
            id_pais=db_pais.id_pais,
            nombre=db_pais.nombre,
            id_estatus=db_pais.id_estatus
        )
    
    def delete_pais(self, id_pais: int) -> bool:
        """
        Eliminación lógica de un país
        
        Args:
            id_pais (int): ID del país
            
        Returns:
            bool: True si se eliminó correctamente
        """
        return self.dao.delete_logical(id_pais)
    
    def reactivate_pais(self, id_pais: int) -> bool:
        """
        Reactiva un país
        
        Args:
            id_pais (int): ID del país
            
        Returns:
            bool: True si se reactivó correctamente
        """
        return self.dao.reactivate(id_pais)
