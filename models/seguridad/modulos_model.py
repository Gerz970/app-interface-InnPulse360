from sqlalchemy import Column, Integer, String, SmallInteger, ForeignKey, Table
from sqlalchemy.orm import relationship
from core.base import Base

# Tabla de asociación para módulos y roles
modulo_rol = Table(
    "Tb_modulo_rol",
    Base.metadata,
    Column("modulo_id", ForeignKey("SEGURIDAD.Tb_Modulos.id_modulo"), primary_key=True),
    Column("rol_id", ForeignKey("SEGURIDAD.Tb_rol.id_rol"), primary_key=True),
    schema="SEGURIDAD"
)

class Modulos(Base):
    """
    Modelo SQLAlchemy para la tabla SEGURIDAD.Tb_Modulos
    Refleja exactamente la estructura de la base de datos
    """
    __tablename__ = "Tb_Modulos"
    __table_args__ = {'schema': 'SEGURIDAD'}
    
    # Campos de la tabla
    id_modulo = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nombre = Column(String(25), nullable=False)
    descripcion = Column(String(100), nullable=True)
    icono = Column(String(25), nullable=True)
    ruta = Column(String(250), nullable=True)
    id_estatus = Column(Integer, nullable=False)
    movil = Column(Integer, nullable=True)
    
    # Relaciones
    roles = relationship(
        "Roles", 
        secondary=modulo_rol, 
        back_populates="modulos"
    )
    
    def __repr__(self):
        return f"<Modulos(id_modulo={self.id_modulo}, nombre='{self.nombre}')>"
