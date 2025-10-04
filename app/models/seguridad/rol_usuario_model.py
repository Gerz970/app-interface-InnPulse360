from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class RolUsuario(Base):
    """
    Modelo SQLAlchemy para la tabla SEGURIDAD.Tb_rolUsuario
    Tabla intermedia para relación muchos-a-muchos entre Usuario y Roles
    """
    __tablename__ = "Tb_rolUsuario"
    __table_args__ = {'schema': 'SEGURIDAD'}
    
    # Campos de la tabla
    rol_id = Column(
        Integer, 
        ForeignKey('SEGURIDAD.Tb_rol.id_rol'), 
        primary_key=True,
        nullable=False
    )
    usuario_id = Column(
        Integer, 
        ForeignKey('SEGURIDAD.Tb_usuario.id_usuario'), 
        primary_key=True,
        nullable=False
    )
    
    def __repr__(self):
        return f"<RolUsuario(rol_id={self.rol_id}, usuario_id={self.usuario_id})>"
