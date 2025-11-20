from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL, SmallInteger, Boolean, Time
from sqlalchemy.orm import relationship
from core.base import Base

class TipoCargo(Base):
    __tablename__ = "Tb_tipo_cargos"
    __table_args__ = {'schema': 'RESERVA'}

    id_tipo = Column(Integer, primary_key=True, autoincrement=True)
    nombre_cargo = Column(String(25), nullable=False)
    descripcion = Column(String(100), nullable=False)
    id_estatus = Column(Integer, nullable=False)
    costo = Column(DECIMAL(18, 2), nullable=False)

    cargos = relationship("Cargo", back_populates="tipo_cargo")

