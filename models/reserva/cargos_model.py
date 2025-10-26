from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL, SmallInteger, Boolean, Time
from sqlalchemy.orm import relationship
from core.base import Base

class Cargo(Base):
    __tablename__ = "Tb_cargos"
    __table_args__ = {'schema': 'RESERVA'}

    id_cargo = Column(Integer, primary_key=True, autoincrement=True)
    reservacion_id = Column(Integer, ForeignKey("RESERVA.Tb_reservaciones.id_reservacion"))
    concepto = Column(String(250), nullable=False)
    costo_unitario = Column(DECIMAL(18, 2), nullable=False)
    cantidad = Column(Integer, nullable=False)
    tipo_id = Column(Integer, ForeignKey("RESERVA.Tb_tipo_cargos.id_tipo"))

    tipo_cargo = relationship("TipoCargo", back_populates="cargos",uselist=False)
    reservacion = relationship("Reservacion", back_populates="cargos")
