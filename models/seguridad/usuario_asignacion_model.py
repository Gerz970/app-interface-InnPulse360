from sqlalchemy import Column, Integer, SmallInteger, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from core.base import Base


class UsuarioAsignacion(Base):
    """
    Modelo SQLAlchemy para la tabla SEGURIDAD.Tb_usuarioAsignacion
    Asocia usuarios con empleados o clientes (exclusivo)
    """
    __tablename__ = "Tb_usuarioAsignacion"
    __table_args__ = {'schema': 'SEGURIDAD'}
    
    # Campos de la tabla
    id_asignacion = Column(Integer, primary_key=True, autoincrement=True, index=True)
    usuario_id = Column(Integer, ForeignKey("SEGURIDAD.Tb_usuario.id_usuario"), nullable=False, unique=True)
    empleado_id = Column(Integer, nullable=True)  # FK a empleados (sin definir por ahora)
    cliente_id = Column(Integer, ForeignKey("CLIENTE.Tb_cliente.id_cliente"), nullable=True)
    tipo_asignacion = Column(SmallInteger, nullable=False)  # 1=Empleado, 2=Cliente
    fecha_asignacion = Column(DateTime, default=datetime.utcnow)
    estatus = Column(SmallInteger, default=1)
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="asignacion", uselist=False)
    cliente = relationship("Cliente", backref="usuarios_asignados", foreign_keys=[cliente_id])
    
    def __repr__(self):
        tipo = "Empleado" if self.tipo_asignacion == 1 else "Cliente"
        return f"<UsuarioAsignacion(usuario_id={self.usuario_id}, tipo={tipo})>"
