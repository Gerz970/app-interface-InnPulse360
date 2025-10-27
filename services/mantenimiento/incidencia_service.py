from dao.mantenimiento.dao_incidencia import IncidenciaDao
from models.mantenimiento.incidencia_model import Incidencia
from schemas.mantenimiento.incidencia_schema import IncidenciaCreate, IncidenciaUpdate
from sqlalchemy.orm import Session

class IncidenciaService:
    def __init__(self):
        self.dao = IncidenciaDao()

    def obtener_todos(self, db: Session):
        return self.dao.obtener_todos(db)

    def obtener_por_id(self, db: Session, id_incidencia: int):
        return self.dao.obtener_por_id(db, id_incidencia)

    def crear(self, db: Session, data: IncidenciaCreate):
        nueva_incidencia = Incidencia(**data.dict())
        return self.dao.crear(db, nueva_incidencia)

    def actualizar(self, db: Session, id_incidencia: int, data: IncidenciaUpdate):
        return self.dao.actualizar(db, id_incidencia, data.dict(exclude_unset=True))

    def eliminar(self, db: Session, id_incidencia: int):
        return self.dao.eliminar(db, id_incidencia)
