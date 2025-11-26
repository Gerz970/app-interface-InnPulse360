from sqlalchemy import Column, Integer, Text, DateTime, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from core.base import Base


class Mensaje(Base):
    """
    Modelo SQLAlchemy para la tabla MENSAJERIA.Tb_Mensaje
    Refleja exactamente la estructura de la base de datos
    """
    __tablename__ = "Tb_Mensaje"
    __table_args__ = {'schema': 'MENSAJERIA'}
    
    # Campos de la tabla
    id_mensaje = Column(Integer, primary_key=True, autoincrement=True, index=True)
    conversacion_id = Column(Integer, ForeignKey('MENSAJERIA.Tb_Conversacion.id_conversacion'), nullable=False, index=True)
    remitente_id = Column(Integer, ForeignKey('SEGURIDAD.Tb_usuario.id_usuario'), nullable=False, index=True)
    contenido = Column(Text, nullable=False)
    fecha_envio = Column(DateTime, nullable=False, index=True)
    fecha_leido = Column(DateTime, nullable=True, index=True)
    id_estatus = Column(SmallInteger, nullable=False, default=1, index=True)  # 1=Enviado, 2=Leído, 3=Eliminado
    
    # Relaciones
    conversacion = relationship(
        "Conversacion",
        back_populates="mensajes"
    )
    
    remitente = relationship(
        "Usuario",
        backref="mensajes_enviados"
    )
    
    adjuntos = relationship(
        "MensajeAdjunto",
        back_populates="mensaje",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<Mensaje(id_mensaje={self.id_mensaje}, conversacion_id={self.conversacion_id})>"

