from sqlalchemy.orm import Session
from models.hotel.habitacionArea_model import HabitacionArea

class HabitacionAreaDAO:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, piso_id:int):
        return (self.db.query(HabitacionArea)
                .filter(HabitacionArea.piso_id == piso_id)
                .order_by(HabitacionArea.piso_id)
                .all())

    def get_by_id(self, id_habitacion_area: int):
        return self.db.query(HabitacionArea).filter(HabitacionArea.id_habitacion_area == id_habitacion_area).first()

    def create(self, habitacion_area: HabitacionArea):
        self.db.add(habitacion_area)
        self.db.commit()
        self.db.refresh(habitacion_area)
        return habitacion_area

    def update(self, id_habitacion_area: int, data: dict):
        habitacion = self.get_by_id(id_habitacion_area)
        if habitacion:
            for key, value in data.items():
                setattr(habitacion, key, value)
            self.db.commit()
            self.db.refresh(habitacion)
        return habitacion

    def delete(self, id_habitacion_area: int):
        habitacion = self.get_by_id(id_habitacion_area)
        if habitacion:
            habitacion.estatus_id = 0
            self.db.commit()
            self.db.refresh(habitacion)
        return habitacion

    def get_habitaciones_disponibles_por_piso(self, piso_id: int):
        """
        Obtiene habitaciones disponibles para un piso (sin reservas activas).
        Una reserva activa tiene estatus = 1.
        """
        from models.reserva.reservaciones_model import Reservacion
        
        # Obtener IDs de habitaciones con reservas activas (estatus = 1 Y 2)
        habitaciones_ocupadas_ids = [
            r[0] for r in self.db.query(Reservacion.habitacion_area_id)
            .filter(Reservacion.id_estatus.in_([1, 2])).all()
        ]
        
        # Habitaciones del piso que NO están en habitaciones_ocupadas y están activas
        habitaciones = self.db.query(HabitacionArea).filter(
            HabitacionArea.piso_id == piso_id,
            HabitacionArea.estatus_id == 1,  # Solo habitaciones activas
            ~HabitacionArea.id_habitacion_area.in_(habitaciones_ocupadas_ids) if habitaciones_ocupadas_ids else True
        ).all()
        
        return habitaciones

    def get_habitaciones_con_estado_por_piso(self, piso_id: int):
        """
        Obtiene habitaciones de un piso con información de estado:
        - Reservaciones activas y en curso
        - Limpiezas pendientes (estatus = 1)
        - Limpiezas en proceso (estatus = 2)
        """
        from models.reserva.reservaciones_model import Reservacion
        from models.camarista.limpieza_model import Limpieza
        
        # Obtener todas las habitaciones del piso activas
        habitaciones = self.db.query(HabitacionArea).filter(
            HabitacionArea.piso_id == piso_id,
            HabitacionArea.estatus_id == 1
        ).all()
        
        # Obtener IDs de habitaciones con reservas activas
        habitaciones_con_reservacion_ids = set([
            r[0] for r in self.db.query(Reservacion.habitacion_area_id)
            .filter(Reservacion.id_estatus.in_([1, 2])).all()
        ])
        
        # Obtener IDs de habitaciones con limpiezas pendientes (estatus = 1)
        habitaciones_con_limpieza_pendiente_ids = set([
            l[0] for l in self.db.query(Limpieza.habitacion_area_id)
            .filter(Limpieza.estatus_limpieza_id == 1).all()
        ])
        
        # Obtener IDs de habitaciones con limpiezas en proceso (estatus = 2)
        habitaciones_con_limpieza_en_proceso_ids = set([
            l[0] for l in self.db.query(Limpieza.habitacion_area_id)
            .filter(Limpieza.estatus_limpieza_id == 2).all()
        ])
        
        # Construir resultado con información de estado
        resultado = []
        for hab in habitaciones:
            hab_id = hab.id_habitacion_area
            tiene_reservacion_activa = hab_id in habitaciones_con_reservacion_ids
            tiene_limpieza_pendiente = hab_id in habitaciones_con_limpieza_pendiente_ids
            tiene_limpieza_en_proceso = hab_id in habitaciones_con_limpieza_en_proceso_ids
            puede_seleccionarse = not tiene_limpieza_pendiente and not tiene_limpieza_en_proceso
            
            resultado.append({
                'habitacion': hab,
                'tiene_reservacion_activa': tiene_reservacion_activa,
                'tiene_limpieza_pendiente': tiene_limpieza_pendiente,
                'tiene_limpieza_en_proceso': tiene_limpieza_en_proceso,
                'puede_seleccionarse': puede_seleccionarse
            })
        
        return resultado