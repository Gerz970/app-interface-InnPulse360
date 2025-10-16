from sqlalchemy import Column, Integer, String, ForeignKey, Table
from core.base import Base
from sqlalchemy.orm import relationship

puesto_empleado = Table(
    "Tb_puestoEmpleado",
    Base.metadata,
    Column("empleado_id", ForeignKey("EMPLEADOS.Tb_empleado.id_empleado"), primary_key=True),
    Column("puesto_id", ForeignKey("EMPLEADOS.Tb_puesto.id_puesto"), primary_key=True),
    schema="EMPLEADOS"
)

class Puesto(Base):
    __tablename__ = "Tb_puesto"
    __table_args__ = {'schema':'EMPLEADOS'}

    id_puesto = Column(Integer, primary_key=True, autoincrement=True, index=True)
    puesto = Column(String(250), nullable=False)
    descripcion = Column(String(250), nullable=False)
    estatus_id = Column(Integer(), nullable=False)

    empleado = relationship(
        "Empleado", 
        secondary=puesto_empleado,
        back_populates="puestos"
    )

    def __repr__(self):
        return f"<Puesto(id_puesto={self.id_puesto})"