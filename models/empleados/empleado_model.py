from sqlalchemy import Column, Integer, String, Date, ForeignKey
from core.base import Base
from sqlalchemy.orm import relationship
from .puesto_model import puesto_empleado

class Empleado(Base):
    __tablename__ = "Tb_empleado"
    __table_args__ = {'schema': 'EMPLEADOS'}

    id_empleado = Column(Integer, primary_key=True, autoincrement=True, index=True)
    clave_empleado = Column(String(25), nullable=False)
    nombre = Column(String(150), nullable=False)
    apellido_paterno = Column(String(50), nullable=False)
    apellido_materno = Column(String(50), nullable=False)
    fecha_nacimiento = Column(Date)
    rfc = Column(String(13), nullable=False)
    curp = Column(String(18), nullable=False)

    domicilio_relacion = relationship("DomicilioEmpleado", back_populates="empleado", uselist=False)

    puestos = relationship(
        "Puesto",
        secondary=puesto_empleado,
        back_populates="empleado"
    )

    def __repr__(self):
        return f"<Empleado(id_empleado={self.id_empleado}, empleado='{self.empleado}')>"
