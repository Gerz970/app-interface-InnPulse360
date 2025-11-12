from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from core.base import Base


class TipoHabitacion(Base):
    """
    Modelo SQLAlchemy para la tabla HOTEL.Tb_tipoHabitacion
    Refleja exactamente la estructura de la base de datos
    """
    __tablename__ = "Tb_tipoHabitacion"
    __table_args__ = {'schema': 'HOTEL'}
    
    # Campos de la tabla
    id_tipoHabitacion = Column(Integer, primary_key=True, autoincrement=True, index=True)
    clave = Column(String(10), nullable=True)
    precio_unitario = Column(Numeric(18, 2), nullable=False, comment="Precio unitario")
    periodicidad_id = Column(Integer, ForeignKey("CATALOGOS.Tb_periodicidad.id_periodicidad"), nullable=False)
    tipo_habitacion = Column(String(25), nullable=False)
    estatus_id = Column(Integer, nullable=False)
    url_foto_perfil = Column(String(500), nullable=True)
    
    # Relaciones
    periodicidad = relationship("Periodicidad")  # carga la relación con Periodicidad

    caracteristicas = relationship(
        "Caracteristica", 
        secondary="HOTEL.Tb_tipoHabitacionCaracteristicas",
        back_populates="tipos_habitacion"
    )
    
    def __repr__(self):
        return f"<TipoHabitacion(id_tipoHabitacion={self.id_tipoHabitacion}, tipo_habitacion='{self.tipo_habitacion}')>"
