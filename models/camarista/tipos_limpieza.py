from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from core.base import Base

class TiposLimpieza(Base):
    __tablename__ = "Tb_tipos_limpieza"
    __table_args__ = {'schema':'CAMARISTA'}

    id_tipo_limpieza = Column(Integer, primary_key=True, autoincrement=True, index= True)
    nombre_tipo = Column(String(25), nullable=False)
    descripcion = Column(String(25), nullable=False)
    id_estatus = Column(Integer, nullable=False)

    
    def __repr__(self):
        return f"<TiposLimpieza(id_tipo_limpieza={self.id_tipo_limpieza}, nombre_tipo='{self.nombre_tipo}')>"
