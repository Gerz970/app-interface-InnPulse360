"""
Servicio de Mensaje
Maneja la lógica de negocio para mensajes e integración con WebSocket y FCM
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime

from dao.mensajeria.dao_conversacion import ConversacionDAO
from dao.mensajeria.dao_mensaje import MensajeDAO
from dao.seguridad.dao_usuario import UsuarioDAO
from models.mensajeria.mensaje_model import Mensaje
from schemas.mensajeria.mensaje_schema import MensajeCreate, MensajeResponse
from services.mensajeria.websocket_manager import WebSocketManager
from services.notifications.fcm_push_service import FCMPushService


class MensajeService:
    """
    Servicio para manejar la lógica de negocio de mensajes
    Incluye integración con WebSocket y FCM para notificaciones
    """
    
    def __init__(self, db_session: Session):
        """
        Inicializa el servicio con una sesión de base de datos
        
        Args:
            db_session (Session): Sesión de SQLAlchemy
        """
        self.db = db_session
        self.dao = MensajeDAO(db_session)
        self.conversacion_dao = ConversacionDAO(db_session)
        self.usuario_dao = UsuarioDAO(db_session)
        self.websocket_manager = WebSocketManager()
        self.fcm_service = FCMPushService(db_session)
    
    def enviar_mensaje(
        self,
        conversacion_id: int,
        remitente_id: int,
        contenido: str
    ) -> MensajeResponse:
        """
        Envía un mensaje en una conversación
        
        Args:
            conversacion_id (int): ID de la conversación
            remitente_id (int): ID del usuario que envía
            contenido (str): Contenido del mensaje
            
        Returns:
            MensajeResponse: Mensaje creado
            
        Raises:
            HTTPException: Si hay error de validación
        """
        # Validar que la conversación existe
        conversacion = self.conversacion_dao.get_by_id(conversacion_id)
        if not conversacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversación no encontrada"
            )
        
        # Validar que el remitente es participante
        if conversacion.usuario1_id != remitente_id and conversacion.usuario2_id != remitente_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para enviar mensajes en esta conversación"
            )
        
        # Validar que la conversación está activa
        if conversacion.id_estatus != 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La conversación está archivada"
            )
        
        # Crear el mensaje
        mensaje_data = {
            'conversacion_id': conversacion_id,
            'remitente_id': remitente_id,
            'contenido': contenido,
            'fecha_envio': datetime.now(),
            'id_estatus': 1
        }
        
        mensaje = self.dao.create(mensaje_data)
        
        # Actualizar fecha del último mensaje en la conversación
        self.conversacion_dao.update_ultimo_mensaje(conversacion_id, mensaje.fecha_envio)
        
        # Determinar destinatario
        destinatario_id = (
            conversacion.usuario2_id 
            if remitente_id == conversacion.usuario1_id 
            else conversacion.usuario1_id
        )
        
        # Obtener información del remitente para notificación
        remitente = self.usuario_dao.get_by_id(remitente_id)
        remitente_nombre = remitente.login if remitente else "Usuario"
        
        # Preparar respuesta del mensaje
        mensaje_response = MensajeResponse(
            id_mensaje=mensaje.id_mensaje,
            conversacion_id=mensaje.conversacion_id,
            remitente_id=mensaje.remitente_id,
            contenido=mensaje.contenido,
            fecha_envio=mensaje.fecha_envio,
            fecha_leido=mensaje.fecha_leido,
            id_estatus=mensaje.id_estatus,
            adjuntos=[]
        )
        
        # Enviar notificación FCM si el destinatario no está conectado por WebSocket
        # Nota: El envío por WebSocket se manejará en el endpoint WebSocket cuando el usuario esté conectado
        # Si no está conectado, enviamos notificación push para que se entere cuando vuelva a abrir la app
        if not self.websocket_manager.is_user_connected(destinatario_id):
            try:
                contenido_preview = contenido[:100] + "..." if len(contenido) > 100 else contenido
                self.fcm_service.send_to_user(
                    usuario_id=destinatario_id,
                    title=f"Nuevo mensaje de {remitente_nombre}",
                    body=contenido_preview,
                    data={
                        'type': 'mensaje',
                        'conversacion_id': str(conversacion_id),
                        'mensaje_id': str(mensaje.id_mensaje),
                        'remitente_nombre': remitente_nombre
                    }
                )
            except Exception as e:
                print(f"Error enviando notificación FCM: {e}")
        
        return mensaje_response
    
    def obtener_mensajes_conversacion(
        self,
        conversacion_id: int,
        usuario_id: int,
        skip: int = 0,
        limit: int = 50
    ) -> List[MensajeResponse]:
        """
        Obtiene los mensajes de una conversación con paginación
        
        Args:
            conversacion_id (int): ID de la conversación
            usuario_id (int): ID del usuario que solicita (para validación)
            skip (int): Número de mensajes a saltar
            limit (int): Número máximo de mensajes
            
        Returns:
            List[MensajeResponse]: Lista de mensajes
            
        Raises:
            HTTPException: Si no tiene permisos
        """
        # Validar que el usuario es participante
        conversacion = self.conversacion_dao.get_by_id(conversacion_id)
        if not conversacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversación no encontrada"
            )
        
        if conversacion.usuario1_id != usuario_id and conversacion.usuario2_id != usuario_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para ver los mensajes de esta conversación"
            )
        
        mensajes = self.dao.get_by_conversacion(conversacion_id, skip, limit)
        
        # Marcar mensajes como leídos cuando el usuario los ve
        self.dao.marcar_todos_leidos_conversacion(conversacion_id, usuario_id)
        
        resultado = []
        for msg in mensajes:
            resultado.append(MensajeResponse(
                id_mensaje=msg.id_mensaje,
                conversacion_id=msg.conversacion_id,
                remitente_id=msg.remitente_id,
                contenido=msg.contenido,
                fecha_envio=msg.fecha_envio,
                fecha_leido=msg.fecha_leido,
                id_estatus=msg.id_estatus,
                adjuntos=[]
            ))
        
        return resultado
    
    def marcar_mensaje_leido(
        self,
        mensaje_id: int,
        usuario_id: int
    ) -> MensajeResponse:
        """
        Marca un mensaje como leído
        
        Args:
            mensaje_id (int): ID del mensaje
            usuario_id (int): ID del usuario que marca como leído
            
        Returns:
            MensajeResponse: Mensaje actualizado
            
        Raises:
            HTTPException: Si no existe o no tiene permisos
        """
        mensaje = self.dao.get_by_id(mensaje_id)
        
        if not mensaje:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mensaje no encontrado"
            )
        
        # Validar que el usuario es el destinatario (no el remitente)
        conversacion = self.conversacion_dao.get_by_id(mensaje.conversacion_id)
        if not conversacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversación no encontrada"
            )
        
        destinatario_id = (
            conversacion.usuario2_id 
            if mensaje.remitente_id == conversacion.usuario1_id 
            else conversacion.usuario1_id
        )
        
        if usuario_id != destinatario_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No puedes marcar este mensaje como leído"
            )
        
        mensaje_actualizado = self.dao.marcar_leido(mensaje_id)
        
        return MensajeResponse(
            id_mensaje=mensaje_actualizado.id_mensaje,
            conversacion_id=mensaje_actualizado.conversacion_id,
            remitente_id=mensaje_actualizado.remitente_id,
            contenido=mensaje_actualizado.contenido,
            fecha_envio=mensaje_actualizado.fecha_envio,
            fecha_leido=mensaje_actualizado.fecha_leido,
            id_estatus=mensaje_actualizado.id_estatus,
            adjuntos=[]
        )
    
    def obtener_contador_no_leidos(self, usuario_id: int) -> int:
        """
        Obtiene el contador de mensajes no leídos de un usuario
        
        Args:
            usuario_id (int): ID del usuario
            
        Returns:
            int: Cantidad de mensajes no leídos
        """
        return self.dao.contar_no_leidos_usuario(usuario_id)

