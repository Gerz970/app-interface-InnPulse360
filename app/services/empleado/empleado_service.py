from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from dao.empleado.dao_empleado import EmpleadoDAO
from schemas.empleado import EmpleadoCreate, EmpleadoUpdate, EmpleadoResponse

class EmpleadoService:
    
    def __init__(self, db_session: Session):
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
            empleado = self.dao.get_by_id(empleado_id)
            if not empleado:
                return None
            return EmpleadoResponse.model_validate(empleado)
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener empleado de la base de datos: {str(e)}")
        except Exception as e:
            raise Exception(f"Error inesperado al obtener empleado: {str(e)}")
    
    def obtener_todos_los_empleados(self, skip: int = 0, limit: int = 100) -> List[EmpleadoResponse]:
        try:
            empleados = self.dao.get_all(skip=skip, limit=limit)
            return [EmpleadoResponse.model_validate(emp) for emp in empleados]
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
