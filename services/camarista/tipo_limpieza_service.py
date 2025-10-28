from dao.camarista.dao_tipos_limpieza import TiposLimpiezaDao
from models.camarista.tipos_limpieza import TiposLimpieza
from schemas.camarista.tipos_limpieza_schema import TipoLimpiezaCreate, TipoLimpiezaUpdate
from sqlalchemy.orm import Session

class TipoLimpiezaService:
    def __init__(self):
        self.dao = TiposLimpiezaDao()

    def obtener_todos(self, db: Session):
        return self.dao.get_all(db)

    def obtener_por_id(self, db: Session, id_tipo_limpieza: int):
        return self.dao.get_by_id(db, id_tipo_limpieza)

    def crear(self, db: Session, data: TipoLimpiezaCreate):
        nuevo_tipo_limpieza = TiposLimpieza(**data.dict())
        return self.dao.create(db, nuevo_tipo_limpieza)

    def actualizar(self, db: Session, id_tipo_limpieza: int, data: TipoLimpiezaUpdate):
        return self.dao.update(db, id_tipo_limpieza, data.dict(exclude_unset=True))

    def eliminar(self, db: Session, id_tipo_limpieza: int):
        return self.dao.delete(db, id_tipo_limpieza)
    