from sqlalchemy import Column, Integer, String
from core.base import Base

class EstatusLimpieza(Base):
    __tablename__ = "Tb_estatus_limpieza"
    __table_args__ = {'schema': 'CAMARISTA'}

    id_estatus_limpieza = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nombre = Column(String(250), nullable=False)
    id_estatus = Column(Integer, nullable=False, default=1)  # 1 = activo, 0 = inactivo

    def __repr__(self):
        return f"<EstatusLimpieza(id={self.id_estatus_limpieza}, nombre='{self.nombre}', estatus={self.id_estatus})>"
