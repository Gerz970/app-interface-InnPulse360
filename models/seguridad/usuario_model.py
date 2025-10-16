from sqlalchemy import Column, Integer, String, SmallInteger
from sqlalchemy.orm import relationship
from core.base import Base
from .roles_model import rol_usuario



class Usuario(Base):
    """
    Modelo SQLAlchemy para la tabla SEGURIDAD.Tb_Usuario
    Refleja exactamente la estructura de la base de datos
    """
    __tablename__ = "Tb_usuario"
    __table_args__ = {'schema': 'SEGURIDAD'}
    
    # Campos de la tabla
    id_usuario = Column(Integer, primary_key=True, autoincrement=True, index=True)
    login = Column(String(25), nullable=False)
    correo_electronico = Column(String(50), nullable=False)
    password = Column(String(1000), nullable=False)
    estatus_id = Column(SmallInteger, nullable=False)
    
    # Relaciones
    roles = relationship(
        "Roles", 
        secondary=rol_usuario, 
        back_populates="usuarios"
    )

    
    def __repr__(self):
        return f"<Usuario(id_usuario={self.id_usuario}, login='{self.login}')>"
