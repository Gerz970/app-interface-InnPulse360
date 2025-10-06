from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.base import Base


class Estado(Base):
    """
    Modelo SQLAlchemy para la tabla CATALOGOS.Tb_estado
    Refleja exactamente la estructura de la base de datos
    """
    __tablename__ = "Tb_estado"
    __table_args__ = {'schema': 'CATALOGOS'}
    
    # Campos de la tabla
    id_estado = Column(Integer, primary_key=True, autoincrement=True, index=True)
    id_pais = Column(Integer, ForeignKey('CATALOGOS.Tb_pais.id_pais'), nullable=False)
    nombre = Column(String(250), nullable=False)
    id_estatus = Column(Integer, nullable=False)
    
    # Relaciones
    pais = relationship("Pais", back_populates="estados")
    
    def __repr__(self):
        return f"<Estado(id_estado={self.id_estado}, nombre='{self.nombre}', id_pais={self.id_pais})>"
