from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from core.base import Base


class Pais(Base):
    """
    Modelo SQLAlchemy para la tabla CATALOGOS.Tb_pais
    Refleja exactamente la estructura de la base de datos
    """
    __tablename__ = "Tb_pais"
    __table_args__ = {'schema': 'CATALOGOS'}
    
    # Campos de la tabla
    id_pais = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nombre = Column(String(250), nullable=False)
    id_estatus = Column(Integer, nullable=False)
    
    # Relaciones
    estados = relationship(
        "Estado", 
        back_populates="pais",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<Pais(id_pais={self.id_pais}, nombre='{self.nombre}')>"
