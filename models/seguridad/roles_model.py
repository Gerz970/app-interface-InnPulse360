from sqlalchemy import Column, Integer, String, SmallInteger, ForeignKey, Table
from sqlalchemy.orm import relationship
from core.base import Base

# Tabla de asociación
rol_usuario = Table(
    "Tb_rolUsuario",
    Base.metadata,
    Column("usuario_id", ForeignKey("SEGURIDAD.Tb_usuario.id_usuario"), primary_key=True),
    Column("rol_id", ForeignKey("SEGURIDAD.Tb_rol.id_rol"), primary_key=True),
    schema="SEGURIDAD"
)

class Roles(Base):
    """
    Modelo SQLAlchemy para la tabla SEGURIDAD.Tb_Roles
    Refleja exactamente la estructura de la base de datos
    """
    __tablename__ = "Tb_rol"
    __table_args__ = {'schema': 'SEGURIDAD'}
    
    # Campos de la tabla
    id_rol = Column(Integer, primary_key=True, autoincrement=True, index=True)
    rol = Column(String(50), nullable=False)
    descripcion = Column(String(250), nullable=False)
    estatus_id = Column(SmallInteger, nullable=False)
    
    # Relaciones
    usuarios = relationship(
        "Usuario", 
        secondary=rol_usuario, 
        back_populates="roles"
    )

    def __repr__(self):
        return f"<Roles(id_rol={self.id_rol}, rol='{self.rol}')>"
