"""
Rutas API para envío de emails
Endpoint básico para testing de envío de correos
"""

from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import Dict, Any, List, Optional

from services.email.email_service import EmailService
from schemas.email.email_basic_schemas import EmailSendBasic, EmailResponseBasic
from schemas.email.email_schemas import EmailLogResponse
from dao.email.dao_email_log import EmailLogDAO
from core.database_connection import get_database_session

# Crear router
router = APIRouter(
    prefix="/emails",
    tags=["Emails"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/send",
    response_model=EmailResponseBasic,
    status_code=status.HTTP_200_OK,
    summary="Enviar Email",
    description="Endpoint básico para envío de emails. Útil para testing del servicio SMTP."
)
async def send_email(email_data: EmailSendBasic) -> EmailResponseBasic:
    """
    Envía un email usando el servicio SMTP configurado
    
    Args:
        email_data (EmailSendBasic): Datos del email a enviar
        
    Returns:
        EmailResponseBasic: Resultado del envío
        
    Raises:
        HTTPException: Si hay error en el procesamiento
        
    Example:
        ```json
        {
            "destinatario_email": "usuario@ejemplo.com",
            "asunto": "Prueba de Email",
            "contenido_html": "<h1>Hola</h1><p>Este es un email de prueba.</p>"
        }
        ```
    """
    try:
        # Crear instancia del servicio
        email_service = EmailService()
        
        # Enviar email
        result = await email_service.send_email(email_data)
        
        # Si falló el envío, retornar error
        if not result.success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "message": result.message,
                    "error": result.error
                }
            )
        
        return result
        
    except HTTPException:
        raise
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Error al procesar el envío de email",
                "error": str(e)
            }
        )


@router.post(
    "/send-welcome",
    response_model=EmailResponseBasic,
    status_code=status.HTTP_200_OK,
    summary="Enviar Email de Bienvenida",
    description="Envía email de bienvenida usando plantilla específica"
)
async def send_welcome_email(
    destinatario_email: str,
    destinatario_nombre: str,
    usuario_email: str,
    codigo_activacion: Optional[str] = None
) -> EmailResponseBasic:
    """
    Envía email de bienvenida usando plantilla específica
    
    Args:
        destinatario_email: Email del destinatario
        destinatario_nombre: Nombre del destinatario
        usuario_email: Email del usuario
        codigo_activacion: Código de activación opcional
        
    Returns:
        EmailResponseBasic: Resultado del envío
    """
    try:
        email_service = EmailService()
        result = await email_service.send_welcome_email(
            destinatario_email, destinatario_nombre, usuario_email, codigo_activacion
        )
        
        if not result.success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "message": result.message,
                    "error": result.error
                }
            )
        
        return result
        
    except HTTPException:
        raise
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Error al procesar el envío de email de bienvenida",
                "error": str(e)
            }
        )


@router.post(
    "/send-password-reset",
    response_model=EmailResponseBasic,
    status_code=status.HTTP_200_OK,
    summary="Enviar Email de Restablecimiento",
    description="Envía email de restablecimiento de contraseña"
)
async def send_password_reset_email(
    destinatario_email: str,
    destinatario_nombre: str,
    reset_token: str
) -> EmailResponseBasic:
    """
    Envía email de restablecimiento de contraseña
    
    Args:
        destinatario_email: Email del destinatario
        destinatario_nombre: Nombre del destinatario
        reset_token: Token para restablecer contraseña
        
    Returns:
        EmailResponseBasic: Resultado del envío
    """
    try:
        email_service = EmailService()
        result = await email_service.send_password_reset_email(
            destinatario_email, destinatario_nombre, reset_token
        )
        
        if not result.success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "message": result.message,
                    "error": result.error
                }
            )
        
        return result
        
    except HTTPException:
        raise
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Error al procesar el envío de email de restablecimiento",
                "error": str(e)
            }
        )


@router.post(
    "/send-role-assignment",
    response_model=EmailResponseBasic,
    status_code=status.HTTP_200_OK,
    summary="Enviar Email de Asignación de Rol",
    description="Envía email de asignación de rol"
)
async def send_role_assignment_email(
    destinatario_email: str,
    destinatario_nombre: str,
    rol_asignado: str,
    asignado_por: str
) -> EmailResponseBasic:
    """
    Envía email de asignación de rol
    
    Args:
        destinatario_email: Email del destinatario
        destinatario_nombre: Nombre del destinatario
        rol_asignado: Rol que se asignó
        asignado_por: Quién asignó el rol
        
    Returns:
        EmailResponseBasic: Resultado del envío
    """
    try:
        email_service = EmailService()
        result = await email_service.send_role_assignment_email(
            destinatario_email, destinatario_nombre, rol_asignado, asignado_por
        )
        
        if not result.success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "message": result.message,
                    "error": result.error
                }
            )
        
        return result
        
    except HTTPException:
        raise
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Error al procesar el envío de email de asignación de rol",
                "error": str(e)
            }
        )


@router.get(
    "/test-connection",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="Probar Conexión SMTP",
    description="Prueba la conexión al servidor SMTP configurado"
)
async def test_smtp_connection() -> Dict[str, Any]:
    """
    Prueba la conexión al servidor SMTP
    
    Returns:
        Dict: Resultado de la prueba de conexión
        
    Raises:
        HTTPException: Si hay error en la conexión
    """
    try:
        email_service = EmailService()
        result = email_service.test_connection()
        
        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result
            )
        
        return result
        
    except HTTPException:
        raise
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "message": f"Error al probar conexión: {str(e)}"
            }
        )


@router.get(
    "/logs",
    response_model=List[EmailLogResponse],
    status_code=status.HTTP_200_OK,
    summary="Obtener Logs de Email",
    description="Obtiene los logs de emails enviados con filtros opcionales"
)
async def get_email_logs(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(50, ge=1, le=100, description="Número de registros a retornar"),
    email: Optional[str] = Query(None, description="Filtrar por email destinatario"),
    estado: Optional[str] = Query(None, description="Filtrar por estado"),
    db: Any = Depends(get_database_session)
) -> List[EmailLogResponse]:
    """
    Obtiene los logs de emails enviados
    
    Args:
        skip: Número de registros a saltar
        limit: Número de registros a retornar
        email: Email del destinatario para filtrar
        estado: Estado del email para filtrar
        
    Returns:
        List[EmailLogResponse]: Lista de logs de email
        
    Raises:
        HTTPException: Si hay error al obtener los logs
    """
    try:
        email_dao = EmailLogDAO(db)
        
        if email:
            logs = email_dao.get_by_email(email, skip, limit)
        else:
            # Obtener logs recientes - usar query directo
            from models.email.email_log_model import EmailLog
            logs = db.query(EmailLog).filter(
                EmailLog.estatus_id == 1
            ).order_by(
                EmailLog.fecha_creacion.desc()
            ).offset(skip).limit(limit).all()
        
        # Filtrar por estado si se proporciona
        if estado:
            logs = [log for log in logs if log.estado_envio == estado]
        
        return logs
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Error al obtener logs de email",
                "error": str(e)
            }
        )


@router.get(
    "/logs/stats",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="Estadísticas de Email",
    description="Obtiene estadísticas de emails enviados"
)
async def get_email_stats(
    days: int = Query(30, ge=1, le=365, description="Días hacia atrás para estadísticas"),
    db: Any = Depends(get_database_session)
) -> Dict[str, Any]:
    """
    Obtiene estadísticas de emails enviados
    
    Args:
        days: Número de días hacia atrás para las estadísticas
        
    Returns:
        Dict[str, Any]: Estadísticas de email
        
    Raises:
        HTTPException: Si hay error al obtener estadísticas
    """
    try:
        email_dao = EmailLogDAO(db)
        stats = email_dao.get_stats_by_period(days)
        return stats
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Error al obtener estadísticas de email",
                "error": str(e)
            }
        )
