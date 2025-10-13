from sqlalchemy import Column, Integer, ForeignKey
from core.base import Base
from sqlalchemy.orm import relationship

class DomicilioEmpleado(Base):
    __tablename__ = "Tb_domicilioEmpleado"
    __table_args__ = {"schema": "EMPLEADOS"}

    domicilio_id = Column(Integer, ForeignKey("EMPLEADOS.Tb_domicilio.id_id_domicilio"), primary_key=True)
    empleado_id = Column(Integer, ForeignKey("EMPLEADOS.Tb_empleado.id_empleado"), primary_key=True)

    domicilio = relationship("Domicilio", back_populates="empleado_relacion")
    empleado = relationship("Empleado", back_populates="domicilio_relacion")
