from sqlalchemy.orm import Session
from dao.mantenimiento.dao_mantenimiento import MantenimientoDao
from models.mantenimiento.mantenimiento_model import Mantenimiento
from schemas.mantenimiento.mantenimiento_schema import MantenimientoCreate, MantenimientoUpdate
from datetime import datetime
from models.seguridad.usuario_asignacion_model import UsuarioAsignacion
import logging
import threading
from sqlalchemy.orm import joinedload

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
                        logger.info(f"No se encontró usuario asignado para empleado_id {mantenimiento.empleado_id}")
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

    def actualizar(self, db: Session, mantenimiento_id: int, data: MantenimientoUpdate):
        """
        Actualiza un mantenimiento.
        Si se asigna un empleado, envía notificación push al empleado.
        """
        # Obtener mantenimiento actual para comparar empleado_id
        mantenimiento_actual = (
            db.query(Mantenimiento)
            .options(joinedload(Mantenimiento.incidencias))   
            .filter(Mantenimiento.id_mantenimiento == mantenimiento_id)
            .first()
        )

        if not mantenimiento_actual:
            return None

        empleado_id_anterior = mantenimiento_actual.empleado_id
        
        # Preparar datos de actualización
        data_dict = data.model_dump(exclude_unset=True)
        
        if data_dict.get('estatus') == 2:
            for incidencia in mantenimiento_actual.incidencias:
                incidencia.id_estatus = 3  # Cambiar el estatus de la incidencia

        db.commit()
        db.refresh(mantenimiento_actual)

        # Actualizar mantenimiento
        mantenimiento_actualizado = self.dao.update(db, mantenimiento_id, data_dict)
        
        if mantenimiento_actualizado:
            empleado_id_nuevo = mantenimiento_actualizado.empleado_id
            
            # Enviar notificación solo si se asignó un empleado
            # (antes era None y ahora tiene valor, o cambió de valor)
            if empleado_id_nuevo and empleado_id_nuevo != empleado_id_anterior:
                self._enviar_notificacion_asignacion(db, mantenimiento_actualizado)
        
        return mantenimiento_actualizado
    
    def _enviar_notificacion_asignacion(self, db: Session, mantenimiento):
        """
        Envía notificación push al empleado cuando se le asigna un mantenimiento.
        Se ejecuta en un hilo separado para no bloquear la respuesta principal.
        
        Args:
            db (Session): Sesión de base de datos
            mantenimiento: Mantenimiento actualizado con empleado asignado
        """
        # Guardar datos necesarios antes de pasar al hilo
        mantenimiento_id = mantenimiento.id_mantenimiento
        empleado_id = mantenimiento.empleado_id
        descripcion = mantenimiento.descripcion
        
        # Ejecutar en hilo separado para no bloquear la respuesta
        def enviar_en_background():
            try:
                # Crear nueva sesión de BD para el hilo (importante: no reutilizar la sesión del hilo principal)
                from core.database_connection import get_database_session
                from models.seguridad.usuario_asignacion_model import UsuarioAsignacion
                
                db_background = next(get_database_session())
                
                try:
                    # Solo enviar si hay empleado asignado
                    if not empleado_id:
                        return
                    
                    # Buscar usuario_id desde empleado_id en UsuarioAsignacion
                    usuario_asignacion = db_background.query(UsuarioAsignacion).filter(
                        UsuarioAsignacion.empleado_id == empleado_id,
                        UsuarioAsignacion.tipo_asignacion == 1,  # 1=Empleado
                        UsuarioAsignacion.estatus == 1  # Activo
                    ).first()
                    
                    if not usuario_asignacion:
                        logger.info(f"No se encontró usuario asignado para empleado_id {empleado_id}")
                        return
                    
                    usuario_id = usuario_asignacion.usuario_id
                    
                    # Importar aquí para evitar importación circular
                    from services.notifications.fcm_push_service import FCMPushService
                    
                    # Crear servicio de notificaciones con nueva sesión
                    push_service = FCMPushService(db_background)
                    
                    # Enviar notificación
                    push_service.send_to_user(
                        usuario_id=usuario_id,
                        title="Nueva tarea de mantenimiento asignada",
                        body=f"Se te ha asignado: {descripcion}",
                        data={
                            "tipo": "mantenimiento_asignado",
                            "mantenimiento_id": str(mantenimiento_id),
                            "empleado_id": str(empleado_id),
                            "screen": "mantenimiento_detail"
                        }
                    )
                    
                    logger.info(f"✅ Notificación enviada al usuario {usuario_id} (empleado_id: {empleado_id}) por mantenimiento {mantenimiento_id}")
                    
                finally:
                    # Cerrar sesión de BD del hilo
                    db_background.close()
                    
            except Exception as e:
                # No fallar la operación principal si falla la notificación
                logger.error(f"❌ Error enviando notificación de mantenimiento: {e}", exc_info=True)
        
        # Iniciar hilo en background sin esperar (daemon=True permite que el programa termine sin esperar el hilo)
        thread = threading.Thread(target=enviar_en_background, daemon=True)
        thread.start()


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
