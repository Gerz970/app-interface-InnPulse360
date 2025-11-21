from dao.camarista.dao_limpieza import LimpiezaDao
from models.camarista.limpieza_model import Limpieza
from models.seguridad.usuario_asignacion_model import UsuarioAsignacion
from schemas.camarista.limpieza_schema import LimpiezaCreate, LimpiezaUpdate
from sqlalchemy.orm import Session
from datetime import date, datetime, time
import logging
import threading

logger = logging.getLogger(__name__)

class LimpiezaService:
    def __init__(self):
        self.dao = LimpiezaDao()

    def obtener_todos(self, db: Session):
        return self.dao.get_all(db)

    def obtener_por_id(self, db: Session, id_limpieza: int):
        return self.dao.get_by_id(db, id_limpieza)

    def _enviar_notificacion_asignacion(self, db: Session, limpieza: Limpieza):
        """
        Envía notificación push cuando se asigna una limpieza a un empleado
        Se ejecuta en un hilo separado para no bloquear la respuesta principal
        
        Args:
            db (Session): Sesión de base de datos
            limpieza (Limpieza): Limpieza asignada
        """
        # Guardar datos necesarios antes de pasar al hilo
        limpieza_id = limpieza.id_limpieza
        empleado_id = limpieza.empleado_id
        habitacion_area_id = limpieza.habitacion_area_id
        
        # Ejecutar en hilo separado para no bloquear la respuesta
        def enviar_en_background():
            try:
                # Crear nueva sesión de BD para el hilo (importante: no reutilizar la sesión del hilo principal)
                from core.database_connection import get_database_session
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
                    
                    # Recargar limpieza con relaciones desde BD
                    from sqlalchemy.orm import joinedload
                    limpieza_completa = db_background.query(Limpieza).options(
                        joinedload(Limpieza.habitacion_area)
                    ).filter(Limpieza.id_limpieza == limpieza_id).first()
                    
                    if not limpieza_completa:
                        logger.warning(f"No se encontró limpieza {limpieza_id} para notificación")
                        return
                    
                    # Importar aquí para evitar importación circular
                    from services.notifications.fcm_push_service import FCMPushService
                    
                    # Crear servicio de notificaciones con nueva sesión
                    push_service = FCMPushService(db_background)
                    
                    # Obtener información de la habitación/área
                    habitacion_nombre = "habitación/área"
                    if limpieza_completa.habitacion_area:
                        # Usar descripcion como principal, nombre_clave como respaldo
                        habitacion_nombre = (
                            limpieza_completa.habitacion_area.descripcion or 
                            limpieza_completa.habitacion_area.nombre_clave or 
                            f"Habitación {limpieza_completa.habitacion_area.id_habitacion_area}"
                        )
                    
                    # Enviar notificación (sin esperar respuesta)
                    push_service.send_to_user(
                        usuario_id=usuario_id,
                        title="Nueva limpieza asignada",
                        body=f"Se te ha asignado la limpieza de {habitacion_nombre}",
                        data={
                            "tipo": "limpieza_asignada",
                            "limpieza_id": str(limpieza_id),
                            "habitacion_area_id": str(habitacion_area_id),
                            "empleado_id": str(empleado_id),
                            "screen": "limpieza_detail"
                        }
                    )
                    
                    logger.info(f"Notificación enviada al usuario {usuario_id} por limpieza {limpieza_id}")
                    
                finally:
                    # Cerrar sesión de BD del hilo
                    db_background.close()
                    
            except Exception as e:
                # No fallar la operación principal si falla la notificación
                logger.error(f"Error enviando notificación de limpieza: {e}", exc_info=True)
        
        # Iniciar hilo en background sin esperar (daemon=True permite que el programa termine sin esperar el hilo)
        thread = threading.Thread(target=enviar_en_background, daemon=True)
        thread.start()

    def crear(self, db: Session, data: LimpiezaCreate):
        data_dict = data.dict()
        empleado_id_anterior = None
        empleado_id_nuevo = data_dict.get('empleado_id')
        
        # Si empleado_id es None o 0, no incluirlo en el modelo
        if empleado_id_nuevo is None or empleado_id_nuevo == 0:
            data_dict.pop('empleado_id', None)
            empleado_id_nuevo = None
        
        nueva_limpieza = Limpieza(**data_dict)
        limpieza_creada = self.dao.create(db, nueva_limpieza)
        
        # Enviar notificación si se asignó un empleado
        if empleado_id_nuevo:
            # Recargar con relaciones para obtener habitacion_area
            limpieza_completa = self.dao.get_by_id(db, limpieza_creada.id_limpieza)
            if limpieza_completa:
                self._enviar_notificacion_asignacion(db, limpieza_completa)
        
        return limpieza_creada

    def actualizar(self, db: Session, id_limpieza: int, data: LimpiezaUpdate):
        # Obtener limpieza actual para comparar empleado_id
        limpieza_actual = self.dao.get_by_id(db, id_limpieza)
        empleado_id_anterior = limpieza_actual.empleado_id if limpieza_actual else None
        
        # Actualizar limpieza
        limpieza_actualizada = self.dao.update(db, id_limpieza, data.dict(exclude_unset=True))
        
        if limpieza_actualizada:
            empleado_id_nuevo = limpieza_actualizada.empleado_id
            
            # Enviar notificación solo si:
            # 1. Se asignó un empleado (antes era None y ahora tiene valor)
            # 2. Se cambió el empleado asignado (diferente valor)
            if empleado_id_nuevo and empleado_id_nuevo != empleado_id_anterior:
                self._enviar_notificacion_asignacion(db, limpieza_actualizada)
        
        return limpieza_actualizada

    def eliminar(self, db: Session, id_limpieza: int):
        return self.dao.delete(db, id_limpieza)

    def obtener_por_empleado(self, db: Session, empleado_id: int):
        return self.dao.get_by_empleado(db, empleado_id)

    def obtener_por_habitacion_area(self, db: Session, habitacion_area_id: int):
        return self.dao.get_by_habitacion_area(db, habitacion_area_id)

    def obtener_por_estatus(self, db: Session, estatus_limpieza_id: int):
        return self.dao.get_by_estatus(db, estatus_limpieza_id)

    def obtener_por_fecha(self, db: Session, fecha):
        inicio_dia = datetime.combine(fecha, time.min)
        fin_dia = datetime.combine(fecha, time.max)
    
        limpiezas = self.dao.get_by_rango_fecha(db, inicio_dia, fin_dia)
        return limpiezas

    def crear_masivo(self, db: Session, datos_limpiezas: list):
        """Crea múltiples limpiezas en una sola transacción"""
        limpiezas = []
        for data in datos_limpiezas:
            data_dict = data.dict()
            # Si empleado_id es None o 0, no incluirlo en el modelo
            if data_dict.get('empleado_id') is None or data_dict.get('empleado_id') == 0:
                data_dict.pop('empleado_id', None)
            limpiezas.append(Limpieza(**data_dict))
        return self.dao.crear_masivo(db, limpiezas)