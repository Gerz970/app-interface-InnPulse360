from sqlalchemy.orm import Session
from models.mantenimiento.incidencia_mantenimiento_model import IncidenciaMantenimiento

class IncidenciaMantenimientoDao:
    def crear_relacion(self, db: Session, incidencia_id: int, mantenimiento_id: int):
        relacion = IncidenciaMantenimiento(
            incidencia_id=incidencia_id,
            mantenimiento_id=mantenimiento_id
        )
        db.add(relacion)
        db.commit()
        db.refresh(relacion)
        return relacion
