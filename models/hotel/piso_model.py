from sqlalchemy import Column, Integer, String, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from core.base import Base
from .habitacionArea_model import HabitacionArea

class Piso(Base):
    __tablename__ = "Tb_piso"
    __table_args__ = {'schema': 'HOTEL'}

    id_piso = Column(Integer, primary_key=True, autoincrement=True, index=True)
    id_hotel = Column(Integer, ForeignKey("HOTEL.Tb_Hotel.id_hotel"), nullable=False)
    numero_pisos = Column(SmallInteger, nullable=True)
    nombre = Column(String(50), nullable=False)
    descripcion = Column(String(150), nullable=False)
    estatus_id = Column(SmallInteger, nullable=False)

    # Relación con Hotel (muchos pisos pertenecen a un hotel)
    hotel = relationship("Hotel", back_populates="pisos")
    habitaciones = relationship("HabitacionArea", back_populates="piso", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Piso(id_piso={self.id_piso}, nombre='{self.nombre}')>"
