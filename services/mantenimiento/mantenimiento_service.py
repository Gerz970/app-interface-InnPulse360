from sqlalchemy.orm import Session
from dao.mantenimiento.dao_mantenimiento import MantenimientoDao
from models.mantenimiento.mantenimiento_model import Mantenimiento
from schemas.mantenimiento.mantenimiento_schema import MantenimientoCreate, MantenimientoUpdate

class MantenimientoService:
    def __init__(self):
        self.dao = MantenimientoDao()

    def obtener_todos(self, db: Session):
        return self.dao.get_all(db)

    def obtener_por_id(self, db: Session, id_mantenimiento: int):
        return self.dao.get_by_id(db, id_mantenimiento)

    def crear(self, db: Session, data: MantenimientoCreate):
        mantenimiento = Mantenimiento(**data.model_dump())
        return self.dao.create(db, mantenimiento)

    def actualizar(self, db: Session, id_mantenimiento: int, data: MantenimientoUpdate):
        return self.dao.update(db, id_mantenimiento, data.model_dump(exclude_unset=True))

    def eliminar(self, db: Session, id_mantenimiento: int):
        return self.dao.delete(db, id_mantenimiento)
