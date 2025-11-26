"""
Manager para manejar conexiones WebSocket activas
Gestiona las conexiones de usuarios conectados en tiempo real
"""

from typing import Dict, List
from fastapi import WebSocket
import json
import logging

logger = logging.getLogger(__name__)


class WebSocketManager:
    """
    Clase singleton para manejar conexiones WebSocket activas
    Almacena las conexiones por usuario_id
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(WebSocketManager, cls).__new__(cls)
            cls._instance.active_connections: Dict[int, List[WebSocket]] = {}
        return cls._instance
    
    async def connect(self, websocket: WebSocket, usuario_id: int):
        """
        Conecta un WebSocket para un usuario
        
        Args:
            websocket (WebSocket): Conexión WebSocket
            usuario_id (int): ID del usuario
        """
        await websocket.accept()
        if usuario_id not in self.active_connections:
            self.active_connections[usuario_id] = []
        self.active_connections[usuario_id].append(websocket)
        logger.info(f"Usuario {usuario_id} conectado. Total conexiones: {len(self.active_connections[usuario_id])}")
    
    def disconnect(self, websocket: WebSocket, usuario_id: int):
        """
        Desconecta un WebSocket de un usuario
        
        Args:
            websocket (WebSocket): Conexión WebSocket
            usuario_id (int): ID del usuario
        """
        if usuario_id in self.active_connections:
            try:
                self.active_connections[usuario_id].remove(websocket)
                if not self.active_connections[usuario_id]:
                    del self.active_connections[usuario_id]
                logger.info(f"Usuario {usuario_id} desconectado")
            except ValueError:
                logger.warning(f"WebSocket no encontrado en conexiones del usuario {usuario_id}")
    
    async def send_personal_message(self, message: dict, usuario_id: int):
        """
        Envía un mensaje a un usuario específico
        
        Args:
            message (dict): Mensaje a enviar
            usuario_id (int): ID del usuario destinatario
        """
        if usuario_id in self.active_connections:
            disconnected = []
            for connection in self.active_connections[usuario_id]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error(f"Error enviando mensaje a usuario {usuario_id}: {e}")
                    disconnected.append(connection)
            
            # Remover conexiones desconectadas
            for conn in disconnected:
                self.active_connections[usuario_id].remove(conn)
            
            # Si no quedan conexiones, eliminar entrada
            if not self.active_connections[usuario_id]:
                del self.active_connections[usuario_id]
    
    def is_user_connected(self, usuario_id: int) -> bool:
        """
        Verifica si un usuario está conectado
        
        Args:
            usuario_id (int): ID del usuario
            
        Returns:
            bool: True si está conectado, False si no
        """
        return usuario_id in self.active_connections and len(self.active_connections[usuario_id]) > 0
    
    async def broadcast_to_conversation(self, message: dict, usuario1_id: int, usuario2_id: int):
        """
        Envía un mensaje a ambos usuarios de una conversación
        
        Args:
            message (dict): Mensaje a enviar
            usuario1_id (int): ID del primer usuario
            usuario2_id (int): ID del segundo usuario
        """
        await self.send_personal_message(message, usuario1_id)
        await self.send_personal_message(message, usuario2_id)

