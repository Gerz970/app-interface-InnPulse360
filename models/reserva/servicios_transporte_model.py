from sqlalchemy import Column, Integer, String, Date, Time, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from core.base import Base

class ServicioTransporte(Base):
    __tablename__ = "Tb_ServiciosTransporte"
    __table_args__ = {'schema': 'RESERVA'}

    id_servicio_transporte = Column(Integer, primary_key=True, autoincrement=True)
    destino = Column(String(250), nullable=False)
    fecha_servicio = Column(Date, nullable=False)
    hora_servicio = Column(Time, nullable=False)
    id_estatus = Column(SmallInteger, nullable=False, default=1)  # 1 = activo, 0 = eliminado
    empleado_id = Column(Integer, ForeignKey("EMPLEADOS.Tb_empleado.id_empleado"), primary_key=True) 
    observaciones_cliente = Column(String(500))
    observaciones_empleado = Column(String(500))
    calificacion_viaje = Column(SmallInteger)

    cargo = relationship(
        "Cargo",
        secondary="RESERVA.Tb_cargo_servicio_transporte",
        back_populates="servicios_transporte"
    )

    empleado = relationship("Empleado", back_populates="servicios_transporte")

    from models.reserva.cargos_model import Cargo
