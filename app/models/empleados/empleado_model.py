from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table
from core.base import Base
from sqlalchemy.orm import relationship
from .puesto_model import puesto_empleado

empresa_empleado = Table(
    "Tb_empresaEmpleados",
    Base.metadata,
    Column("empleado_id", ForeignKey("EMPLEADOS.Tb_empleado.id_empleado"), primary_key=True),
    Column("hotel_id", ForeignKey("HOTEL.Tb_Hotel.id_hotel"), primary_key=True),
    schema="EMPLEADOS"
)

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

    domicilio_relacion = relationship("DomicilioEmpleado", back_populates="empleado", cascade="all, delete-orphan")

    puestos = relationship( 
        "Puesto",
        secondary=puesto_empleado,  # ← Usar el objeto directamente
        back_populates="empleados",
        cascade="all"
    )

    hoteles = relationship(
        "Hotel",
        secondary=empresa_empleado,
        back_populates="empleados"
    )

    @property
    def domicilio(self):
        """Acceso directo al domicilio a través de la tabla intermedia."""
        return self.domicilio_relacion.domicilio if self.domicilio_relacion else None

    def __repr__(self):
        return f"<Empleado(id_empleado={self.id_empleado})>"
