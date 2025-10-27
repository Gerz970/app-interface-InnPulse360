from sqlalchemy import Column, Integer, ForeignKey
from core.base import Base

class IncidenciaMantenimiento(Base):
    __tablename__ = "Tb_incidencia_mantenimiento"
    __table_args__ = {'schema': 'MANTENIMIENTO'}

    incidencia_id = Column(
        Integer, 
        ForeignKey("MANTENIMIENTO.Tb_incidencia.id_incidencia"), 
        primary_key=True
    )
    mantenimiento_id = Column(
        Integer, 
        ForeignKey("MANTENIMIENTO.Tb_mantenimiento.id_mantenimiento"), 
        primary_key=True
    )
