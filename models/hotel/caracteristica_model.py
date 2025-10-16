from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from core.base import Base


class Caracteristica(Base):
    """
    Modelo SQLAlchemy para la tabla HOTEL.Tb_caracteristicas
    Refleja exactamente la estructura de la base de datos
    """
    __tablename__ = "Tb_caracteristicas"
    __table_args__ = {'schema': 'HOTEL'}
    
    # Campos de la tabla
    id_caracteristica = Column(Integer, primary_key=True, autoincrement=True, index=True)
    caracteristica = Column(String(50), nullable=False)
    descripcion = Column(String(500), nullable=True)
    
    # Relaciones
    tipos_habitacion = relationship(
        "TipoHabitacion", 
        secondary="HOTEL.Tb_tipoHabitacionCaracteristicas",
        back_populates="caracteristicas"
    )
    
    def __repr__(self):
        return f"<Caracteristica(id_caracteristica={self.id_caracteristica}, caracteristica='{self.caracteristica}')>"
