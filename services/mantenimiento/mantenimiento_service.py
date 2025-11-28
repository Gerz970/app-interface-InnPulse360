from sqlalchemy.orm import Session
from dao.mantenimiento.dao_mantenimiento import MantenimientoDao
from models.mantenimiento.mantenimiento_model import Mantenimiento
from schemas.mantenimiento.mantenimiento_schema import MantenimientoCreate, MantenimientoUpdate
from datetime import datetime
from models.seguridad.usuario_asignacion_model import UsuarioAsignacion
import logging
import threading

logger = logging.getLogger(__name__)

class MantenimientoService:
    def __init__(self):
        self.dao = MantenimientoDao()

    def obtener_todos(self, db: Session):
        return self.dao.get_all(db)

    def obtener_por_id(self, db: Session, id_mantenimiento: int):
        return self.dao.get_by_id(db, id_mantenimiento)

    def crear(self, db: Session, data: MantenimientoCreate):
        mantenimiento = Mantenimiento(**data.model_dump())
        mantenimientoCreado = self.dao.create(db, mantenimiento)
        
        def enviar_en_background():
            # Crear nueva sesión de BD para el hilo (importante: no reutilizar la sesión del hilo principal)
            from core.database_connection import get_database_session
            db_background = next(get_database_session())
            try:
                from services.notifications.fcm_push_service import FCMPushService
                    
             # Crear servicio de notificaciones con nueva sesión
                push_service = FCMPushService(db_background)
                    
                # Buscar usuario_id desde empleado_id en UsuarioAsignacion
                usuario_asignacion = db_background.query(UsuarioAsignacion).filter(
                        UsuarioAsignacion.empleado_id == mantenimiento.empleado_id,
                        UsuarioAsignacion.tipo_asignacion == 1,  # 1=Empleado
                        UsuarioAsignacion.estatus == 1  # Activo
                ).first()
                   
                if not usuario_asignacion:
                        logger.info(f"No se encontró usuario asignado para empleado_id {empleado_id}")
                        return
                    
                usuario_id = usuario_asignacion.usuario_id
                # Enviar notificación (sin esperar respuesta)
                push_service.send_to_user(
                    usuario_id=usuario_id,
                    title="Nueva tarea de mantenimiento asignada",
                    body=f"Se te ha asignado: {mantenimiento.descripcion}",
                )         
            finally:
                # Cerrar sesión de BD del hilo
                db_background.close() 
            thread = threading.Thread(target=enviar_en_background, daemon=True)
            thread.start()  
        return mantenimientoCreado        

    def actualizar(self, db: Session, id_mantenimiento: int, data: MantenimientoUpdate):
        return self.dao.update(db, id_mantenimiento, data.model_dump(exclude_unset=True))

    def eliminar(self, db: Session, id_mantenimiento: int):
        return self.dao.delete(db, id_mantenimiento)
    
    def obtener_por_empleado(self, db: Session, empleado_id: int):
        return db.query(Mantenimiento).filter(Mantenimiento.empleado_id == empleado_id).all()

    def obtener_por_fecha(self, db: Session, fecha_inicio: datetime):
        return db.query(Mantenimiento).filter(Mantenimiento.fecha >= fecha_inicio).all()

    def obtener_por_empleado_fecha(self, db: Session, empleado_id: int, fecha:datetime):
        return( 
            db.query(Mantenimiento).filter(
            Mantenimiento.empleado_id == empleado_id,
            Mantenimiento.fecha >= fecha
            ).all()
        )
    
    def obtener_por_empleado_por_estatus(self, db: Session, empleado_id: int, estatus: int):
        return db.query(Mantenimiento).filter(Mantenimiento.empleado_id == empleado_id, Mantenimiento.estatus == estatus).all()
