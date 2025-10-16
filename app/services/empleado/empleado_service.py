from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from dao.empleado.dao_empleado import EmpleadoDAO
from schemas.empleado import EmpleadoCreate, EmpleadoUpdate, EmpleadoResponse
from models.empleados.empleado_model import Empleado
from models.empleados.domicilio_empleado_model import DomicilioEmpleado
from schemas.empleado.domicilio_base import DomicilioBase


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
            empleado = (
                self.db.query(Empleado)
                .options(
                    joinedload(Empleado.domicilio_relacion)
                    .joinedload(DomicilioEmpleado.domicilio)
                )
                .filter(Empleado.id_empleado == empleado_id)
                .first()
            )

            if not empleado:
                return None

            domicilio = None
            if empleado.domicilio_relacion and empleado.domicilio_relacion.domicilio:
                domicilio_obj = empleado.domicilio_relacion.domicilio
                domicilio_dict = {
                    "id_domicilio": domicilio_obj.id_domicilio,
                    "domicilio_completo": domicilio_obj.domicilio_completo,
                    "codigo_postal": domicilio_obj.codigo_postal,
                    "estatus_id": domicilio_obj.estatus_id
                }
                domicilio = DomicilioBase.model_validate(domicilio_dict)

            return EmpleadoResponse(
                id_empleado=empleado.id_empleado,
                clave_empleado=empleado.clave_empleado,
                nombre=empleado.nombre,
                apellido_paterno=empleado.apellido_paterno,
                apellido_materno=empleado.apellido_materno,
                fecha_nacimiento=empleado.fecha_nacimiento,
                rfc=empleado.rfc,
                curp=empleado.curp,
                domicilio=domicilio
            )
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener empleado de la base de datos: {str(e)}")
        except Exception as e:
            raise Exception(f"Error inesperado al obtener empleado: {str(e)}")
    
    def obtener_todos_los_empleados(self, skip: int = 0, limit: int = 100) -> List[EmpleadoResponse]:
        try:
            empleados = (
                self.db.query(Empleado)
                .options(
                    joinedload(Empleado.domicilio_relacion)
                    .joinedload(DomicilioEmpleado.domicilio)
                )
                .order_by(Empleado.id_empleado)
                .offset(skip)
                .limit(limit)
                .all()
            )

            result = []
            for emp in empleados:
                domicilio = None
                if emp.domicilio_relacion and emp.domicilio_relacion.domicilio:
                    domicilio_obj = emp.domicilio_relacion.domicilio
                    domicilio_dict = {
                        "id_domicilio": domicilio_obj.id_domicilio,
                        "domicilio_completo": domicilio_obj.domicilio_completo,
                        "codigo_postal": domicilio_obj.codigo_postal,
                        "estatus_id": domicilio_obj.estatus_id
                    }
                    domicilio = DomicilioBase.model_validate(domicilio_dict)

                result.append(
                    EmpleadoResponse(
                        id_empleado=emp.id_empleado,
                        clave_empleado=emp.clave_empleado,
                        nombre=emp.nombre,
                        apellido_paterno=emp.apellido_paterno,
                        apellido_materno=emp.apellido_materno,
                        fecha_nacimiento=emp.fecha_nacimiento,
                        rfc=emp.rfc,
                        curp=emp.curp,
                        domicilio=domicilio
                    )
                )
            return result
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

   