"""
DAO (Data Access Object) para operaciones CRUD de DeviceToken
Maneja todas las interacciones con la base de datos para tokens de dispositivos FCM
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.seguridad.device_token_model import DeviceToken
from datetime import datetime


class DeviceTokenDAO:
    """
    Clase DAO para manejar operaciones CRUD de DeviceToken en la base de datos
    Utiliza SQLAlchemy ORM para las operaciones
    """
    
    def __init__(self, db_session: Session):
        """
        Inicializa el DAO con una sesión de base de datos
        
        Args:
            db_session (Session): Sesión de SQLAlchemy para operaciones de BD
        """
        self.db = db_session
    
    def create_or_update(self, usuario_id: int, device_token: str, plataforma: str) -> DeviceToken:
        """
        Crea o actualiza un token de dispositivo
        Si el token ya existe, lo actualiza. Si no, lo crea.
        
        Args:
            usuario_id (int): ID del usuario propietario del token
            device_token (str): Token FCM del dispositivo
            plataforma (str): Plataforma del dispositivo ('android' o 'ios')
            
        Returns:
            DeviceToken: Token creado o actualizado
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            # Buscar si ya existe este token
            existing = self.db.query(DeviceToken).filter(
                DeviceToken.device_token == device_token
            ).first()
            
            if existing:
                # Actualizar token existente
                existing.usuario_id = usuario_id
                existing.plataforma = plataforma
                existing.activo = True
                existing.fecha_actualizacion = datetime.utcnow()
                self.db.commit()
                self.db.refresh(existing)
                return existing
            else:
                # Crear nuevo token
                nuevo_token = DeviceToken(
                    usuario_id=usuario_id,
                    device_token=device_token,
                    plataforma=plataforma,
                    activo=True
                )
                self.db.add(nuevo_token)
                self.db.commit()
                self.db.refresh(nuevo_token)
                return nuevo_token
                
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def get_by_usuario_id(self, usuario_id: int) -> List[DeviceToken]:
        """
        Obtener todos los tokens activos de un usuario
        
        Args:
            usuario_id (int): ID del usuario
            
        Returns:
            List[DeviceToken]: Lista de tokens activos del usuario
        """
        try:
            return self.db.query(DeviceToken).filter(
                DeviceToken.usuario_id == usuario_id,
                DeviceToken.activo == True
            ).all()
        except SQLAlchemyError as e:
            raise e
    
    def deactivate_by_usuario_id(self, usuario_id: int) -> bool:
        """
        Desactivar todos los tokens de un usuario (útil para logout)
        
        Args:
            usuario_id (int): ID del usuario
            
        Returns:
            bool: True si se desactivaron tokens, False si no había tokens
        """
        try:
            tokens_actualizados = self.db.query(DeviceToken).filter(
                DeviceToken.usuario_id == usuario_id,
                DeviceToken.activo == True
            ).update({"activo": False, "fecha_actualizacion": datetime.utcnow()})
            
            self.db.commit()
            return tokens_actualizados > 0
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

