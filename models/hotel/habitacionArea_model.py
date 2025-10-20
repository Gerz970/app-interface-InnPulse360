from sqlalchemy import Column, Integer, String, SmallInteger, ForeignKey
from core.base import Base
from sqlalchemy.orm import relationship

class HabitacionArea(Base):
    __tablename__ = "Tb_habitacionArea"
    __table_args__ = {'schema': 'HOTEL'}
    
    # Campos de la tabla
    id_habitacion_area = Column(Integer, primary_key=True, autoincrement=True, index=True)
    piso_id = Column(Integer, ForeignKey("HOTEL.Tb_piso.id_piso"), nullable=False)
    tipo_habitacion_id = Column(Integer, ForeignKey("HOTEL.Tb_tipoHabitacion.id_tipoHabitacion"), nullable=False)
    nombre_clave = Column(String(25), nullable=False)
    descripcion = Column(String(150), nullable=False)
    estatus_id = Column(SmallInteger, nullable=False)

    piso = relationship("Piso", back_populates="habitaciones")
    tipo_habitacion = relationship("TipoHabitacion")

    def __repr__(self):
        return f"<HabitacionArea(id={self.id_habitacion_area}, nombre_clave='{self.nombre_clave}')>"