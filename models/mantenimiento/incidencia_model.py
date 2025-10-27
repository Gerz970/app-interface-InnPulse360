from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from core.base import Base
from sqlalchemy.orm import relationship

class Incidencia(Base):
    __tablename__ = "Tb_incidencia"
    __table_args__ = {'schema': 'MANTENIMIENTO'}

    id_incidencia = Column(Integer, primary_key=True, autoincrement=True, index=True)
    habitacion_area_id = Column(Integer, ForeignKey("HOTEL.Tb_habitacionArea.id_habitacion_area"))
    incidencia = Column(String(50), nullable=False)
    descripcion = Column(String(500))
    fecha_incidencia = Column(DateTime, nullable=False)
    id_estatus = Column(Integer, nullable=False)  # 1: activa, 0: cancelada, 3: atendida

    habitacion_area = relationship("HabitacionArea", back_populates="incidencias")


