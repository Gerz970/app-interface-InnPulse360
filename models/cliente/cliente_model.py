from sqlalchemy import Column, Integer, String, SmallInteger
from core.base import Base
from sqlalchemy.orm import relationship

class Cliente(Base):
    __tablename__ = "Tb_cliente"
    __table_args__ = {'schema': 'CLIENTE'}

    id_cliente = Column(Integer, primary_key=True, autoincrement=True, index=True)
    tipo_persona = Column(SmallInteger, nullable=False)
    documento_identificacion = Column(String(50), nullable=True)
    nombre_razon_social = Column(String(250), nullable=False)
    apellido_paterno = Column(String(250))
    apellido_materno = Column(String(250))
    rfc = Column(String(13))
    curp = Column(String(18))
    telefono = Column(String(10))
    direccion = Column(String(100))
    pais_id = Column(Integer)
    estado_id = Column(Integer, nullable=True)
    correo_electronico = Column(String(20))
    representante = Column(String(100))
    id_estatus = Column(Integer)

    reservacion = relationship("Reservacion", back_populates="cliente")


