from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
from core.database_connection import get_database_session
from services.ai.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["Chat IA"])
security = HTTPBearer()
chat_service = ChatService()

class ChatMessage(BaseModel):
    message: str
    user_id: Optional[str] = None  # Opcional, se puede obtener del token

class ChatResponse(BaseModel):
    response: str
    timestamp: str
    sources: List[str] = []  # Archivos de documentación usados

@router.post("/", response_model=ChatResponse)
def enviar_mensaje(
    data: ChatMessage,
    db: Session = Depends(get_database_session),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Envía un mensaje al asistente de IA y recibe una respuesta.
    Mantiene el contexto de la conversación por usuario.
    """
    try:
        # Obtener user_id del token (puedes extraerlo del JWT)
        # Por ahora usamos un ID simple, pero puedes mejorarlo
        token = credentials.credentials
        
        # TODO: Extraer user_id del token JWT
        # Por ahora usamos el token como identificador temporal
        user_id = data.user_id or f"user_{token[:10]}"
        
        resultado = chat_service.chat(user_id, data.message)
        
        return ChatResponse(
            response=resultado["response"],
            timestamp=resultado["timestamp"],
            sources=resultado.get("sources", [])
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el chat: {str(e)}")

@router.post("/limpiar")
def limpiar_conversacion(
    db: Session = Depends(get_database_session),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Limpia el historial de conversación del usuario actual.
    """
    try:
        token = credentials.credentials
        user_id = f"user_{token[:10]}"
        chat_service.limpiar_historial(user_id)
        return {"message": "Historial limpiado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al limpiar historial: {str(e)}")

@router.post("/recargar-docs")
def recargar_documentacion(
    db: Session = Depends(get_database_session),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Recarga la documentación desde los archivos markdown.
    Útil después de actualizar la documentación.
    """
    try:
        documentos_cargados = chat_service.recargar_documentacion()
        return {
            "message": "Documentación recargada correctamente",
            "documentos": documentos_cargados
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al recargar documentación: {str(e)}")

