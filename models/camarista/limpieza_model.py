from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from core.base import Base

class Limpieza(Base):
    __tablename__ = "Tb_limpieza"
    __table_args__ = {'schema': 'CAMARISTA'}

    id_limpieza = Column(Integer, primary_key=True, autoincrement=True, index=True)
    habitacion_area_id = Column(Integer, ForeignKey("HOTEL.Tb_habitacionArea.id_habitacion_area"), nullable=False)
    descripcion = Column(String(500))
    fecha_programada = Column(DateTime, nullable=False)
    fecha_termino = Column(DateTime)
    tipo_limpieza_id = Column(Integer, ForeignKey("CAMARISTA.Tb_tipos_limpieza.id_tipo_limpieza"), nullable=False)
    estatus_limpieza_id = Column(Integer, ForeignKey("CAMARISTA.Tb_estatus_limpieza.id_estatus_limpieza"), nullable=False)
    comentarios_observaciones = Column(String(500))
    empleado_id = Column(Integer, ForeignKey("EMPLEADOS.Tb_empleado.id_empleado"), nullable=False)

    # Relaciones
    habitacion_area = relationship("HabitacionArea", back_populates="limpiezas")
    tipo_limpieza = relationship("TiposLimpieza", back_populates="limpiezas")
    estatus_limpieza = relationship("EstatusLimpieza")
    empleado = relationship("Empleado", back_populates="limpiezas")

    def __repr__(self):
        return f"<Limpieza(id_limpieza={self.id_limpieza}, estatus_limpieza_id={self.estatus_limpieza_id})>"
