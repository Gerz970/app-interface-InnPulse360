from sqlalchemy import Column, Integer, String, DateTime, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from core.base import Base


class Conversacion(Base):
    """
    Modelo SQLAlchemy para la tabla MENSAJERIA.Tb_Conversacion
    Refleja exactamente la estructura de la base de datos
    """
    __tablename__ = "Tb_Conversacion"
    __table_args__ = {'schema': 'MENSAJERIA'}
    
    # Campos de la tabla
    id_conversacion = Column(Integer, primary_key=True, autoincrement=True, index=True)
    tipo_conversacion = Column(String(20), nullable=False)  # 'cliente_admin', 'empleado_empleado'
    usuario1_id = Column(Integer, ForeignKey('SEGURIDAD.Tb_usuario.id_usuario'), nullable=False, index=True)
    usuario2_id = Column(Integer, ForeignKey('SEGURIDAD.Tb_usuario.id_usuario'), nullable=False, index=True)
    cliente_id = Column(Integer, ForeignKey('CLIENTE.Tb_cliente.id_cliente'), nullable=True, index=True)
    empleado1_id = Column(Integer, ForeignKey('EMPLEADOS.Tb_empleado.id_empleado'), nullable=True, index=True)
    empleado2_id = Column(Integer, ForeignKey('EMPLEADOS.Tb_empleado.id_empleado'), nullable=True, index=True)
    fecha_creacion = Column(DateTime, nullable=False)
    fecha_ultimo_mensaje = Column(DateTime, nullable=True, index=True)
    id_estatus = Column(SmallInteger, nullable=False, default=1, index=True)  # 1=Activa, 0=Archivada
    
    # Relaciones
    usuario1 = relationship(
        "Usuario",
        foreign_keys=[usuario1_id],
        backref="conversaciones_como_usuario1"
    )
    
    usuario2 = relationship(
        "Usuario",
        foreign_keys=[usuario2_id],
        backref="conversaciones_como_usuario2"
    )
    
    cliente = relationship(
        "Cliente",
        backref="conversaciones"
    )
    
    empleado1 = relationship(
        "Empleado",
        foreign_keys=[empleado1_id],
        backref="conversaciones_como_empleado1"
    )
    
    empleado2 = relationship(
        "Empleado",
        foreign_keys=[empleado2_id],
        backref="conversaciones_como_empleado2"
    )
    
    mensajes = relationship(
        "Mensaje",
        back_populates="conversacion",
        cascade="all, delete-orphan",
        order_by="desc(Mensaje.fecha_envio)"
    )
    
    def __repr__(self):
        return f"<Conversacion(id_conversacion={self.id_conversacion}, tipo='{self.tipo_conversacion}')>"

