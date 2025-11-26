from sqlalchemy import Column, Integer, String, BigInteger, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from core.base import Base


class MensajeAdjunto(Base):
    """
    Modelo SQLAlchemy para la tabla MENSAJERIA.Tb_MensajeAdjunto
    Refleja exactamente la estructura de la base de datos
    """
    __tablename__ = "Tb_MensajeAdjunto"
    __table_args__ = {'schema': 'MENSAJERIA'}
    
    # Campos de la tabla
    id_adjunto = Column(Integer, primary_key=True, autoincrement=True, index=True)
    mensaje_id = Column(Integer, ForeignKey('MENSAJERIA.Tb_Mensaje.id_mensaje'), nullable=False, index=True)
    nombre_archivo = Column(String(255), nullable=False)
    tipo_archivo = Column(String(50), nullable=False)  # 'imagen', 'pdf', 'documento', etc.
    ruta_archivo = Column(String(500), nullable=False)  # Ruta en Supabase Storage
    tamanio_bytes = Column(BigInteger, nullable=False)
    fecha_subida = Column(DateTime, nullable=False)
    
    # Relaciones
    mensaje = relationship(
        "Mensaje",
        back_populates="adjuntos"
    )
    
    def __repr__(self):
        return f"<MensajeAdjunto(id_adjunto={self.id_adjunto}, mensaje_id={self.mensaje_id}, nombre='{self.nombre_archivo}')>"

