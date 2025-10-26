from sqlalchemy.orm import Session
from dao.reserva.dao_cargo import CargoDAO
from dao.reserva.dao_cargo_servicio_transporte import CargoServicioTransporteDao
from schemas.reserva.cargos_schema import CargoCreate
from models.reserva.cargo_servicio_transporte_model import CargoServicioTransporte

class CargoService:
    def __init__(self):
        self.dao = CargoDAO()
        self.relacion_dao = CargoServicioTransporteDao()

    def listar_todos(self, db: Session):
        return self.dao.get_all(db)

    def obtener_por_id(self, db: Session, id_cargo: int):
        return self.dao.get_by_id(db, id_cargo)

    def obtener_por_id_reserva(self, db: Session, id_reserva: int):
        return self.dao.get_by_id_reserva(db, id_reserva)
    
    def crear(self, db: Session, cargo_data: CargoCreate):
        return self.dao.create(db, cargo_data)
    
    def crearCargoConServicio(self, db: Session, cargo_data: CargoCreate, servicio_transporte_id: int):
        """
        Crea un nuevo cargo y lo asocia con un servicio de transporte.
        """
        nuevo_cargo = self.dao.create(db, cargo_data)

        relacion = CargoServicioTransporte(
            cargo_id=nuevo_cargo.id_cargo,
            servicio_transporte_id=servicio_transporte_id
        )
        self.relacion_dao.create(db, relacion)

        return nuevo_cargo

    def actualizar(self, db: Session, id_cargo: int, cargo_data: CargoCreate):
        return self.dao.update(db, id_cargo, cargo_data)

    def eliminar(self, db: Session, id_cargo: int):
        return self.dao.delete(db, id_cargo)
