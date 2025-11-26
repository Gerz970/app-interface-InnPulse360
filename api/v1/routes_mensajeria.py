"""
Endpoints REST para el módulo de Mensajería
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from core.database_connection import get_database_session
from services.mensajeria.conversacion_service import ConversacionService
from services.mensajeria.mensaje_service import MensajeService
from schemas.mensajeria.conversacion_schema import (
    ConversacionCreateClienteAdmin,
    ConversacionCreateEmpleadoEmpleado,
    ConversacionResponse,
    ConversacionListResponse
)
from schemas.mensajeria.mensaje_schema import MensajeCreate, MensajeResponse
from api.v1.routes_usuario import get_current_user
from schemas.seguridad.usuario_response import UsuarioResponse

router = APIRouter(
    prefix="/mensajeria",
    tags=["Mensajería"]
)


def get_conversacion_service(db: Session = Depends(get_database_session)) -> ConversacionService:
    """Dependency para obtener el servicio de conversación"""
    return ConversacionService(db)


def get_mensaje_service(db: Session = Depends(get_database_session)) -> MensajeService:
    """Dependency para obtener el servicio de mensaje"""
    return MensajeService(db)


# =============================================================================
# ENDPOINTS DE CONVERSACIONES
# =============================================================================

@router.get("/conversaciones", response_model=List[ConversacionListResponse])
def listar_conversaciones(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: UsuarioResponse = Depends(get_current_user),
    conversacion_service: ConversacionService = Depends(get_conversacion_service)
):
    """
    Lista todas las conversaciones del usuario actual
    
    - **skip**: Número de conversaciones a saltar (paginación)
    - **limit**: Número máximo de conversaciones a retornar
    """
    try:
        print(f"🔵 API: Obteniendo conversaciones para usuario_id={current_user.id_usuario}, skip={skip}, limit={limit}")
        resultado = conversacion_service.obtener_conversaciones_usuario(
            usuario_id=current_user.id_usuario,
            skip=skip,
            limit=limit
        )
        print(f"🔵 API: Retornando {len(resultado)} conversaciones")
        return resultado
    except Exception as e:
        print(f"❌ API: Error obteniendo conversaciones: {e}")
        print(f"❌ API: Tipo de error: {type(e)}")
        import traceback
        print(f"❌ API: Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener conversaciones: {str(e)}"
        )


@router.get("/conversaciones/{conversacion_id}", response_model=ConversacionResponse)
def obtener_conversacion(
    conversacion_id: int,
    current_user: UsuarioResponse = Depends(get_current_user),
    conversacion_service: ConversacionService = Depends(get_conversacion_service)
):
    """
    Obtiene el detalle de una conversación específica
    
    - **conversacion_id**: ID de la conversación
    """
    return conversacion_service.obtener_conversacion_por_id(
        conversacion_id=conversacion_id,
        usuario_id=current_user.id_usuario
    )


@router.post("/conversaciones/cliente-admin", response_model=ConversacionResponse)
def crear_conversacion_cliente_admin(
    data: ConversacionCreateClienteAdmin,
    current_user: UsuarioResponse = Depends(get_current_user),
    conversacion_service: ConversacionService = Depends(get_conversacion_service)
):
    """
    Crea una nueva conversación entre un cliente y un administrador
    
    - **cliente_id**: ID del cliente
    - **admin_id**: ID del administrador
    """
    return conversacion_service.crear_conversacion_cliente_admin(
        cliente_id=data.cliente_id,
        admin_id=data.admin_id,
        usuario_actual_id=current_user.id_usuario
    )


@router.post("/conversaciones/empleado-empleado", response_model=ConversacionResponse)
def crear_conversacion_empleado_empleado(
    data: ConversacionCreateEmpleadoEmpleado,
    current_user: UsuarioResponse = Depends(get_current_user),
    conversacion_service: ConversacionService = Depends(get_conversacion_service)
):
    """
    Crea una nueva conversación entre dos empleados
    
    - **empleado1_id**: ID del primer empleado
    - **empleado2_id**: ID del segundo empleado
    """
    return conversacion_service.crear_conversacion_empleado_empleado(
        empleado1_id=data.empleado1_id,
        empleado2_id=data.empleado2_id,
        usuario_actual_id=current_user.id_usuario
    )


@router.put("/conversaciones/{conversacion_id}/archivar", response_model=ConversacionResponse)
def archivar_conversacion(
    conversacion_id: int,
    current_user: UsuarioResponse = Depends(get_current_user),
    conversacion_service: ConversacionService = Depends(get_conversacion_service)
):
    """
    Archiva una conversación
    
    - **conversacion_id**: ID de la conversación a archivar
    """
    return conversacion_service.archivar_conversacion(
        conversacion_id=conversacion_id,
        usuario_id=current_user.id_usuario
    )


@router.get("/conversaciones/buscar-usuario")
def buscar_usuarios_disponibles(
    query: Optional[str] = Query(None, description="Búsqueda por nombre/login"),
    current_user: UsuarioResponse = Depends(get_current_user),
    conversacion_service: ConversacionService = Depends(get_conversacion_service)
):
    """
    Busca usuarios disponibles para iniciar una conversación
    
    - **query**: Término de búsqueda (opcional)
    - Retorna usuarios según el rol del usuario actual:
      - Si es Cliente: muestra Administradores
      - Si es Empleado: muestra otros Empleados
    """
    try:
        # Normalizar query - convertir string vacío a None
        query_normalizado = query if query and query.strip() else None
        print(f"🔵 API: Buscando usuarios para usuario_id={current_user.id_usuario}, query={query_normalizado}")
        resultado = conversacion_service.buscar_usuarios_disponibles(
            usuario_actual_id=current_user.id_usuario,
            query=query_normalizado
        )
        print(f"🔵 API: Retornando {len(resultado)} usuarios disponibles")
        return resultado
    except Exception as e:
        print(f"❌ API: Error buscando usuarios: {e}")
        print(f"❌ API: Tipo de error: {type(e)}")
        import traceback
        print(f"❌ API: Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar usuarios: {str(e)}"
        )


@router.get("/conversaciones/no-leidos")
def obtener_contador_no_leidos(
    current_user: UsuarioResponse = Depends(get_current_user),
    mensaje_service: MensajeService = Depends(get_mensaje_service)
):
    """
    Obtiene el contador de mensajes no leídos del usuario actual
    """
    contador = mensaje_service.obtener_contador_no_leidos(current_user.id_usuario)
    return {"contador_no_leidos": contador}


# =============================================================================
# ENDPOINTS DE MENSAJES
# =============================================================================

@router.get("/conversaciones/{conversacion_id}/mensajes", response_model=List[MensajeResponse])
def obtener_mensajes(
    conversacion_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: UsuarioResponse = Depends(get_current_user),
    mensaje_service: MensajeService = Depends(get_mensaje_service)
):
    """
    Obtiene los mensajes de una conversación con paginación
    
    - **conversacion_id**: ID de la conversación
    - **skip**: Número de mensajes a saltar
    - **limit**: Número máximo de mensajes a retornar
    """
    return mensaje_service.obtener_mensajes_conversacion(
        conversacion_id=conversacion_id,
        usuario_id=current_user.id_usuario,
        skip=skip,
        limit=limit
    )


@router.post("/conversaciones/{conversacion_id}/mensajes", response_model=MensajeResponse)
def enviar_mensaje(
    conversacion_id: int,
    data: MensajeCreate,
    current_user: UsuarioResponse = Depends(get_current_user),
    mensaje_service: MensajeService = Depends(get_mensaje_service)
):
    """
    Envía un mensaje en una conversación
    
    - **conversacion_id**: ID de la conversación
    - **contenido**: Contenido del mensaje
    """
    # Validar que el conversacion_id del path coincide con el del body
    if data.conversacion_id != conversacion_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El conversacion_id del path no coincide con el del body"
        )
    
    return mensaje_service.enviar_mensaje(
        conversacion_id=conversacion_id,
        remitente_id=current_user.id_usuario,
        contenido=data.contenido
    )


@router.put("/mensajes/{mensaje_id}/leido", response_model=MensajeResponse)
def marcar_mensaje_leido(
    mensaje_id: int,
    current_user: UsuarioResponse = Depends(get_current_user),
    mensaje_service: MensajeService = Depends(get_mensaje_service)
):
    """
    Marca un mensaje como leído
    
    - **mensaje_id**: ID del mensaje a marcar como leído
    """
    return mensaje_service.marcar_mensaje_leido(
        mensaje_id=mensaje_id,
        usuario_id=current_user.id_usuario
    )

