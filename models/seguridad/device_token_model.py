from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from core.base import Base
from datetime import datetime


class DeviceToken(Base):
    """
    Modelo SQLAlchemy para la tabla SEGURIDAD.Tb_device_token
    Almacena tokens de dispositivos para notificaciones push FCM
    """
    __tablename__ = "Tb_device_token"
    __table_args__ = {'schema': 'SEGURIDAD'}
    
    id_device_token = Column(Integer, primary_key=True, autoincrement=True, index=True)
    usuario_id = Column(Integer, ForeignKey("SEGURIDAD.Tb_usuario.id_usuario"), nullable=False, index=True)
    device_token = Column(String(500), nullable=False, unique=True)
    plataforma = Column(String(20), nullable=False)  # 'android' o 'ios'
    fecha_registro = Column(DateTime, nullable=False, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    activo = Column(Boolean, nullable=False, default=True)
    
    # Relación con Usuario
    usuario = relationship("Usuario", backref="device_tokens")
    
    def __repr__(self):
        return f"<DeviceToken(id_device_token={self.id_device_token}, usuario_id={self.usuario_id}, plataforma='{self.plataforma}')>"

