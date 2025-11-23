from dao.reportes.dao_reportes import ReportesDAO
from sqlalchemy.orm import Session
from datetime import date

class ResportesService:
    def __init__(self, db: Session):
        self.db = db
        self.dao = ReportesDAO()

    def obtener_entradas_tipo_dia(self, dia: date):
        return self.dao.obtener_entradas_tipo_dia(self.db, dia)
