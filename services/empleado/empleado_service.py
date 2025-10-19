from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from dao.empleado.dao_empleado import EmpleadoDAO
from dao.empleado.dao_direccion import DireccionDAO
from schemas.empleado import EmpleadoCreate, EmpleadoUpdate, EmpleadoResponse
from models.empleados.empleado_model import Empleado
from models.empleados.domicilio_empleado_model import DomicilioEmpleado
from schemas.empleado.domicilio_base import DomicilioUpdate, DomicilioBase


class EmpleadoService:
    
    def __init__(self, db_session: Session):
        self.db = db_session
        self.dao = EmpleadoDAO(db_session)
    
    def crear_empleado(self, empleado_data: EmpleadoCreate) -> EmpleadoResponse:
        try:
            empleado_creado = self.dao.create(empleado_data)
            return EmpleadoResponse.model_validate(empleado_creado)
        except SQLAlchemyError as e:
            raise Exception(f"Error al crear empleado en la base de datos: {str(e)}")
        except Exception as e:
            raise Exception(f"Error inesperado al crear empleado: {str(e)}")
    
    def obtener_empleado_por_id(self, empleado_id: int) -> Optional[EmpleadoResponse]:
        try:
            return(self.dao.get_by_id(empleado_id))
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener empleado de la base de datos: {str(e)}")
        except Exception as e:
            raise Exception(f"Error inesperado al obtener empleado: {str(e)}")
    
    def obtener_todos_los_empleados_por_hotel(self, hotel_id: int, skip: int = 0, limit: int = 100) -> List[EmpleadoResponse]:
        try:
            empleados = self.dao.get_all(hotel_id)

            return empleados
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener empleados de la base de datos: {str(e)}")
        except Exception as e:
            raise Exception(f"Error inesperado al obtener empleados: {str(e)}")
    
    def actualizar_empleado(self, empleado_id: int, empleado_update: EmpleadoUpdate) -> Optional[EmpleadoResponse]:
        try:
            update_data = empleado_update.model_dump(exclude_unset=True)
            if not update_data:
                raise ValueError("Debe proporcionar al menos un campo para actualizar")
            
            empleado_actualizado = self.dao.update(empleado_id, empleado_update)
            if not empleado_actualizado:
                return None

            return EmpleadoResponse.model_validate(empleado_actualizado)
        except ValueError as e:
            raise e
        except SQLAlchemyError as e:
            raise Exception(f"Error al actualizar empleado en la base de datos: {str(e)}")
        except Exception as e:
            raise Exception(f"Error inesperado al actualizar empleado: {str(e)}")

    def eliminar_empleado(self, empleado_id: int) -> bool:
        """
        Elimina físicamente un empleado.
        """
        try:
            eliminado = self.dao.delete(empleado_id)
            return eliminado
        except SQLAlchemyError as e:
            raise Exception(f"Error al eliminar empleado de la base de datos: {str(e)}")
        except Exception as e:
            raise Exception(f"Error inesperado al eliminar empleado: {str(e)}")

    def actualizar_direccion(self, direccion_id: int, direccion_update: DomicilioUpdate) -> Optional[DomicilioBase]:
        try:
            update_data = direccion_update.model_dump(exclude_unset=True)
            if not update_data:
                raise ValueError("Debe proporcionar al menos un campo para actualizar")
            # Crear instancia del DAO con la sesión actual
            direccion_dao = DireccionDAO(self.db)

        # Llamar al método de instancia
            direccion_actualizado = direccion_dao.update(direccion_id, direccion_update)

            if not direccion_actualizado:
                return None

            return DomicilioBase.model_validate(direccion_actualizado)
        except ValueError as e:
            raise e
        except SQLAlchemyError as e:
            raise Exception(f"Error al actualizar direccion en la base de datos: {str(e)}")
        except Exception as e:
            raise Exception(f"Error inesperado al actualizar direccion: {str(e)}")

   