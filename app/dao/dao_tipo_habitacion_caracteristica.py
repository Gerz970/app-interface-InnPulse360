"""
DAO (Data Access Object) para operaciones de asignación de características a tipos de habitación
Maneja la tabla intermedia entre TipoHabitacion y Caracteristica
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_
from models.catalogos.models import TipoHabitacionCaracteristica, TipoHabitacion, Caracteristica


class TipoHabitacionCaracteristicaDAO:
    """
    Clase DAO para manejar operaciones de asignación de características a tipos de habitación
    Utiliza SQLAlchemy ORM para las operaciones
    """
    
    def __init__(self, db_session: Session):
        """
        Inicializa el DAO con una sesión de base de datos
        
        Args:
            db_session (Session): Sesión de SQLAlchemy para operaciones de BD
        """
        self.db = db_session
    
    def assign_caracteristica_to_tipo_habitacion(self, tipo_habitacion_id: int, caracteristica_id: int) -> bool:
        """
        Asigna una característica a un tipo de habitación
        
        Args:
            tipo_habitacion_id (int): ID del tipo de habitación
            caracteristica_id (int): ID de la característica
            
        Returns:
            bool: True si se asignó correctamente, False si ya existía
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            # Verificar si ya existe la asignación
            existing = self.db.query(TipoHabitacionCaracteristica).filter(
                and_(
                    TipoHabitacionCaracteristica.tipo_habitacion_id == tipo_habitacion_id,
                    TipoHabitacionCaracteristica.caracteristica_id == caracteristica_id
                )
            ).first()
            
            if existing:
                return False  # Ya existe la asignación
            
            # Crear nueva asignación
            tipo_habitacion_caracteristica = TipoHabitacionCaracteristica(
                tipo_habitacion_id=tipo_habitacion_id,
                caracteristica_id=caracteristica_id
            )
            
            self.db.add(tipo_habitacion_caracteristica)
            self.db.commit()
            
            return True
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def remove_caracteristica_from_tipo_habitacion(self, tipo_habitacion_id: int, caracteristica_id: int) -> bool:
        """
        Remueve una característica de un tipo de habitación
        
        Args:
            tipo_habitacion_id (int): ID del tipo de habitación
            caracteristica_id (int): ID de la característica
            
        Returns:
            bool: True si se removió correctamente, False si no existía
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            # Buscar la asignación
            tipo_habitacion_caracteristica = self.db.query(TipoHabitacionCaracteristica).filter(
                and_(
                    TipoHabitacionCaracteristica.tipo_habitacion_id == tipo_habitacion_id,
                    TipoHabitacionCaracteristica.caracteristica_id == caracteristica_id
                )
            ).first()
            
            if not tipo_habitacion_caracteristica:
                return False  # No existe la asignación
            
            # Eliminar la asignación
            self.db.delete(tipo_habitacion_caracteristica)
            self.db.commit()
            
            return True
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def get_caracteristicas_by_tipo_habitacion(self, tipo_habitacion_id: int) -> List[Caracteristica]:
        """
        Obtiene todas las características asignadas a un tipo de habitación
        
        Args:
            tipo_habitacion_id (int): ID del tipo de habitación
            
        Returns:
            List[Caracteristica]: Lista de características asignadas al tipo de habitación
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            return (
                self.db.query(Caracteristica)
                .join(TipoHabitacionCaracteristica, Caracteristica.id_caracteristica == TipoHabitacionCaracteristica.caracteristica_id)
                .filter(TipoHabitacionCaracteristica.tipo_habitacion_id == tipo_habitacion_id)
                .order_by(Caracteristica.id_caracteristica.asc())
                .all()
            )
        except SQLAlchemyError as e:
            raise e
    
    def get_tipos_habitacion_by_caracteristica(self, caracteristica_id: int) -> List[TipoHabitacion]:
        """
        Obtiene todos los tipos de habitación que tienen una característica específica
        
        Args:
            caracteristica_id (int): ID de la característica
            
        Returns:
            List[TipoHabitacion]: Lista de tipos de habitación con la característica
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            return (
                self.db.query(TipoHabitacion)
                .join(TipoHabitacionCaracteristica, TipoHabitacion.id_tipoHabitacion == TipoHabitacionCaracteristica.tipo_habitacion_id)
                .filter(TipoHabitacionCaracteristica.caracteristica_id == caracteristica_id)
                .filter(TipoHabitacion.estatus_id == 1)  # Solo tipos de habitación activos
                .order_by(TipoHabitacion.id_tipoHabitacion.asc())
                .all()
            )
        except SQLAlchemyError as e:
            raise e
    
    def get_all_assignments(self, skip: int = 0, limit: int = 100) -> List[TipoHabitacionCaracteristica]:
        """
        Obtiene todas las asignaciones con paginación
        
        Args:
            skip (int): Número de registros a saltar
            limit (int): Número máximo de registros a retornar
            
        Returns:
            List[TipoHabitacionCaracteristica]: Lista de asignaciones
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            return (
                self.db.query(TipoHabitacionCaracteristica)
                .offset(skip)
                .limit(limit)
                .all()
            )
        except SQLAlchemyError as e:
            raise e
    
    def bulk_assign_caracteristicas_to_tipo_habitacion(self, tipo_habitacion_id: int, caracteristicas_ids: List[int]) -> int:
        """
        Asigna múltiples características a un tipo de habitación (solo las que no estén ya asignadas)
        
        Args:
            tipo_habitacion_id (int): ID del tipo de habitación
            caracteristicas_ids (List[int]): Lista de IDs de características
            
        Returns:
            int: Número de características asignadas exitosamente
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            assigned_count = 0
            
            for caracteristica_id in caracteristicas_ids:
                # Verificar si ya existe la asignación
                existing = self.db.query(TipoHabitacionCaracteristica).filter(
                    and_(
                        TipoHabitacionCaracteristica.tipo_habitacion_id == tipo_habitacion_id,
                        TipoHabitacionCaracteristica.caracteristica_id == caracteristica_id
                    )
                ).first()
                
                if not existing:
                    # Crear nueva asignación
                    tipo_habitacion_caracteristica = TipoHabitacionCaracteristica(
                        tipo_habitacion_id=tipo_habitacion_id,
                        caracteristica_id=caracteristica_id
                    )
                    self.db.add(tipo_habitacion_caracteristica)
                    assigned_count += 1
            
            self.db.commit()
            return assigned_count
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def bulk_remove_caracteristicas_from_tipo_habitacion(self, tipo_habitacion_id: int, caracteristicas_ids: List[int]) -> int:
        """
        Remueve múltiples características de un tipo de habitación
        
        Args:
            tipo_habitacion_id (int): ID del tipo de habitación
            caracteristicas_ids (List[int]): Lista de IDs de características
            
        Returns:
            int: Número de características removidas exitosamente
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            removed_count = 0
            
            for caracteristica_id in caracteristicas_ids:
                # Buscar la asignación
                tipo_habitacion_caracteristica = self.db.query(TipoHabitacionCaracteristica).filter(
                    and_(
                        TipoHabitacionCaracteristica.tipo_habitacion_id == tipo_habitacion_id,
                        TipoHabitacionCaracteristica.caracteristica_id == caracteristica_id
                    )
                ).first()
                
                if tipo_habitacion_caracteristica:
                    # Eliminar la asignación
                    self.db.delete(tipo_habitacion_caracteristica)
                    removed_count += 1
            
            self.db.commit()
            return removed_count
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def exists_assignment(self, tipo_habitacion_id: int, caracteristica_id: int) -> bool:
        """
        Verifica si existe una asignación entre tipo de habitación y característica
        
        Args:
            tipo_habitacion_id (int): ID del tipo de habitación
            caracteristica_id (int): ID de la característica
            
        Returns:
            bool: True si existe la asignación, False si no
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            return (
                self.db.query(TipoHabitacionCaracteristica)
                .filter(
                    and_(
                        TipoHabitacionCaracteristica.tipo_habitacion_id == tipo_habitacion_id,
                        TipoHabitacionCaracteristica.caracteristica_id == caracteristica_id
                    )
                )
                .first() is not None
            )
        except SQLAlchemyError as e:
            raise e
