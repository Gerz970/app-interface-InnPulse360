from sqlalchemy import Column, Integer, ForeignKey
from core.base import Base

class CargoServicioTransporte(Base):
    __tablename__ = "Tb_cargo_servicio_transporte"
    __table_args__ = {'schema': 'RESERVA'}
    
    cargo_id = Column(
        Integer, 
        ForeignKey('RESERVA.Tb_cargos.id_cargo'), 
        primary_key=True,
        nullable=False
    )
    servicio_transporte_id = Column(
        Integer, 
        ForeignKey('RESERVA.Tb_ServiciosTransporte.id_servicio_transporte'), 
        primary_key=True,
        nullable=False
    )
    
    def __repr__(self):
        return f"<CargoServicioTransporte(cargo_id={self.cargo_id}, servicio_transporte_id={self.servicio_transporte_id})>"
