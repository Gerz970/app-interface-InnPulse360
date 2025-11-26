"""
Endpoints WebSocket para mensajería en tiempo real
Este archivo contiene funciones que se registrarán en main.py
"""

import json
import logging
from typing import Optional
from fastapi import WebSocket, WebSocketDisconnect, HTTPException, status, Query
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from core.database_connection import get_database_session
from core.config import AuthSettings
from services.mensajeria.websocket_manager import WebSocketManager
from services.mensajeria.mensaje_service import MensajeService
from services.mensajeria.conversacion_service import ConversacionService

logger = logging.getLogger(__name__)

websocket_manager = WebSocketManager()


async def verify_token(token: str) -> Optional[dict]:
    """
    Verifica un token JWT y retorna el payload
    
    Args:
        token (str): Token JWT
        
    Returns:
        Optional[dict]: Payload del token o None si es inválido
    """
    try:
        payload = jwt.decode(
            token,
            AuthSettings.secret_key,
            algorithms=[AuthSettings.algorithm]
        )
        return payload
    except JWTError:
        return None


def register_websocket_endpoint(app):
    """
    Registra el endpoint WebSocket en la aplicación FastAPI
    
    Args:
        app: Instancia de FastAPI
    """
    @app.websocket("/ws/{usuario_id}")
    async def websocket_endpoint(
        websocket: WebSocket,
        usuario_id: int,
        token: Optional[str] = Query(None)
    ):
        """
        Endpoint WebSocket para mensajería en tiempo real
        
        Args:
            websocket (WebSocket): Conexión WebSocket
            usuario_id (int): ID del usuario (debe coincidir con el token)
            token (Optional[str]): Token JWT en query parameter
        """
        # Verificar token
        if not token:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return
        
        payload = await verify_token(token)
        if not payload:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return
        
        # Verificar que el usuario_id del token coincide con el de la URL
        token_usuario_id = payload.get("sub")
        if not token_usuario_id or int(token_usuario_id) != usuario_id:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return
        
        # Conectar el WebSocket
        await websocket_manager.connect(websocket, usuario_id)
        
        try:
            # Obtener sesión de base de datos
            db = next(get_database_session())
            mensaje_service = MensajeService(db)
            conversacion_service = ConversacionService(db)
            
            while True:
                # Recibir mensaje del cliente
                data = await websocket.receive_text()
                
                try:
                    message_data = json.loads(data)
                    message_type = message_data.get("type")
                    
                    if message_type == "enviar_mensaje":
                        # Enviar mensaje a través del servicio
                        conversacion_id = message_data.get("conversacion_id")
                        contenido = message_data.get("contenido")
                        
                        if not conversacion_id or not contenido:
                            await websocket.send_json({
                                "type": "error",
                                "message": "conversacion_id y contenido son requeridos"
                            })
                            continue
                        
                        # Crear mensaje usando el servicio
                        mensaje_response = mensaje_service.enviar_mensaje(
                            conversacion_id=conversacion_id,
                            remitente_id=usuario_id,
                            contenido=contenido
                        )
                        
                        # Obtener conversación para determinar destinatario
                        conversacion = conversacion_service.obtener_conversacion_por_id(
                            conversacion_id, usuario_id
                        )
                        destinatario_id = (
                            conversacion.usuario2_id 
                            if usuario_id == conversacion.usuario1_id 
                            else conversacion.usuario1_id
                        )
                        
                        # Enviar mensaje al destinatario si está conectado
                        await websocket_manager.send_personal_message({
                            "type": "nuevo_mensaje",
                            "conversacion_id": conversacion_id,
                            "mensaje": {
                                "id_mensaje": mensaje_response.id_mensaje,
                                "conversacion_id": mensaje_response.conversacion_id,
                                "remitente_id": mensaje_response.remitente_id,
                                "contenido": mensaje_response.contenido,
                                "fecha_envio": mensaje_response.fecha_envio.isoformat(),
                                "fecha_leido": mensaje_response.fecha_leido.isoformat() if mensaje_response.fecha_leido else None,
                                "id_estatus": mensaje_response.id_estatus
                            }
                        }, destinatario_id)
                        
                        # Confirmar al remitente
                        await websocket.send_json({
                            "type": "mensaje_enviado",
                            "mensaje": {
                                "id_mensaje": mensaje_response.id_mensaje,
                                "conversacion_id": mensaje_response.conversacion_id,
                                "remitente_id": mensaje_response.remitente_id,
                                "contenido": mensaje_response.contenido,
                                "fecha_envio": mensaje_response.fecha_envio.isoformat(),
                                "fecha_leido": mensaje_response.fecha_leido.isoformat() if mensaje_response.fecha_leido else None,
                                "id_estatus": mensaje_response.id_estatus
                            }
                        })
                    
                    elif message_type == "ping":
                        # Responder a ping con pong
                        await websocket.send_json({"type": "pong"})
                    
                    else:
                        await websocket.send_json({
                            "type": "error",
                            "message": f"Tipo de mensaje desconocido: {message_type}"
                        })
                
                except json.JSONDecodeError:
                    await websocket.send_json({
                        "type": "error",
                        "message": "Formato JSON inválido"
                    })
                except Exception as e:
                    logger.error(f"Error procesando mensaje WebSocket: {e}")
                    await websocket.send_json({
                        "type": "error",
                        "message": str(e)
                    })
        
        except WebSocketDisconnect:
            websocket_manager.disconnect(websocket, usuario_id)
            logger.info(f"Usuario {usuario_id} desconectado")
        except Exception as e:
            logger.error(f"Error en WebSocket: {e}")
            websocket_manager.disconnect(websocket, usuario_id)
        finally:
            if 'db' in locals():
                db.close()

