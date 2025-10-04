from sqlalchemy import Column, Integer, ForeignKey
from .base import Base


class TipoHabitacionCaracteristica(Base):
    """
    Modelo SQLAlchemy para la tabla CATALOGOS.Tb_tipoHabitacionCaracteristicas
    Tabla puente para relación muchos-a-muchos entre TipoHabitacion y Caracteristica
    """
    __tablename__ = "Tb_tipoHabitacionCaracteristicas"
    __table_args__ = {'schema': 'CATALOGOS'}
    
    # Campos de la tabla
    tipo_habitacion_id = Column(
        Integer, 
        ForeignKey('CATALOGOS.Tb_tipoHabitacion.id_tipoHabitacion'), 
        primary_key=True,
        nullable=False
    )
    caracteristica_id = Column(
        Integer, 
        ForeignKey('CATALOGOS.Tb_caracteristicas.id_caracteristica'), 
        primary_key=True,
        nullable=False
    )
    
    def __repr__(self):
        return f"<TipoHabitacionCaracteristica(tipo_habitacion_id={self.tipo_habitacion_id}, caracteristica_id={self.caracteristica_id})>"
