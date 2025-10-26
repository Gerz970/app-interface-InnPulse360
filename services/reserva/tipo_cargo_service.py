from sqlalchemy.orm import Session
from dao.reserva.dao_tipo_cargo import TipoCargoDAO
from schemas.reserva.tipo_cargo_schema import TipoCargoCreate, TipoCargoUpdate


class TipoCargoService:
    def __init__(self):
        self.dao = TipoCargoDAO()

    def listar_todos(self, db: Session):
        return self.dao.get_all(db)

    def obtener_por_id(self, db: Session, id_tipo: int):
        return self.dao.get_by_id(db, id_tipo)

    def crear(self, db: Session, tipo_data: TipoCargoCreate):
        return self.dao.create(db, tipo_data)

    def actualizar(self, db: Session, id_tipo: int, tipo_data: TipoCargoUpdate):
        return self.dao.update(db, id_tipo, tipo_data)

    def eliminar(self, db: Session, id_tipo: int):
        return self.dao.delete(db, id_tipo)
