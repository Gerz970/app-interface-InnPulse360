from sqlalchemy import Column, Integer, String, ForeignKey, SmallInteger
from core.base import Base

class Cliente(Base):
    """
    Modelo SQLAlchemy para la tabla CLIENTE.Tb_cliente
    """
    __tablename__ = "Tb_cliente"
    __table_args__ = {'schema': 'CLIENTE'}

    id_cliente = Column(Integer, primary_key=True, autoincrement=True)
    tipo_persona = Column(SmallInteger, nullable=False, comment="1.- Persona Fisica, 2.- Persona Moral")
    documento_identificacion = Column(Integer, nullable=False)
    nombre_razon = Column(String(250), nullable=False)
    telefono = Column(String(10), nullable=True)
    direccion = Column(String(100), nullable=True)
    pais_id = Column(Integer, nullable=False)
    estado_id = Column(Integer, nullable=False)
    correo_electronico = Column(String(20), nullable=True)
    representante = Column(String(100), nullable=True)
    id_estatus = Column(Integer, nullable=False, default=1)
    
    def __repr__(self):
        return f"<Cliente(id_cliente={self.id_cliente}, nombre_razon='{self.nombre_razon}')>"
