"""
Modelo SQLAlchemy para log de emails enviados
Permite rastrear y auditar todos los correos enviados por el sistema
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, SmallInteger, JSON
from sqlalchemy.sql import func
from core.base import Base


class EmailLog(Base):
    """
    Modelo para log de emails enviados
    Registra todos los correos enviados para auditoría y seguimiento
    """
    __tablename__ = "Tb_email_log"
    __table_args__ = {'schema': 'EMAIL'}
    
    # Campos principales
    id_log = Column(Integer, primary_key=True, autoincrement=True, index=True)
    
    # Información del destinatario
    destinatario_email = Column(String(255), nullable=False, index=True)
    destinatario_nombre = Column(String(255), nullable=True)
    
    # Información del remitente
    remitente_email = Column(String(255), nullable=False)
    remitente_nombre = Column(String(255), nullable=True)
    
    # Contenido del email
    asunto = Column(String(500), nullable=False)
    contenido_html = Column(Text, nullable=True)
    contenido_texto = Column(Text, nullable=True)
    
    # Información de la plantilla utilizada
    id_template = Column(Integer, nullable=True, index=True)  # FK a EmailTemplate
    tipo_email = Column(String(50), nullable=False, index=True)  # welcome_user, password_reset, etc.
    
    # Variables utilizadas en la plantilla (JSON)
    variables_utilizadas = Column(JSON, nullable=True)
    
    # Estado del envío
    estado_envio = Column(String(20), nullable=False, default='pending', index=True)  # pending, sent, failed, retry
    fecha_envio = Column(DateTime(timezone=True), nullable=True)
    fecha_entrega = Column(DateTime(timezone=True), nullable=True)
    
    # Información de errores
    error_mensaje = Column(Text, nullable=True)
    intentos_envio = Column(Integer, nullable=False, default=0)
    max_intentos = Column(Integer, nullable=False, default=3)
    
    # Información del sistema
    ip_origen = Column(String(45), nullable=True)  # IPv4 o IPv6
    user_agent = Column(String(500), nullable=True)
    usuario_id = Column(Integer, nullable=True, index=True)  # Usuario que triggereó el email
    
    # Información de seguimiento
    email_id_externo = Column(String(255), nullable=True)  # ID del proveedor de email (SendGrid, etc.)
    proveedor_email = Column(String(50), nullable=False, default='smtp')  # smtp, sendgrid, ses, etc.
    
    # Metadatos
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now())
    estatus_id = Column(SmallInteger, nullable=False, default=1)  # 1=Activo, 0=Eliminado
    
    def __repr__(self):
        return f"<EmailLog(id={self.id_log}, destinatario='{self.destinatario_email}', estado='{self.estado_envio}')>"
    
    def to_dict(self):
        """
        Convierte el modelo a diccionario para fácil serialización
        """
        return {
            'id_log': self.id_log,
            'destinatario_email': self.destinatario_email,
            'destinatario_nombre': self.destinatario_nombre,
            'remitente_email': self.remitente_email,
            'remitente_nombre': self.remitente_nombre,
            'asunto': self.asunto,
            'id_template': self.id_template,
            'tipo_email': self.tipo_email,
            'variables_utilizadas': self.variables_utilizadas,
            'estado_envio': self.estado_envio,
            'fecha_envio': self.fecha_envio,
            'fecha_entrega': self.fecha_entrega,
            'error_mensaje': self.error_mensaje,
            'intentos_envio': self.intentos_envio,
            'max_intentos': self.max_intentos,
            'ip_origen': self.ip_origen,
            'user_agent': self.user_agent,
            'usuario_id': self.usuario_id,
            'email_id_externo': self.email_id_externo,
            'proveedor_email': self.proveedor_email,
            'fecha_creacion': self.fecha_creacion,
            'fecha_actualizacion': self.fecha_actualizacion,
            'estatus_id': self.estatus_id
        }
    
    def marcar_como_enviado(self):
        """
        Marca el email como enviado exitosamente
        """
        self.estado_envio = 'sent'
        self.fecha_envio = func.now()
        self.intentos_envio += 1
    
    def marcar_como_fallido(self, error_mensaje: str):
        """
        Marca el email como fallido
        """
        self.estado_envio = 'failed'
        self.error_mensaje = error_mensaje
        self.intentos_envio += 1
    
    def puede_reintentar(self) -> bool:
        """
        Verifica si se puede reintentar el envío
        """
        return self.intentos_envio < self.max_intentos and self.estado_envio in ['pending', 'failed']
