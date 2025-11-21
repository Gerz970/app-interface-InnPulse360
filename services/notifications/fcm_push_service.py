"""
Servicio para enviar notificaciones push usando Firebase Cloud Messaging (FCM)
Usa API HTTP v1 con autenticación mediante Service Account JSON
"""

import json
import logging
from typing import List, Optional, Dict
from pathlib import Path
from sqlalchemy.orm import Session

from google.auth.transport.requests import Request
from google.oauth2 import service_account
import requests

from core.config import FCMSettings
from dao.seguridad.dao_device_token import DeviceTokenDAO

logger = logging.getLogger(__name__)


class FCMPushService:
    """
    Servicio para enviar notificaciones push usando FCM API HTTP v1
    """
    
    def __init__(self, db: Session):
        """
        Inicializa el servicio FCM
        
        Args:
            db (Session): Sesión de base de datos
        """
        self.db = db
        self.device_token_dao = DeviceTokenDAO(db)
        self.fcm_settings = FCMSettings()
        self._credentials = None
        self._project_id = None
        self._initialize_credentials()
    
    def _initialize_credentials(self):
        """
        Inicializa las credenciales de Google desde variables de entorno o archivo JSON
        Prioriza variables de entorno sobre archivo físico
        """
        try:
            # Opción 1: Intentar cargar desde variables de entorno (recomendado)
            if self.fcm_settings.has_env_variables:
                logger.info("Cargando credenciales FCM desde variables de entorno")
                service_account_dict = self.fcm_settings.get_service_account_dict()
                
                # Crear credenciales desde diccionario
                self._credentials = service_account.Credentials.from_service_account_info(
                    service_account_dict,
                    scopes=['https://www.googleapis.com/auth/firebase.messaging']
                )
                
                self._project_id = self.fcm_settings.project_id
                logger.info(f"✅ Credenciales FCM cargadas desde variables de entorno (Project ID: {self._project_id})")
                return
            
            # Opción 2: Fallback a archivo JSON (solo para desarrollo local)
            logger.info("Variables de entorno no encontradas, intentando cargar desde archivo JSON")
            service_account_path = Path(self.fcm_settings.service_account_path)
            
            if not service_account_path.exists():
                logger.warning(f"Service Account JSON no encontrado en: {service_account_path}")
                logger.warning("Configura las variables de entorno FCM_* en tu archivo .env")
                return
            
            # Cargar credenciales desde el archivo JSON
            self._credentials = service_account.Credentials.from_service_account_file(
                str(service_account_path),
                scopes=['https://www.googleapis.com/auth/firebase.messaging']
            )
            
            # Obtener project_id del archivo JSON
            with open(service_account_path, 'r') as f:
                service_account_data = json.load(f)
                self._project_id = service_account_data.get('project_id')
            
            if not self._project_id:
                logger.error("No se encontró project_id en el Service Account JSON")
            else:
                logger.info(f"✅ Credenciales FCM cargadas desde archivo JSON (Project ID: {self._project_id})")
                
        except Exception as e:
            logger.error(f"Error inicializando credenciales FCM: {e}")
            self._credentials = None
            self._project_id = None
    
    def _get_access_token(self) -> Optional[str]:
        """
        Obtiene un token de acceso válido usando las credenciales
        
        Returns:
            str: Token de acceso o None si hay error
        """
        if not self._credentials:
            logger.error("Credenciales FCM no inicializadas")
            return None
        
        try:
            # Refrescar token si es necesario
            if not self._credentials.valid:
                self._credentials.refresh(Request())
            
            return self._credentials.token
        except Exception as e:
            logger.error(f"Error obteniendo access token: {e}")
            return None
    
    def send_to_user(self, usuario_id: int, title: str, body: str, data: Optional[Dict] = None) -> Dict:
        """
        Enviar notificación a un usuario específico
        
        Args:
            usuario_id: ID del usuario destinatario
            title: Título de la notificación
            body: Cuerpo de la notificación
            data: Datos adicionales (opcional) - se pueden usar para navegación en la app
            
        Returns:
            Dict: Resultado del envío con información de éxito/fallo
        """
        # Obtener todos los tokens activos del usuario desde TU BD
        tokens = self.device_token_dao.get_by_usuario_id(usuario_id)
        
        if not tokens:
            logger.info(f"No hay tokens registrados para el usuario {usuario_id}")
            return {
                "success": False,
                "message": "Usuario sin tokens registrados",
                "sent_to": 0,
                "total_tokens": 0
            }
        
        # Enviar notificación a cada token del usuario
        results = []
        for token in tokens:
            result = self._send_fcm_notification(
                device_token=token.device_token,
                title=title,
                body=body,
                data=data
            )
            results.append(result)
        
        successful = sum(1 for r in results if r.get("success"))
        return {
            "success": successful > 0,
            "sent_to": successful,
            "total_tokens": len(tokens),
            "results": results
        }
    
    def send_to_multiple_users(self, usuario_ids: List[int], title: str, body: str, data: Optional[Dict] = None) -> List[Dict]:
        """
        Enviar notificación a múltiples usuarios específicos
        
        Args:
            usuario_ids: Lista de IDs de usuarios destinatarios
            title: Título de la notificación
            body: Cuerpo de la notificación
            data: Datos adicionales (opcional)
            
        Returns:
            List[Dict]: Lista de resultados por usuario
        """
        all_results = []
        for usuario_id in usuario_ids:
            result = self.send_to_user(usuario_id, title, body, data)
            all_results.append({
                "usuario_id": usuario_id,
                "result": result
            })
        return all_results
    
    def _send_fcm_notification(self, device_token: str, title: str, body: str, data: Optional[Dict] = None) -> Dict:
        """
        Enviar notificación individual a través de FCM API HTTP v1
        
        Args:
            device_token: Token FCM del dispositivo
            title: Título de la notificación
            body: Cuerpo de la notificación
            data: Datos adicionales (opcional)
            
        Returns:
            Dict: Resultado del envío
        """
        if not self._project_id:
            logger.error("Project ID no configurado")
            return {
                "success": False,
                "error": "Project ID no configurado",
                "device_token": device_token[:20] + "..."
            }
        
        access_token = self._get_access_token()
        if not access_token:
            logger.error("No se pudo obtener access token")
            return {
                "success": False,
                "error": "No se pudo obtener access token",
                "device_token": device_token[:20] + "..."
            }
        
        # URL de la API HTTP v1
        url = f"https://fcm.googleapis.com/v1/projects/{self._project_id}/messages:send"
        
        # Construir el mensaje según formato HTTP v1
        message = {
            "message": {
                "token": device_token,
                "notification": {
                    "title": title,
                    "body": body
                },
                "android": {
                    "priority": "high"
                },
                "apns": {
                    "headers": {
                        "apns-priority": "10"
                    },
                    "payload": {
                        "aps": {
                            "sound": "default",
                            "badge": 1
                        }
                    }
                }
            }
        }
        
        # Agregar datos adicionales si se proporcionan
        if data:
            message["message"]["data"] = {str(k): str(v) for k, v in data.items()}
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(
                url,
                json=message,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                result_data = response.json()
                logger.info(f"Notificación enviada exitosamente a {device_token[:20]}...")
                return {
                    "success": True,
                    "message_id": result_data.get("name", ""),
                    "device_token": device_token[:20] + "..."
                }
            else:
                error_data = response.json() if response.text else {}
                error_message = error_data.get("error", {}).get("message", response.text)
                logger.error(f"Error de FCM ({response.status_code}): {error_message}")
                return {
                    "success": False,
                    "error": error_message,
                    "status_code": response.status_code,
                    "device_token": device_token[:20] + "..."
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error de conexión con FCM: {e}")
            return {
                "success": False,
                "error": str(e),
                "device_token": device_token[:20] + "..."
            }
        except Exception as e:
            logger.error(f"Error inesperado enviando notificación: {e}")
            return {
                "success": False,
                "error": str(e),
                "device_token": device_token[:20] + "..."
            }

