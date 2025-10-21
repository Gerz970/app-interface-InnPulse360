from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from dao.catalogos.dao_periodicidad import PeriodicidadDAO
from models.catalogos.periodicidad_model import Periodicidad
from schemas.catalogos.periodicidad_schemas import PeriodicidadCreate, PeriodicidadUpdate

class PeriodicidadService:
    def __init__(self, db: Session):
        self.dao = PeriodicidadDAO(db)

    def listar(self, skip: int = 0, limit: int = 100):
        return self.dao.get_all(skip, limit)

    def obtener(self, id_periodicidad: int):
        periodicidad = self.dao.get_by_id(id_periodicidad)
        if not periodicidad or not periodicidad.id_estatus:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Periodicidad no encontrada o inactiva"
            )
        return periodicidad

    def crear(self, data: PeriodicidadCreate):
        # Crear usando **data
        nueva = Periodicidad(**data.model_dump())
        return self.dao.create(nueva)

    def actualizar(self, id_periodicidad: int, data: PeriodicidadUpdate):
        db_periodicidad = self.dao.get_by_id(id_periodicidad)
        if not db_periodicidad:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Periodicidad no encontrada"
            )
        # Actualizar usando **data
        return self.dao.update(db_periodicidad, data.model_dump(exclude_unset=True))

    def eliminar(self, id_periodicidad: int):
        db_periodicidad = self.dao.get_by_id(id_periodicidad)
        if not db_periodicidad:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Periodicidad no encontrada"
            )
        return self.dao.delete_logico(db_periodicidad)
