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
