from dao.reportes.dao_reportes import ReportesDAO
from sqlalchemy.orm import Session
from datetime import date

class ResportesService:
    def __init__(self, db: Session):
        self.db = db
        self.dao = ReportesDAO()

    def obtener_entradas_tipo_dia(self, dia: date):
        return self.dao.obtener_entradas_tipo_dia(self.db, dia)
    
    def obtener_limpiezas_por_empleado(self, fecha_inicio: date, fecha_fin: date):
        return self.dao.obtener_limpiezas_por_empleado(self.db, fecha_inicio, fecha_fin)

    def obtener_limpiezas_por_tipo_por_estatus(self, fecha_inicio: date, fecha_fin: date, estatus:int):
        return self.dao.obtener_limpiezas_por_tipo_por_estatus(self.db, fecha_inicio, fecha_fin, estatus)
