from sqlalchemy import Column, Integer, String, SmallInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


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
        secondary="SEGURIDAD.Tb_rolUsuario", 
        back_populates="roles"
    )

    
    def __repr__(self):
        return f"<Roles(id_rol={self.id_rol}, rol='{self.rol}')>"
