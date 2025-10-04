from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base


class TipoHabitacion(Base):
    """
    Modelo SQLAlchemy para la tabla CATALOGOS.Tb_tipoHabitacion
    Refleja exactamente la estructura de la base de datos
    """
    __tablename__ = "Tb_tipoHabitacion"
    __table_args__ = {'schema': 'CATALOGOS'}
    
    # Campos de la tabla
    id_tipoHabitacion = Column(Integer, primary_key=True, autoincrement=True, index=True)
    clave = Column(String(10), nullable=True)
    tipo_habitacion = Column(String(25), nullable=False)
    estatus_id = Column(Integer, nullable=False)
    
    # Relaciones
    caracteristicas = relationship(
        "Caracteristica", 
        secondary="CATALOGOS.Tb_tipoHabitacionCaracteristicas",
        back_populates="tipos_habitacion"
    )
    
    def __repr__(self):
        return f"<TipoHabitacion(id_tipoHabitacion={self.id_tipoHabitacion}, tipo_habitacion='{self.tipo_habitacion}')>"
