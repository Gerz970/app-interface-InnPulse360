from dao.camarista.dao_limpieza import LimpiezaDao
from models.camarista.limpieza_model import Limpieza
from schemas.camarista.limpieza_schema import LimpiezaCreate, LimpiezaUpdate
from sqlalchemy.orm import Session

class LimpiezaService:
    def __init__(self):
        self.dao = LimpiezaDao()

    def obtener_todos(self, db: Session):
        return self.dao.get_all(db)

    def obtener_por_id(self, db: Session, id_limpieza: int):
        return self.dao.get_by_id(db, id_limpieza)

    def crear(self, db: Session, data: LimpiezaCreate):
        nueva_limpieza = Limpieza(**data.dict())
        return self.dao.create(db, nueva_limpieza)

    def actualizar(self, db: Session, id_limpieza: int, data: LimpiezaUpdate):
        return self.dao.update(db, id_limpieza, data.dict(exclude_unset=True))

    def eliminar(self, db: Session, id_limpieza: int):
        return self.dao.delete(db, id_limpieza)
