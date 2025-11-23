from sqlalchemy.orm import Session
from models.reserva.cargos_model import Cargo
from models.reserva.tipo_cargos_model import TipoCargo
from sqlalchemy import func, Date
from datetime import date

class ReportesDAO:

    def obtener_entradas_tipo_dia(self, db: Session, fecha: date):
        resultados = (
        db.query(
            TipoCargo.nombre_cargo,
            func.sum(Cargo.costo_unitario).label("total")
        )
            .join(TipoCargo, TipoCargo.id_tipo == Cargo.tipo_id)
            .filter(func.cast(Cargo.created_at, Date) == fecha)
            .group_by(TipoCargo.nombre_cargo, Cargo.tipo_id, func.cast(Cargo.created_at, Date))
            .all()
        )

        return [
            {
                "nombre_cargo": nombre,
                "total": total
            }
            for nombre, total in resultados
]
