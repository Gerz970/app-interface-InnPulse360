from sqlalchemy import Column, Integer, String, Boolean
from core.base import Base

class Periodicidad(Base):
    __tablename__ = "Tb_periodicidad"
    __table_args__ = {'schema': 'CATALOGOS'}

    id_periodicidad = Column(Integer, primary_key=True, autoincrement=True, index=True, comment="Identificador de la periodicidad")
    periodicidad = Column(String(50), nullable=False, comment="Nombre de la periodicidad")
    descripcion = Column(String(100), nullable=True, comment="Descripción de la periodicidad")
    id_estatus = Column(Boolean, nullable=False, default=True, comment="Estatus del registro (True=Activo, False=Inactivo)")

    def __repr__(self):
        return f"<Periodicidad(id_periodicidad={self.id_periodicidad}, periodicidad='{self.periodicidad}')>"
