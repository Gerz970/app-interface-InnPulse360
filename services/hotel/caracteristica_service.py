"""
Servicio de Caracteristica
Maneja la lógica de negocio para características
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from dao.hotel.dao_caracteristica import CaracteristicaDAO
from models.hotel.caracteristica_model import Caracteristica
from schemas.hotel.caracteristica_schemas import CaracteristicaCreate, CaracteristicaUpdate, CaracteristicaResponse


class CaracteristicaService:
    """
    Servicio para manejar la lógica de negocio de características
    """
    
    def __init__(self, db_session: Session):
        """
        Inicializa el servicio con una sesión de base de datos
        
        Args:
            db_session (Session): Sesión de SQLAlchemy
        """
        self.db = db_session
        self.dao = CaracteristicaDAO(db_session)
    
    def create_caracteristica(self, caracteristica_data: CaracteristicaCreate) -> CaracteristicaResponse:
        """
        Crea una nueva característica
        
        Args:
            caracteristica_data (CaracteristicaCreate): Datos de la característica
            
        Returns:
            CaracteristicaResponse: Característica creada
            
        Raises:
            HTTPException: Si el nombre de la característica ya existe
        """
        # Verificar si el nombre de la característica ya existe
        if self.dao.exists_by_nombre(caracteristica_data.caracteristica):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre de la característica ya está en uso"
            )
        
        # Crear la característica
        db_caracteristica = self.dao.create(caracteristica_data)
        
        return CaracteristicaResponse(
            id_caracteristica=db_caracteristica.id_caracteristica,
            caracteristica=db_caracteristica.caracteristica,
            descripcion=db_caracteristica.descripcion
        )
    
    def get_caracteristica_by_id(self, id_caracteristica: int) -> Optional[CaracteristicaResponse]:
        """
        Obtiene una característica por ID
        
        Args:
            id_caracteristica (int): ID de la característica
            
        Returns:
            Optional[CaracteristicaResponse]: Característica encontrada o None
        """
        db_caracteristica = self.dao.get_by_id(id_caracteristica)
        if not db_caracteristica:
            return None
        
        return CaracteristicaResponse(
            id_caracteristica=db_caracteristica.id_caracteristica,
            caracteristica=db_caracteristica.caracteristica,
            descripcion=db_caracteristica.descripcion
        )
    
    def get_caracteristica_by_nombre(self, caracteristica: str) -> Optional[CaracteristicaResponse]:
        """
        Obtiene una característica por nombre
        
        Args:
            caracteristica (str): Nombre de la característica
            
        Returns:
            Optional[CaracteristicaResponse]: Característica encontrada o None
        """
        db_caracteristica = self.dao.get_by_nombre(caracteristica)
        if not db_caracteristica:
            return None
        
        return CaracteristicaResponse(
            id_caracteristica=db_caracteristica.id_caracteristica,
            caracteristica=db_caracteristica.caracteristica,
            descripcion=db_caracteristica.descripcion
        )
    
    def get_all_caracteristicas(self, skip: int = 0, limit: int = 100) -> List[CaracteristicaResponse]:
        """
        Obtiene una lista de características
        
        Args:
            skip (int): Registros a saltar
            limit (int): Límite de registros
            
        Returns:
            List[CaracteristicaResponse]: Lista de características
        """
        db_caracteristicas = self.dao.get_all(skip, limit)
        return [
            CaracteristicaResponse(
                id_caracteristica=caracteristica.id_caracteristica,
                caracteristica=caracteristica.caracteristica,
                descripcion=caracteristica.descripcion
            )
            for caracteristica in db_caracteristicas
        ]
    
    def update_caracteristica(self, id_caracteristica: int, caracteristica_data: CaracteristicaUpdate) -> Optional[CaracteristicaResponse]:
        """
        Actualiza una característica existente
        
        Args:
            id_caracteristica (int): ID de la característica
            caracteristica_data (CaracteristicaUpdate): Datos a actualizar
            
        Returns:
            Optional[CaracteristicaResponse]: Característica actualizada o None
            
        Raises:
            HTTPException: Si hay conflictos de nombre
        """
        # Verificar si la característica existe
        existing_caracteristica = self.dao.get_by_id(id_caracteristica)
        if not existing_caracteristica:
            return None
        
        # Verificar conflictos de nombre si se está actualizando
        if caracteristica_data.caracteristica and caracteristica_data.caracteristica != existing_caracteristica.caracteristica:
            if self.dao.exists_by_nombre(caracteristica_data.caracteristica, exclude_id=id_caracteristica):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El nombre de la característica ya está en uso"
                )
        
        # Actualizar la característica
        db_caracteristica = self.dao.update(id_caracteristica, caracteristica_data)
        if not db_caracteristica:
            return None
        
        return CaracteristicaResponse(
            id_caracteristica=db_caracteristica.id_caracteristica,
            caracteristica=db_caracteristica.caracteristica,
            descripcion=db_caracteristica.descripcion
        )
    
    def delete_caracteristica(self, id_caracteristica: int) -> bool:
        """
        Elimina una característica
        
        Args:
            id_caracteristica (int): ID de la característica
            
        Returns:
            bool: True si se eliminó correctamente
        """
        return self.dao.delete(id_caracteristica)
