from sqlalchemy import Column, Integer, String, SmallInteger
from core.base import Base


class Cliente(Base):
    """
    Modelo SQLAlchemy para la tabla CLIENTE.Tb_cliente
    Refleja exactamente la estructura de la base de datos
    """
    __tablename__ = "Tb_cliente"
    __table_args__ = {'schema': 'CLIENTE'}
    
    # Campos de la tabla
    id_cliente = Column(Integer, primary_key=True, autoincrement=True, index=True)
    tipo_persona = Column(SmallInteger, nullable=False)  # 1=Física, 2=Moral
    documento_identificacion = Column(Integer, nullable=False)
    nombre_razon_social = Column(String(250), nullable=False)
    apellido_paterno = Column(String(250), nullable=True)
    apellido_materno = Column(String(250), nullable=True)
    rfc = Column(String(13), nullable=True, unique=True, index=True)  # Único e indexado
    curp = Column(String(18), nullable=True)
    telefono = Column(String(10), nullable=True)
    direccion = Column(String(100), nullable=True)
    pais_id = Column(Integer, nullable=False)
    estado_id = Column(Integer, nullable=False)
    correo_electronico = Column(String(20), nullable=False)
    representante = Column(String(100), nullable=False)
    id_estatus = Column(Integer, nullable=False)
    
    def __repr__(self):
        return f"<Cliente(id_cliente={self.id_cliente}, nombre_razon_social='{self.nombre_razon_social}')>"
