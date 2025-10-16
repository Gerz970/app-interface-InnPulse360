from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from dao.empleado.dao_puesto import PuestoDAO
from schemas.empleado.puesto_schema import PuestoCreate, PuestoUpdate, PuestoResponse

class PuestoService:

    def __init__(self, db_session: Session):
        self.dao = PuestoDAO(db_session)

    def crear_puesto(self, puesto_data: PuestoCreate) -> PuestoResponse:
        try:
            nuevo_puesto = self.dao.create(puesto_data)
            return PuestoResponse.model_validate(nuevo_puesto)
        except SQLAlchemyError as e:
            raise Exception(f"Error al crear puesto en la base de datos: {str(e)}")
        except Exception as e:
            raise Exception(f"Error inesperado al crear puesto: {str(e)}")

    def obtener_puesto_por_id(self, puesto_id: int) -> Optional[PuestoResponse]:
        try:
            puesto = self.dao.get_by_id(puesto_id)
            if not puesto:
                return None
            return PuestoResponse.model_validate(puesto)
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener puesto de la base de datos: {str(e)}")
        except Exception as e:
            raise Exception(f"Error inesperado al obtener puesto: {str(e)}")

    def obtener_todos_los_puestos(self, skip: int = 0, limit: int = 100) -> List[PuestoResponse]:
        try:
            puestos = self.dao.get_all(skip=skip, limit=limit)
            return [PuestoResponse.model_validate(p) for p in puestos]
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener puestos de la base de datos: {str(e)}")
        except Exception as e:
            raise Exception(f"Error inesperado al obtener puestos: {str(e)}")

    def actualizar_puesto(self, puesto_id: int, puesto_update: PuestoUpdate) -> Optional[PuestoResponse]:
        try:
            update_data = puesto_update.model_dump(exclude_unset=True)
            if not update_data:
                raise ValueError("Debe proporcionar al menos un campo para actualizar")
            
            puesto_actualizado = self.dao.update(puesto_id, puesto_update)
            if not puesto_actualizado:
                return None
            
            return PuestoResponse.model_validate(puesto_actualizado)
        except ValueError as e:
            raise e
        except SQLAlchemyError as e:
            raise Exception(f"Error al actualizar puesto en la base de datos: {str(e)}")
        except Exception as e:
            raise Exception(f"Error inesperado al actualizar puesto: {str(e)}")

    def eliminar_puesto(self, puesto_id: int) -> bool:
        try:
            return self.dao.delete_logical(puesto_id)
        except SQLAlchemyError as e:
            raise Exception(f"Error al eliminar puesto en la base de datos: {str(e)}")
        except Exception as e:
            raise Exception(f"Error inesperado al eliminar puesto: {str(e)}")
