"""
DAO (Data Access Object) para operaciones CRUD de MensajeAdjunto
Maneja todas las interacciones con la base de datos para la entidad MensajeAdjunto
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.mensajeria.mensaje_adjunto_model import MensajeAdjunto


class MensajeAdjuntoDAO:
    """
    Clase DAO para manejar operaciones CRUD de MensajeAdjunto en la base de datos
    Utiliza SQLAlchemy ORM para las operaciones
    """
    
    def __init__(self, db_session: Session):
        """
        Inicializa el DAO con una sesión de base de datos
        
        Args:
            db_session (Session): Sesión de SQLAlchemy para operaciones de BD
        """
        self.db = db_session
    
    def create(self, adjunto_data: dict) -> MensajeAdjunto:
        """
        Crea un nuevo adjunto en la base de datos
        
        Args:
            adjunto_data (dict): Datos del adjunto a crear
            
        Returns:
            MensajeAdjunto: Objeto MensajeAdjunto creado con ID asignado
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            db_adjunto = MensajeAdjunto(**adjunto_data)
            
            self.db.add(db_adjunto)
            self.db.commit()
            self.db.refresh(db_adjunto)
            
            return db_adjunto
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def get_by_id(self, id_adjunto: int) -> Optional[MensajeAdjunto]:
        """
        Obtiene un adjunto por su ID
        
        Args:
            id_adjunto (int): ID del adjunto a buscar
            
        Returns:
            Optional[MensajeAdjunto]: Adjunto encontrado o None si no existe
        """
        try:
            return self.db.query(MensajeAdjunto).filter(
                MensajeAdjunto.id_adjunto == id_adjunto
            ).first()
        except SQLAlchemyError as e:
            raise e
    
    def get_by_mensaje(self, mensaje_id: int) -> List[MensajeAdjunto]:
        """
        Obtiene todos los adjuntos de un mensaje
        
        Args:
            mensaje_id (int): ID del mensaje
            
        Returns:
            List[MensajeAdjunto]: Lista de adjuntos
        """
        try:
            return (
                self.db.query(MensajeAdjunto)
                    .filter(MensajeAdjunto.mensaje_id == mensaje_id)
                    .all()
            )
        except SQLAlchemyError as e:
            raise e
    
    def delete(self, id_adjunto: int) -> bool:
        """
        Elimina un adjunto de la base de datos
        
        Args:
            id_adjunto (int): ID del adjunto
            
        Returns:
            bool: True si se eliminó correctamente, False si no existe
        """
        try:
            adjunto = self.get_by_id(id_adjunto)
            if adjunto:
                self.db.delete(adjunto)
                self.db.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

