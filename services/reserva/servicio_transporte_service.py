# services/servicio_transporte_service.py
from sqlalchemy.orm import Session
from dao.reserva.dao_servicio_transporte import ServicioTransporteDAO
from schemas.reserva.servicios_transporte_schema import ServicioTransporteCreate, ServicioTransporteUpdate

class ServicioTransporteService:
    def __init__(self):
        self.dao = ServicioTransporteDAO()

    def listar(self, db: Session):
        return self.dao.get_all(db)

    def obtener(self, db: Session, id_servicio: int):
        return self.dao.get_by_id(db, id_servicio)

    def crear(self, db: Session, data: ServicioTransporteCreate):
        return self.dao.create(db, data)

    def actualizar(self, db: Session, id_servicio: int, data: ServicioTransporteUpdate):
        return self.dao.update(db, id_servicio, data)

    def eliminar(self, db: Session, id_servicio: int):
        return self.dao.delete(db, id_servicio)
