"""
DAO (Data Access Object) para operaciones CRUD de Conversacion
Maneja todas las interacciones con la base de datos para la entidad Conversacion
"""

from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_, and_, func, case
from models.mensajeria.conversacion_model import Conversacion
from models.mensajeria.mensaje_model import Mensaje


class ConversacionDAO:
    """
    Clase DAO para manejar operaciones CRUD de Conversacion en la base de datos
    Utiliza SQLAlchemy ORM para las operaciones
    """

    __status_active__ = 1
    __status_archived__ = 0
    
    def __init__(self, db_session: Session):
        """
        Inicializa el DAO con una sesión de base de datos
        
        Args:
            db_session (Session): Sesión de SQLAlchemy para operaciones de BD
        """
        self.db = db_session
    
    def create(self, conversacion_data: dict) -> Conversacion:
        """
        Crea una nueva conversación en la base de datos
        
        Args:
            conversacion_data (dict): Datos de la conversación a crear
            
        Returns:
            Conversacion: Objeto Conversacion creado con ID asignado
            
        Raises:
            SQLAlchemyError: Si hay un error en la base de datos
        """
        try:
            conversacion_dict = conversacion_data.copy()
            conversacion_dict['id_estatus'] = conversacion_dict.get('id_estatus', self.__status_active__)
            db_conversacion = Conversacion(**conversacion_dict)
            
            self.db.add(db_conversacion)
            self.db.commit()
            self.db.refresh(db_conversacion)
            
            return db_conversacion
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def get_by_id(self, id_conversacion: int) -> Optional[Conversacion]:
        """
        Obtiene una conversación por su ID
        
        Args:
            id_conversacion (int): ID de la conversación a buscar
            
        Returns:
            Optional[Conversacion]: Conversación encontrada o None si no existe
        """
        try:
            return self.db.query(Conversacion).filter(
                Conversacion.id_conversacion == id_conversacion
            ).first()
        except SQLAlchemyError as e:
            raise e
    
    def get_by_usuarios(self, usuario1_id: int, usuario2_id: int) -> Optional[Conversacion]:
        """
        Obtiene una conversación entre dos usuarios específicos
        
        Args:
            usuario1_id (int): ID del primer usuario
            usuario2_id (int): ID del segundo usuario
            
        Returns:
            Optional[Conversacion]: Conversación encontrada o None si no existe
        """
        try:
            return self.db.query(Conversacion).filter(
                or_(
                    and_(Conversacion.usuario1_id == usuario1_id, Conversacion.usuario2_id == usuario2_id),
                    and_(Conversacion.usuario1_id == usuario2_id, Conversacion.usuario2_id == usuario1_id)
                ),
                Conversacion.id_estatus == self.__status_active__
            ).first()
        except SQLAlchemyError as e:
            raise e
    
    def get_by_usuario(self, usuario_id: int, skip: int = 0, limit: int = 100) -> List[Conversacion]:
        """
        Obtiene todas las conversaciones de un usuario
        
        Args:
            usuario_id (int): ID del usuario
            skip (int): Número de registros a saltar
            limit (int): Número máximo de registros a retornar
            
        Returns:
            List[Conversacion]: Lista de conversaciones
        """
        try:
            # Para SQL Server, usamos CASE para manejar NULLs en el ORDER BY
            # NULLs irán al final usando un valor muy antiguo
            return (
                self.db.query(Conversacion)
                    .filter(
                        or_(
                            Conversacion.usuario1_id == usuario_id,
                            Conversacion.usuario2_id == usuario_id
                        ),
                        Conversacion.id_estatus == self.__status_active__
                    )
                    .order_by(
                        case(
                            (Conversacion.fecha_ultimo_mensaje.is_(None), 0),
                            else_=1
                        ).desc(),
                        Conversacion.fecha_ultimo_mensaje.desc()
                    )
                    .offset(skip)
                    .limit(limit)
                    .all()
            )
        except SQLAlchemyError as e:
            raise e
    
    def get_by_cliente(self, cliente_id: int) -> List[Conversacion]:
        """
        Obtiene todas las conversaciones de un cliente
        
        Args:
            cliente_id (int): ID del cliente
            
        Returns:
            List[Conversacion]: Lista de conversaciones
        """
        try:
            return (
                self.db.query(Conversacion)
                    .filter(
                        Conversacion.cliente_id == cliente_id,
                        Conversacion.id_estatus == self.__status_active__
                    )
                    .order_by(
                        case(
                            (Conversacion.fecha_ultimo_mensaje.is_(None), 0),
                            else_=1
                        ).desc(),
                        Conversacion.fecha_ultimo_mensaje.desc()
                    )
                    .all()
            )
        except SQLAlchemyError as e:
            raise e
    
    def get_by_empleado(self, empleado_id: int) -> List[Conversacion]:
        """
        Obtiene todas las conversaciones de un empleado
        
        Args:
            empleado_id (int): ID del empleado
            
        Returns:
            List[Conversacion]: Lista de conversaciones
        """
        try:
            return (
                self.db.query(Conversacion)
                    .filter(
                        or_(
                            Conversacion.empleado1_id == empleado_id,
                            Conversacion.empleado2_id == empleado_id
                        ),
                        Conversacion.id_estatus == self.__status_active__
                    )
                    .order_by(
                        case(
                            (Conversacion.fecha_ultimo_mensaje.is_(None), 0),
                            else_=1
                        ).desc(),
                        Conversacion.fecha_ultimo_mensaje.desc()
                    )
                    .all()
            )
        except SQLAlchemyError as e:
            raise e
    
    def update_ultimo_mensaje(self, id_conversacion: int, fecha_ultimo_mensaje) -> Optional[Conversacion]:
        """
        Actualiza la fecha del último mensaje de una conversación
        
        Args:
            id_conversacion (int): ID de la conversación
            fecha_ultimo_mensaje: Fecha del último mensaje
            
        Returns:
            Optional[Conversacion]: Conversación actualizada o None si no existe
        """
        try:
            conversacion = self.get_by_id(id_conversacion)
            if conversacion:
                conversacion.fecha_ultimo_mensaje = fecha_ultimo_mensaje
                self.db.commit()
                self.db.refresh(conversacion)
            return conversacion
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def archivar(self, id_conversacion: int) -> Optional[Conversacion]:
        """
        Archiva una conversación (cambia estatus a archivada)
        
        Args:
            id_conversacion (int): ID de la conversación
            
        Returns:
            Optional[Conversacion]: Conversación archivada o None si no existe
        """
        try:
            conversacion = self.get_by_id(id_conversacion)
            if conversacion:
                conversacion.id_estatus = self.__status_archived__
                self.db.commit()
                self.db.refresh(conversacion)
            return conversacion
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def delete(self, id_conversacion: int) -> bool:
        """
        Elimina una conversación (soft delete - cambia estatus)
        
        Args:
            id_conversacion (int): ID de la conversación
            
        Returns:
            bool: True si se eliminó correctamente, False si no existe
        """
        try:
            conversacion = self.get_by_id(id_conversacion)
            if conversacion:
                conversacion.id_estatus = self.__status_archived__
                self.db.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

