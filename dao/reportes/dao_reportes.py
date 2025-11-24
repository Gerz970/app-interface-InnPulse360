from sqlalchemy.orm import Session
from models.reserva.cargos_model import Cargo
from models.reserva.tipo_cargos_model import TipoCargo
from sqlalchemy import func, Date, cast
from datetime import date
from models.camarista.limpieza_model import Limpieza
from models.camarista.tipos_limpieza import TiposLimpieza
from models.empleados.empleado_model import Empleado

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
    
    def obtener_limpiezas_por_empleado(self, db: Session, fecha_inicio: date, fecha_fin: date):
        resultados = (
            db.query(
                Limpieza.empleado_id,
                func.concat(
                    Empleado.nombre, " ", 
                    Empleado.apellido_paterno, " ", 
                    Empleado.apellido_materno
                ).label("nombre_empleado"),
                func.count().label("total")
            )
            .join(Empleado, Empleado.id_empleado == Limpieza.empleado_id)
            .filter(Limpieza.estatus_limpieza_id == 3)
            .filter(cast(Limpieza.fecha_termino, Date) >= fecha_inicio)
            .filter(cast(Limpieza.fecha_termino, Date) <= fecha_fin)
            .group_by(
                Limpieza.empleado_id,
                Empleado.nombre,
                Empleado.apellido_paterno,
                Empleado.apellido_materno
            )
            .order_by(func.count().desc())   
            .all()
        )

        return [
            {
                "empleado_id": empleado_id,
                "nombre_empleado": nombre_empleado,
                "total": total
            }
            for empleado_id, nombre_empleado, total in resultados
        ]
    
    def obtener_limpiezas_por_tipo_por_estatus(self, db: Session, fecha_inicio: date, fecha_fin: date, estatus: int):
        resultados = (
        db.query(
            Limpieza.tipo_limpieza_id,
            TiposLimpieza.nombre_tipo,
            func.count().label("total")
        )
        .join(TiposLimpieza, TiposLimpieza.id_tipo_limpieza == Limpieza.tipo_limpieza_id)
        .filter(Limpieza.estatus_limpieza_id == estatus)
        .filter(cast(Limpieza.fecha_termino, Date) >= fecha_inicio)
        .filter(cast(Limpieza.fecha_termino, Date) <= fecha_fin)
        .group_by(
            Limpieza.tipo_limpieza_id,
            TiposLimpieza.nombre_tipo
        )
        .order_by(func.count().desc())  
        .all()
        )

        return [
            {
                "tipo_limpieza_id": tipo_limpieza_id,
                "nombre_tipo": nombre_tipo,
                "total": total
            }
            for tipo_limpieza_id, nombre_tipo, total in resultados
        ]
