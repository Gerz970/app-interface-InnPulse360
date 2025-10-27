from sqlalchemy.orm import Session
from dao.mantenimiento.dao_incidencia_mantenimiento import IncidenciaMantenimientoDao
from models.mantenimiento.incidencia_model import Incidencia
from models.mantenimiento.mantenimiento_model import Mantenimiento
from fastapi import HTTPException

class IncidenciaMantenimientoService:
    def __init__(self):
        self.dao = IncidenciaMantenimientoDao()

    def asociar_incidencia_mantenimiento(self, db: Session, incidencia_id: int, mantenimiento_id: int):
        # Validar que ambos existan antes de crear la relación
        incidencia = db.query(Incidencia).filter(Incidencia.id_incidencia == incidencia_id).first()
        mantenimiento = db.query(Mantenimiento).filter(Mantenimiento.id_mantenimiento == mantenimiento_id).first()

        if not incidencia:
            raise HTTPException(status_code=404, detail="Incidencia no encontrada")
        if not mantenimiento:
            raise HTTPException(status_code=404, detail="Mantenimiento no encontrado")

        # Crear la relación
        return self.dao.crear_relacion(db, incidencia_id, mantenimiento_id)
