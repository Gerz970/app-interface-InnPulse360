from dao.hotel.dao_habitacion_area import HabitacionAreaDAO
from models.hotel.habitacionArea_model import HabitacionArea
from schemas.hotel.habitacion_area_schema import HabitacionAreaCreate, HabitacionAreaUpdate, HabitacionAreaResponse
from typing import List

class HabitacionAreaService:
    def __init__(self, dao: HabitacionAreaDAO):
        self.dao = dao

    def listar(self, piso_id:int):
        return self.dao.get_all(piso_id)

    def obtener_por_id(self, id_habitacion_area: int):
        return self.dao.get_by_id(id_habitacion_area)

    def crear(self, data: HabitacionAreaCreate):
        # Crear usando **data
        nuevo = HabitacionArea(**data.model_dump())
        return self.dao.create(nuevo)

    def actualizar(self, id_habitacion_area: int, data: HabitacionAreaUpdate):
        # Actualizar usando **data
        return self.dao.update(id_habitacion_area, data.model_dump(exclude_unset=True))

    def eliminar(self, id_habitacion_area: int):
        return self.dao.delete(id_habitacion_area)

    def obtener_habitaciones_disponibles_por_piso(self, piso_id: int) -> List[HabitacionAreaResponse]:
        """Obtiene habitaciones disponibles para un piso (sin reservas activas)"""
        habitaciones = self.dao.get_habitaciones_disponibles_por_piso(piso_id)
        return [HabitacionAreaResponse.model_validate(hab) for hab in habitaciones]
