from dao.camarista.dao_estatus_limpieza import EstatusLimpiezaDao
from models.camarista.estatus_limpieza_model import EstatusLimpieza
from schemas.camarista.estatus_limpieza_schema import EstatusLimpiezaCreate, EstatusLimpiezaUpdate
from sqlalchemy.orm import Session

class EstatusLimpiezaService:
    def __init__(self):
        self.dao = EstatusLimpiezaDao()

    def obtener_todos(self, db: Session):
        return self.dao.get_all(db)

    def obtener_por_id(self, db: Session, id_estatus_limpieza: int):
        return self.dao.get_by_id(db, id_estatus_limpieza)

    def crear(self, db: Session, data: EstatusLimpiezaCreate):
        nuevo = EstatusLimpieza(**data.dict())
        return self.dao.create(db, nuevo)

    def actualizar(self, db: Session, id_estatus_limpieza: int, data: EstatusLimpiezaUpdate):
        return self.dao.update(db, id_estatus_limpieza, data.dict(exclude_unset=True))

    def eliminar(self, db: Session, id_estatus_limpieza: int):
        return self.dao.delete(db, id_estatus_limpieza)
