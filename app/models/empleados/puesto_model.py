from sqlalchemy import Column, Integer, String
from core.base import Base

class Puesto(Base):
    __tablename__ = "Tb_puesto"
    __table_args__ = {'schema':'EMPLEADOS'}

    id_puesto = Column(Integer, primary_key=True, autoincrement=True, index=True)
    puesto = Column(String(250), nullable=False)
    descripcion = Column(String(250), nullable=False)
    estatus_id = Column(Integer(), nullable=False)

    def __repr__(self):
        return f"<Puesto(id_puesto={self.id_puesto})"