from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL, SmallInteger, Boolean, Time, Text
from sqlalchemy.orm import relationship
from core.base import Base

class Reservacion(Base):
    __tablename__ = "Tb_reservaciones"
    __table_args__ = {'schema': 'RESERVA'}

    id_reservacion = Column(Integer, primary_key=True, autoincrement=True, index=True)
    cliente_id = Column(Integer, ForeignKey("CLIENTE.Tb_cliente.id_cliente"), unique=True)
    habitacion_area_id = Column(Integer, ForeignKey("HOTEL.Tb_habitacionArea.id_habitacion_area"), nullable=False)
    fecha_reserva = Column(DateTime, nullable=False)
    fecha_salida = Column(DateTime, nullable=False)
    duracion = Column(Integer)
    id_estatus = Column(Integer, nullable=False)
    fecha_registro = Column(DateTime, nullable=True)
    codigo_reservacion = Column(String(50), nullable=True)
    comentarios = Column(Text, nullable=True)

    cargos = relationship("Cargo", back_populates="reservacion", cascade="all, delete-orphan")
    habitacion = relationship("HabitacionArea", back_populates="reservas")
    cliente = relationship("Cliente", back_populates="reservacion", uselist=False)

