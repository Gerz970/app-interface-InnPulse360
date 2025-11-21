from dao.camarista.dao_limpieza import LimpiezaDao
from models.camarista.limpieza_model import Limpieza
from schemas.camarista.limpieza_schema import LimpiezaCreate, LimpiezaUpdate
from sqlalchemy.orm import Session
from datetime import date, datetime, time

class LimpiezaService:
    def __init__(self):
        self.dao = LimpiezaDao()

    def obtener_todos(self, db: Session):
        return self.dao.get_all(db)

    def obtener_por_id(self, db: Session, id_limpieza: int):
        return self.dao.get_by_id(db, id_limpieza)

    def crear(self, db: Session, data: LimpiezaCreate):
        data_dict = data.dict()
        # Si empleado_id es None o 0, no incluirlo en el modelo
        if data_dict.get('empleado_id') is None or data_dict.get('empleado_id') == 0:
            data_dict.pop('empleado_id', None)
        nueva_limpieza = Limpieza(**data_dict)
        return self.dao.create(db, nueva_limpieza)

    def actualizar(self, db: Session, id_limpieza: int, data: LimpiezaUpdate):
        return self.dao.update(db, id_limpieza, data.dict(exclude_unset=True))

    def eliminar(self, db: Session, id_limpieza: int):
        return self.dao.delete(db, id_limpieza)

    def obtener_por_empleado(self, db: Session, empleado_id: int):
        return self.dao.get_by_empleado(db, empleado_id)

    def obtener_por_habitacion_area(self, db: Session, habitacion_area_id: int):
        return self.dao.get_by_habitacion_area(db, habitacion_area_id)

    def obtener_por_estatus(self, db: Session, estatus_limpieza_id: int):
        return self.dao.get_by_estatus(db, estatus_limpieza_id)

    def obtener_por_fecha(self, db: Session, fecha):
        inicio_dia = datetime.combine(fecha, time.min)
        fin_dia = datetime.combine(fecha, time.max)
    
        limpiezas = self.dao.get_by_rango_fecha(db, inicio_dia, fin_dia)
        return limpiezas

    def crear_masivo(self, db: Session, datos_limpiezas: list):
        """Crea múltiples limpiezas en una sola transacción"""
        limpiezas = []
        for data in datos_limpiezas:
            data_dict = data.dict()
            # Si empleado_id es None o 0, no incluirlo en el modelo
            if data_dict.get('empleado_id') is None or data_dict.get('empleado_id') == 0:
                data_dict.pop('empleado_id', None)
            limpiezas.append(Limpieza(**data_dict))
        return self.dao.crear_masivo(db, limpiezas)