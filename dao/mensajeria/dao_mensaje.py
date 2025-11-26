"""
DAO (Data Access Object) para operaciones CRUD de Mensaje
Maneja todas las interacciones con la base de datos para la entidad Mensaje
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_, or_, func
from datetime import datetime
from models.mensajeria.mensaje_model import Mensaje
from models.mensajeria.conversacion_model import Conversacion


class MensajeDAO:
    """
    Clase DAO para manejar operaciones CRUD de Mensaje en la base de datos
    Utiliza SQLAlchemy ORM para las operaciones
    """

    __status_enviado__ = 1
    __status_leido__ = 2
    __status_eliminado__ = 3
    
    def __init__(self, db_session: Session):
        """
        Inicializa el DAO con una sesión de base de datos
        
        Args:
            db_session (Session): Sesión de SQLAlchemy para operaciones de BD
        """
        self.db = db_session
    
    def create(self, mensaje_data: dict) -> Mensaje:
        """
        Crea un nuevo mensaje en la base de datos
        
        Args:
            mensaje_data (dict): Datos del mensaje a crear
            
        Returns:
            Mensaje: Objeto Mensaje creado con ID asignado
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            mensaje_dict = mensaje_data.copy()
            mensaje_dict['id_estatus'] = mensaje_dict.get('id_estatus', self.__status_enviado__)
            if 'fecha_envio' not in mensaje_dict:
                mensaje_dict['fecha_envio'] = datetime.now()
            
            db_mensaje = Mensaje(**mensaje_dict)
            
            self.db.add(db_mensaje)
            self.db.commit()
            self.db.refresh(db_mensaje)
            
            return db_mensaje
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def get_by_id(self, id_mensaje: int) -> Optional[Mensaje]:
        """
        Obtiene un mensaje por su ID
        
        Args:
            id_mensaje (int): ID del mensaje a buscar
            
        Returns:
            Optional[Mensaje]: Mensaje encontrado o None si no existe
        """
        try:
            return self.db.query(Mensaje).filter(
                Mensaje.id_mensaje == id_mensaje
            ).first()
        except SQLAlchemyError as e:
            raise e
    
    def get_by_conversacion(
        self, 
        conversacion_id: int, 
        skip: int = 0, 
        limit: int = 50
    ) -> List[Mensaje]:
        """
        Obtiene los mensajes de una conversación con paginación
        
        Args:
            conversacion_id (int): ID de la conversación
            skip (int): Número de registros a saltar
            limit (int): Número máximo de registros a retornar
            
        Returns:
            List[Mensaje]: Lista de mensajes ordenados por fecha (más recientes primero)
        """
        try:
            return (
                self.db.query(Mensaje)
                    .filter(
                        Mensaje.conversacion_id == conversacion_id,
                        Mensaje.id_estatus != self.__status_eliminado__
                    )
                    .order_by(Mensaje.fecha_envio.desc())
                    .offset(skip)
                    .limit(limit)
                    .all()
            )
        except SQLAlchemyError as e:
            raise e
    
    def get_no_leidos(self, conversacion_id: int, usuario_id: int) -> List[Mensaje]:
        """
        Obtiene los mensajes no leídos de una conversación para un usuario específico
        
        Args:
            conversacion_id (int): ID de la conversación
            usuario_id (int): ID del usuario (para filtrar mensajes que no son suyos)
            
        Returns:
            List[Mensaje]: Lista de mensajes no leídos
        """
        try:
            return (
                self.db.query(Mensaje)
                    .filter(
                        Mensaje.conversacion_id == conversacion_id,
                        Mensaje.remitente_id != usuario_id,
                        Mensaje.fecha_leido.is_(None),
                        Mensaje.id_estatus == self.__status_enviado__
                    )
                    .order_by(Mensaje.fecha_envio.asc())
                    .all()
            )
        except SQLAlchemyError as e:
            raise e
    
    def contar_no_leidos_usuario(self, usuario_id: int) -> int:
        """
        Cuenta los mensajes no leídos de todas las conversaciones de un usuario
        
        Args:
            usuario_id (int): ID del usuario
            
        Returns:
            int: Cantidad de mensajes no leídos
        """
        try:
            # Obtener IDs de conversaciones donde el usuario participa
            conversaciones = (
                self.db.query(Conversacion.id_conversacion)
                    .filter(
                        or_(
                            Conversacion.usuario1_id == usuario_id,
                            Conversacion.usuario2_id == usuario_id
                        ),
                        Conversacion.id_estatus == 1
                    )
                    .all()
            )
            
            conversacion_ids = [c[0] for c in conversaciones]
            
            if not conversacion_ids:
                return 0
            
            # Contar mensajes no leídos donde el usuario NO es el remitente
            count = (
                self.db.query(func.count(Mensaje.id_mensaje))
                    .filter(
                        Mensaje.conversacion_id.in_(conversacion_ids),
                        Mensaje.remitente_id != usuario_id,
                        Mensaje.fecha_leido.is_(None),
                        Mensaje.id_estatus == self.__status_enviado__
                    )
                    .scalar()
            )
            
            return count or 0
        except SQLAlchemyError as e:
            raise e
    
    def marcar_leido(self, id_mensaje: int) -> Optional[Mensaje]:
        """
        Marca un mensaje como leído
        
        Args:
            id_mensaje (int): ID del mensaje
            
        Returns:
            Optional[Mensaje]: Mensaje actualizado o None si no existe
        """
        try:
            mensaje = self.get_by_id(id_mensaje)
            if mensaje and mensaje.fecha_leido is None:
                mensaje.fecha_leido = datetime.now()
                mensaje.id_estatus = self.__status_leido__
                self.db.commit()
                self.db.refresh(mensaje)
            return mensaje
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def marcar_todos_leidos_conversacion(self, conversacion_id: int, usuario_id: int) -> int:
        """
        Marca todos los mensajes no leídos de una conversación como leídos
        
        Args:
            conversacion_id (int): ID de la conversación
            usuario_id (int): ID del usuario (solo marca mensajes que no son suyos)
            
        Returns:
            int: Cantidad de mensajes marcados como leídos
        """
        try:
            mensajes_no_leidos = self.get_no_leidos(conversacion_id, usuario_id)
            count = 0
            for mensaje in mensajes_no_leidos:
                mensaje.fecha_leido = datetime.now()
                mensaje.id_estatus = self.__status_leido__
                count += 1
            
            if count > 0:
                self.db.commit()
            
            return count
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def delete(self, id_mensaje: int) -> bool:
        """
        Elimina un mensaje (soft delete - cambia estatus)
        
        Args:
            id_mensaje (int): ID del mensaje
            
        Returns:
            bool: True si se eliminó correctamente, False si no existe
        """
        try:
            mensaje = self.get_by_id(id_mensaje)
            if mensaje:
                mensaje.id_estatus = self.__status_eliminado__
                self.db.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

