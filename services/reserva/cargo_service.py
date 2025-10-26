from sqlalchemy.orm import Session
from dao.reserva.dao_cargo import CargoDAO
from schemas.reserva.cargos_schema import CargoCreate


class CargoService:
    def __init__(self):
        self.dao = CargoDAO()

    def listar_todos(self, db: Session):
        return self.dao.get_all(db)

    def obtener_por_id(self, db: Session, id_cargo: int):
        return self.dao.get_by_id(db, id_cargo)

    def obtener_por_id_reserva(self, db: Session, id_reserva: int):
        return self.dao.get_by_id_reserva(db, id_reserva)
    
    def crear(self, db: Session, cargo_data: CargoCreate):
        return self.dao.create(db, cargo_data)

    def actualizar(self, db: Session, id_cargo: int, cargo_data: CargoCreate):
        return self.dao.update(db, id_cargo, cargo_data)

    def eliminar(self, db: Session, id_cargo: int):
        return self.dao.delete(db, id_cargo)
