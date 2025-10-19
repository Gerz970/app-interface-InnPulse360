from sqlalchemy import Column, Integer, String, SmallInteger
from core.base import Base
from sqlalchemy.orm import relationship
from ..empleados.empleado_model import empresa_empleado

class Hotel(Base):
    """
    Modelo SQLAlchemy para la tabla HOTEL.Tb_Hotel
    Refleja exactamente la estructura de la base de datos
    """
    __tablename__ = "Tb_Hotel"
    __table_args__ = {'schema': 'HOTEL'}
    
    # Campos de la tabla
    id_hotel = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nombre = Column(String(150), nullable=False)
    direccion = Column(String(200), nullable=False)
    id_estado = Column(Integer, nullable=True)
    id_pais = Column(Integer, nullable=False)
    codigo_postal = Column(String(20), nullable=True)
    telefono = Column(String(30), nullable=True)
    email_contacto = Column(String(150), nullable=True)
    numero_estrellas = Column(SmallInteger, nullable=True)
    estatus_id = Column(SmallInteger, nullable=False)
    
    empleados = relationship(
        "Empleado",
        secondary=empresa_empleado,
        back_populates="hoteles"
    )

    pisos = relationship("Piso", back_populates="hotel", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Hotel(id_hotel={self.id_hotel}, nombre='{self.nombre}')>"
