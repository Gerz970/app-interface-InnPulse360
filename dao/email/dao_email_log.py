"""
DAO (Data Access Object) para operaciones CRUD de EmailLog
Maneja todas las interacciones con la base de datos para logs de email
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_, func, desc

from models.email.email_log_model import EmailLog
from schemas.email.email_schemas import EmailSend, EmailStatus


class EmailLogDAO:
    """
    Clase DAO para manejar operaciones CRUD de EmailLog en la base de datos
    """
    
    def __init__(self, db_session: Session):
        """
        Inicializa el DAO con una sesión de base de datos
        
        Args:
            db_session (Session): Sesión de SQLAlchemy
        """
        self.db = db_session
    
    def create_log(self, email_data: EmailSend, **kwargs) -> EmailLog:
        """
        Crea un nuevo log de email
        
        Args:
            email_data (EmailSend): Datos del email
            **kwargs: Datos adicionales del log
            
        Returns:
            EmailLog: Log creado
        """
        try:
            db_log = EmailLog(
                destinatario_email=str(email_data.destinatario_email),
                destinatario_nombre=email_data.destinatario_nombre,
                remitente_email=kwargs.get('remitente_email', ''),
                remitente_nombre=kwargs.get('remitente_nombre', ''),
                asunto=email_data.asunto,
                contenido_html=email_data.contenido_html,
                contenido_texto=email_data.contenido_texto,
                id_template=email_data.id_template,
                tipo_email=email_data.tipo_email,
                variables_utilizadas=email_data.variables,
                estado_envio=EmailStatus.PENDING,
                ip_origen=kwargs.get('ip_origen'),
                user_agent=kwargs.get('user_agent'),
                usuario_id=kwargs.get('usuario_id'),
                proveedor_email=kwargs.get('proveedor_email', 'smtp'),
                max_intentos=kwargs.get('max_intentos', 3),
                estatus_id=1
            )
            
            self.db.add(db_log)
            self.db.commit()
            self.db.refresh(db_log)
            
            return db_log
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def get_by_id(self, log_id: int) -> Optional[EmailLog]:
        """
        Obtiene un log por ID
        
        Args:
            log_id (int): ID del log
            
        Returns:
            Optional[EmailLog]: Log encontrado o None
        """
        return self.db.query(EmailLog).filter(
            and_(
                EmailLog.id_log == log_id,
                EmailLog.estatus_id == 1
            )
        ).first()
    
    def update_status(self, log_id: int, estado: EmailStatus, 
                     error_mensaje: Optional[str] = None,
                     email_id_externo: Optional[str] = None) -> bool:
        """
        Actualiza el estado de un log de email
        
        Args:
            log_id (int): ID del log
            estado (EmailStatus): Nuevo estado
            error_mensaje (Optional[str]): Mensaje de error si aplica
            email_id_externo (Optional[str]): ID externo del proveedor
            
        Returns:
            bool: True si se actualizó correctamente
        """
        try:
            db_log = self.get_by_id(log_id)
            if not db_log:
                return False
            
            db_log.estado_envio = estado
            db_log.intentos_envio += 1
            
            if estado == EmailStatus.SENT:
                db_log.fecha_envio = func.now()
            elif estado == EmailStatus.DELIVERED:
                db_log.fecha_entrega = func.now()
            elif estado == EmailStatus.FAILED:
                db_log.error_mensaje = error_mensaje
            
            if email_id_externo:
                db_log.email_id_externo = email_id_externo
            
            self.db.commit()
            return True
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def get_pending_emails(self, limit: int = 100) -> List[EmailLog]:
        """
        Obtiene emails pendientes de envío
        
        Args:
            limit (int): Límite de registros
            
        Returns:
            List[EmailLog]: Lista de emails pendientes
        """
        return self.db.query(EmailLog).filter(
            and_(
                EmailLog.estado_envio == EmailStatus.PENDING,
                EmailLog.estatus_id == 1
            )
        ).order_by(EmailLog.fecha_creacion).limit(limit).all()
    
    def get_failed_retryable(self, limit: int = 50) -> List[EmailLog]:
        """
        Obtiene emails fallidos que pueden reintentarse
        
        Args:
            limit (int): Límite de registros
            
        Returns:
            List[EmailLog]: Lista de emails para reintentar
        """
        return self.db.query(EmailLog).filter(
            and_(
                EmailLog.estado_envio == EmailStatus.FAILED,
                EmailLog.intentos_envio < EmailLog.max_intentos,
                EmailLog.estatus_id == 1
            )
        ).order_by(EmailLog.fecha_creacion).limit(limit).all()
    
    def get_by_user(self, usuario_id: int, skip: int = 0, limit: int = 50) -> List[EmailLog]:
        """
        Obtiene logs de email por usuario
        
        Args:
            usuario_id (int): ID del usuario
            skip (int): Registros a saltar
            limit (int): Límite de registros
            
        Returns:
            List[EmailLog]: Lista de logs
        """
        return self.db.query(EmailLog).filter(
            and_(
                EmailLog.usuario_id == usuario_id,
                EmailLog.estatus_id == 1
            )
        ).order_by(desc(EmailLog.fecha_creacion)).offset(skip).limit(limit).all()
    
    def get_by_email(self, email: str, skip: int = 0, limit: int = 50) -> List[EmailLog]:
        """
        Obtiene logs por email destinatario
        
        Args:
            email (str): Email del destinatario
            skip (int): Registros a saltar
            limit (int): Límite de registros
            
        Returns:
            List[EmailLog]: Lista de logs
        """
        return self.db.query(EmailLog).filter(
            and_(
                EmailLog.destinatario_email == email,
                EmailLog.estatus_id == 1
            )
        ).order_by(desc(EmailLog.fecha_creacion)).offset(skip).limit(limit).all()
    
    def get_by_type(self, tipo_email: str, skip: int = 0, limit: int = 100) -> List[EmailLog]:
        """
        Obtiene logs por tipo de email
        
        Args:
            tipo_email (str): Tipo de email
            skip (int): Registros a saltar
            limit (int): Límite de registros
            
        Returns:
            List[EmailLog]: Lista de logs
        """
        return self.db.query(EmailLog).filter(
            and_(
                EmailLog.tipo_email == tipo_email,
                EmailLog.estatus_id == 1
            )
        ).order_by(desc(EmailLog.fecha_creacion)).offset(skip).limit(limit).all()
    
    def get_stats_by_period(self, days: int = 30) -> Dict[str, Any]:
        """
        Obtiene estadísticas de emails por período
        
        Args:
            days (int): Días hacia atrás
            
        Returns:
            Dict[str, Any]: Estadísticas
        """
        fecha_inicio = datetime.utcnow() - timedelta(days=days)
        
        # Total de emails
        total_query = self.db.query(func.count(EmailLog.id_log)).filter(
            and_(
                EmailLog.fecha_creacion >= fecha_inicio,
                EmailLog.estatus_id == 1
            )
        )
        
        # Por estado
        estados_query = self.db.query(
            EmailLog.estado_envio,
            func.count(EmailLog.id_log).label('count')
        ).filter(
            and_(
                EmailLog.fecha_creacion >= fecha_inicio,
                EmailLog.estatus_id == 1
            )
        ).group_by(EmailLog.estado_envio)
        
        # Por tipo
        tipos_query = self.db.query(
            EmailLog.tipo_email,
            func.count(EmailLog.id_log).label('count')
        ).filter(
            and_(
                EmailLog.fecha_creacion >= fecha_inicio,
                EmailLog.estatus_id == 1
            )
        ).group_by(EmailLog.tipo_email)
        
        total = total_query.scalar() or 0
        estados = {row.estado_envio: row.count for row in estados_query.all()}
        tipos = {row.tipo_email: row.count for row in tipos_query.all()}
        
        # Calcular tasa de entrega
        enviados = estados.get(EmailStatus.SENT, 0) + estados.get(EmailStatus.DELIVERED, 0)
        tasa_entrega = (enviados / total * 100) if total > 0 else 0
        
        return {
            'total_emails': total,
            'por_estado': estados,
            'por_tipo': tipos,
            'tasa_entrega': round(tasa_entrega, 2),
            'periodo_dias': days
        }
    
    def cleanup_old_logs(self, days_to_keep: int = 90) -> int:
        """
        Limpia logs antiguos (eliminación lógica)
        
        Args:
            days_to_keep (int): Días a mantener
            
        Returns:
            int: Número de logs eliminados
        """
        try:
            fecha_limite = datetime.utcnow() - timedelta(days=days_to_keep)
            
            result = self.db.query(EmailLog).filter(
                and_(
                    EmailLog.fecha_creacion < fecha_limite,
                    EmailLog.estatus_id == 1
                )
            ).update({"estatus_id": 0})
            
            self.db.commit()
            return result
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def get_recent_errors(self, hours: int = 24, limit: int = 50) -> List[EmailLog]:
        """
        Obtiene errores recientes
        
        Args:
            hours (int): Horas hacia atrás
            limit (int): Límite de registros
            
        Returns:
            List[EmailLog]: Lista de logs con errores
        """
        fecha_inicio = datetime.utcnow() - timedelta(hours=hours)
        
        return self.db.query(EmailLog).filter(
            and_(
                EmailLog.estado_envio == EmailStatus.FAILED,
                EmailLog.fecha_creacion >= fecha_inicio,
                EmailLog.estatus_id == 1
            )
        ).order_by(desc(EmailLog.fecha_creacion)).limit(limit).all()
    
    def mark_as_retry(self, log_id: int) -> bool:
        """
        Marca un email para reintento
        
        Args:
            log_id (int): ID del log
            
        Returns:
            bool: True si se marcó correctamente
        """
        try:
            db_log = self.get_by_id(log_id)
            if not db_log or not db_log.puede_reintentar():
                return False
            
            db_log.estado_envio = EmailStatus.RETRY
            db_log.error_mensaje = None
            
            self.db.commit()
            return True
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
