from sqlalchemy import Column, Integer, String
from core.base import Base
from sqlalchemy.orm import relationship

class Domicilio(Base):
    __tablename__ = "Tb_domicilio"
    __table_args__ = {"schema": "EMPLEADOS"}

    id_domicilio = Column("id_id_domicilio", Integer, primary_key=True, index=True)
    domicilio_completo = Column(String(250))
    codigo_postal = Column(String(10))
    estatus_id = Column(Integer)

    empleado_relacion = relationship("DomicilioEmpleado", back_populates="domicilio")
