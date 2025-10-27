from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from core.base import Base
from sqlalchemy.orm import relationship

class Mantenimiento(Base):
    __tablename__ = "Tb_mantenimiento"
    __table_args__ = {'schema': 'MANTENIMIENTO'}

    id_mantenimiento = Column(Integer, primary_key=True, autoincrement=True, index=True)
    descripcion = Column(String(500), nullable=False)
    fecha = Column(DateTime, nullable=True)
    fecha_termino = Column(Date, nullable=True)
    empleado_id = Column(Integer, ForeignKey("EMPLEADOS.Tb_empleado.id_empleado"))

    empleado = relationship("Empleado", back_populates="mantenimientos")

    def __repr__(self):
        return f"<Mantenimiento(id_mantenimiento={self.id_mantenimiento}, descripcion='{self.descripcion}')>"
