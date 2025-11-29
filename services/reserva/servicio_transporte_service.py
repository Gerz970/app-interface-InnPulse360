# services/servicio_transporte_service.py
import threading
import logging
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from dao.reserva.dao_servicio_transporte import ServicioTransporteDAO
from dao.seguridad.dao_usuario_asignacion import UsuarioAsignacionDAO
from schemas.reserva.servicios_transporte_schema import ServicioTransporteCreate, ServicioTransporteUpdate

logger = logging.getLogger(__name__)

class ServicioTransporteService:
    def __init__(self):
        self.dao = ServicioTransporteDAO()

    def listar(self, db: Session, usuario_id: int = None):
        """
        Lista servicios de transporte.
        Si se proporciona usuario_id, filtra solo los servicios del cliente asociado al usuario.
        
        Args:
            db (Session): Sesión de base de datos
            usuario_id (int, optional): ID del usuario autenticado. Si se proporciona, filtra por cliente.
            
        Returns:
            List[ServicioTransporte]: Lista de servicios de transporte
        """
        # Si no se proporciona usuario_id, retornar todos (comportamiento anterior para compatibilidad)
        if usuario_id is None:
            return self.dao.get_all(db)
        
        # Obtener cliente_id desde usuario_id
        usuario_asignacion_dao = UsuarioAsignacionDAO(db)
        asignacion = usuario_asignacion_dao.get_by_usuario_id(usuario_id)
        
        # Validar que el usuario tiene asignación a cliente
        if not asignacion:
            # Usuario sin asignación, retornar lista vacía
            return []
        
        # Validar que es tipo CLIENTE (tipo_asignacion == 2)
        if asignacion.tipo_asignacion != UsuarioAsignacionDAO.TIPO_CLIENTE:
            # No es cliente, retornar lista vacía
            return []
        
        # Obtener cliente_id
        cliente_id = asignacion.cliente_id
        if not cliente_id:
            # No tiene cliente_id asignado, retornar lista vacía
            return []
        
        # Filtrar servicios por cliente
        return self.dao.get_all_by_cliente_id(db, cliente_id)

    def obtener(self, db: Session, id_servicio: int, usuario_id: int = None):
        """
        Obtiene un servicio de transporte por ID.
        Si se proporciona usuario_id, valida que el servicio pertenece al cliente asociado al usuario.
        
        Args:
            db (Session): Sesión de base de datos
            id_servicio (int): ID del servicio de transporte
            usuario_id (int, optional): ID del usuario autenticado. Si se proporciona, valida acceso.
            
        Returns:
            Optional[ServicioTransporte]: Servicio encontrado o None
            
        Raises:
            HTTPException: Si el usuario no tiene acceso al servicio (403)
        """
        # Si no se proporciona usuario_id, usar método original (comportamiento anterior)
        if usuario_id is None:
            return self.dao.get_by_id(db, id_servicio)
        
        # Obtener cliente_id desde usuario_id
        usuario_asignacion_dao = UsuarioAsignacionDAO(db)
        asignacion = usuario_asignacion_dao.get_by_usuario_id(usuario_id)
        
        # Validar que el usuario tiene asignación a cliente
        if not asignacion:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes acceso a este servicio"
            )
        
        # Validar que es tipo CLIENTE (tipo_asignacion == 2)
        if asignacion.tipo_asignacion != UsuarioAsignacionDAO.TIPO_CLIENTE:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes acceso a este servicio"
            )
        
        # Obtener cliente_id
        cliente_id = asignacion.cliente_id
        if not cliente_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes acceso a este servicio"
            )
        
        # Obtener servicio validando que pertenece al cliente
        servicio = self.dao.get_by_id_and_cliente_id(db, id_servicio, cliente_id)
        
        if not servicio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Servicio no encontrado o no tienes acceso a este servicio"
            )
        
        return servicio

    def obtener_por_empleado(self, db: Session, empleado_id: int):
        """
        Obtiene todos los servicios de transporte asignados a un empleado específico
        
        Args:
            db (Session): Sesión de base de datos
            empleado_id (int): ID del empleado/conductor
            
        Returns:
            List[ServicioTransporte]: Lista de servicios de transporte del empleado
        """
        return self.dao.get_all_by_empleado_id(db, empleado_id)

    def crear(self, db: Session, data: ServicioTransporteCreate):
        return self.dao.create(db, data)

    def actualizar(self, db: Session, id_servicio: int, data: ServicioTransporteUpdate):
        """
        Actualiza un servicio de transporte.
        - Si se asigna un empleado (chofer), envía notificación push al transportista.
        - Si se inicia el viaje (estatus 4), envía notificación push al cliente.
        - Si se termina el viaje (estatus 3), envía notificación push al cliente.
        
        Args:
            db (Session): Sesión de base de datos
            id_servicio (int): ID del servicio de transporte
            data (ServicioTransporteUpdate): Datos de actualización
            
        Returns:
            Optional[ServicioTransporte]: Servicio actualizado o None si no existe
        """
        # Obtener servicio actual para comparar empleado_id y estatus
        servicio_actual = self.dao.get_by_id(db, id_servicio)
        if not servicio_actual:
            return None
        
        empleado_id_anterior = servicio_actual.empleado_id
        estatus_anterior = servicio_actual.id_estatus
        
        # Actualizar el servicio
        servicio_actualizado = self.dao.update(db, id_servicio, data)
        
        if servicio_actualizado:
            empleado_id_nuevo = servicio_actualizado.empleado_id
            estatus_nuevo = servicio_actualizado.id_estatus
            
            # Enviar notificación si se asignó un empleado
            # (antes era None y ahora tiene valor, o cambió de valor)
            if empleado_id_nuevo and empleado_id_nuevo != empleado_id_anterior:
                self._enviar_notificacion_asignacion(db, servicio_actualizado)
            
            # Enviar notificación al cliente cuando se inicia el viaje (estatus 4)
            if estatus_nuevo == 4 and estatus_anterior != 4:
                self._enviar_notificacion_inicio_viaje(db, servicio_actualizado)
            
            # Enviar notificación al cliente cuando termina el viaje (estatus 3)
            if estatus_nuevo == 3 and estatus_anterior != 3:
                self._enviar_notificacion_fin_viaje(db, servicio_actualizado)
        
        return servicio_actualizado
    
    def _enviar_notificacion_asignacion(self, db: Session, servicio):
        """
        Envía notificación push al transportista cuando se le asigna un viaje.
        Se ejecuta en un hilo separado para no bloquear la respuesta principal.
        
        Args:
            db (Session): Sesión de base de datos
            servicio: ServicioTransporte actualizado con empleado asignado
        """
        # Guardar datos necesarios antes de pasar al hilo
        servicio_id = servicio.id_servicio_transporte
        empleado_id = servicio.empleado_id
        destino = servicio.destino
        
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
                    
                    # Recargar servicio con relaciones desde BD del hilo
                    from sqlalchemy.orm import joinedload
                    from models.reserva.servicios_transporte_model import ServicioTransporte
                    
                    servicio_completo = db_background.query(ServicioTransporte).options(
                        joinedload(ServicioTransporte.empleado)
                    ).filter(ServicioTransporte.id_servicio_transporte == servicio_id).first()
                    
                    if not servicio_completo:
                        logger.warning(f"No se encontró servicio transporte {servicio_id} para notificación")
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
                    
                    # Formatear fecha y hora para el mensaje
                    fecha_str = servicio_completo.fecha_servicio.strftime("%d/%m/%Y") if servicio_completo.fecha_servicio else ""
                    hora_str = servicio_completo.hora_servicio.strftime("%H:%M") if servicio_completo.hora_servicio else ""
                    destino_actualizado = servicio_completo.destino or destino
                    
                    # Enviar notificación
                    push_service.send_to_user(
                        usuario_id=usuario_id,
                        title="Nuevo viaje asignado",
                        body=f"Se te ha asignado un viaje a {destino_actualizado}. Fecha: {fecha_str} Hora: {hora_str}",
                        data={
                            "tipo": "transporte_asignado",
                            "servicio_id": str(servicio_id),
                            "empleado_id": str(empleado_id),
                            "destino": destino_actualizado,
                            "screen": "transportista_detail"
                        }
                    )
                    
                    logger.info(f"✅ Notificación enviada al usuario {usuario_id} (empleado_id: {empleado_id}) por servicio transporte {servicio_id}")
                    
                finally:
                    # Cerrar sesión de BD del hilo
                    db_background.close()
                    
            except Exception as e:
                # No fallar la operación principal si falla la notificación
                logger.error(f"❌ Error enviando notificación de transporte: {e}", exc_info=True)
        
        # Iniciar hilo en background sin esperar (daemon=True permite que el programa termine sin esperar el hilo)
        thread = threading.Thread(target=enviar_en_background, daemon=True)
        thread.start()
    
    def _obtener_cliente_usuario_id(self, db: Session, servicio_id: int):
        """
        Obtiene el usuario_id del cliente asociado a un servicio de transporte
        a través de: ServicioTransporte → CargoServicioTransporte → Cargo → Reservacion → Cliente → UsuarioAsignacion
        
        Args:
            db (Session): Sesión de base de datos
            servicio_id (int): ID del servicio de transporte
            
        Returns:
            Optional[int]: usuario_id del cliente o None si no se encuentra
        """
        from models.reserva.servicios_transporte_model import ServicioTransporte
        from models.reserva.cargo_servicio_transporte_model import CargoServicioTransporte
        from models.reserva.cargos_model import Cargo
        from models.reserva.reservaciones_model import Reservacion
        from models.seguridad.usuario_asignacion_model import UsuarioAsignacion
        
        servicio = db.query(ServicioTransporte).filter(
            ServicioTransporte.id_servicio_transporte == servicio_id
        ).first()
        
        if not servicio:
            return None
        
        # Obtener cargo asociado
        cargo_servicio = db.query(CargoServicioTransporte).filter(
            CargoServicioTransporte.servicio_transporte_id == servicio_id
        ).first()
        
        if not cargo_servicio:
            return None
        
        # Obtener reservación
        cargo = db.query(Cargo).filter(Cargo.id_cargo == cargo_servicio.cargo_id).first()
        if not cargo:
            return None
        
        reservacion = db.query(Reservacion).filter(
            Reservacion.id_reservacion == cargo.reservacion_id
        ).first()
        
        if not reservacion or not reservacion.cliente_id:
            return None
        
        # Obtener usuario_id del cliente
        usuario_asignacion = db.query(UsuarioAsignacion).filter(
            UsuarioAsignacion.cliente_id == reservacion.cliente_id,
            UsuarioAsignacion.tipo_asignacion == 2,  # 2=Cliente
            UsuarioAsignacion.estatus == 1  # Activo
        ).first()
        
        return usuario_asignacion.usuario_id if usuario_asignacion else None
    
    def _enviar_notificacion_inicio_viaje(self, db: Session, servicio):
        """
        Envía notificación push al cliente cuando se inicia el viaje.
        Se ejecuta en un hilo separado para no bloquear la respuesta principal.
        
        Args:
            db (Session): Sesión de base de datos
            servicio: ServicioTransporte con estatus 4 (En Curso)
        """
        # Guardar datos necesarios antes de pasar al hilo
        servicio_id = servicio.id_servicio_transporte
        destino = servicio.destino
        
        # Ejecutar en hilo separado para no bloquear la respuesta
        def enviar_en_background():
            try:
                # Crear nueva sesión de BD para el hilo
                from core.database_connection import get_database_session
                from sqlalchemy.orm import joinedload
                from models.reserva.servicios_transporte_model import ServicioTransporte
                
                db_background = next(get_database_session())
                
                try:
                    # Recargar servicio con relaciones desde BD del hilo
                    servicio_completo = db_background.query(ServicioTransporte).options(
                        joinedload(ServicioTransporte.empleado)
                    ).filter(ServicioTransporte.id_servicio_transporte == servicio_id).first()
                    
                    if not servicio_completo:
                        logger.warning(f"No se encontró servicio transporte {servicio_id} para notificación de inicio")
                        return
                    
                    # Obtener usuario_id del cliente
                    usuario_id = self._obtener_cliente_usuario_id(db_background, servicio_id)
                    
                    if not usuario_id:
                        logger.info(f"No se encontró usuario cliente para servicio transporte {servicio_id}")
                        return
                    
                    # Importar aquí para evitar importación circular
                    from services.notifications.fcm_push_service import FCMPushService
                    
                    # Crear servicio de notificaciones con nueva sesión
                    push_service = FCMPushService(db_background)
                    
                    # Formatear fecha y hora para el mensaje
                    fecha_str = servicio_completo.fecha_servicio.strftime("%d/%m/%Y") if servicio_completo.fecha_servicio else ""
                    hora_str = servicio_completo.hora_servicio.strftime("%H:%M") if servicio_completo.hora_servicio else ""
                    destino_actualizado = servicio_completo.destino or destino
                    
                    # Enviar notificación
                    push_service.send_to_user(
                        usuario_id=usuario_id,
                        title="Tu viaje ha comenzado",
                        body=f"El conductor ha iniciado el viaje a {destino_actualizado}. Fecha: {fecha_str} Hora: {hora_str}",
                        data={
                            "tipo": "transporte_iniciado",
                            "servicio_id": str(servicio_id),
                            "destino": destino_actualizado,
                            "screen": "transporte_detail"
                        }
                    )
                    
                    logger.info(f"✅ Notificación de inicio de viaje enviada al cliente {usuario_id} por servicio {servicio_id}")
                    
                finally:
                    # Cerrar sesión de BD del hilo
                    db_background.close()
                    
            except Exception as e:
                # No fallar la operación principal si falla la notificación
                logger.error(f"❌ Error enviando notificación de inicio de viaje: {e}", exc_info=True)
        
        # Iniciar hilo en background sin esperar
        thread = threading.Thread(target=enviar_en_background, daemon=True)
        thread.start()
    
    def _enviar_notificacion_fin_viaje(self, db: Session, servicio):
        """
        Envía notificación push al cliente cuando termina el viaje.
        Se ejecuta en un hilo separado para no bloquear la respuesta principal.
        
        Args:
            db (Session): Sesión de base de datos
            servicio: ServicioTransporte con estatus 3 (Terminado)
        """
        # Guardar datos necesarios antes de pasar al hilo
        servicio_id = servicio.id_servicio_transporte
        destino = servicio.destino
        
        # Ejecutar en hilo separado para no bloquear la respuesta
        def enviar_en_background():
            try:
                # Crear nueva sesión de BD para el hilo
                from core.database_connection import get_database_session
                from sqlalchemy.orm import joinedload
                from models.reserva.servicios_transporte_model import ServicioTransporte
                
                db_background = next(get_database_session())
                
                try:
                    # Recargar servicio con relaciones desde BD del hilo
                    servicio_completo = db_background.query(ServicioTransporte).options(
                        joinedload(ServicioTransporte.empleado)
                    ).filter(ServicioTransporte.id_servicio_transporte == servicio_id).first()
                    
                    if not servicio_completo:
                        logger.warning(f"No se encontró servicio transporte {servicio_id} para notificación de fin")
                        return
                    
                    # Obtener usuario_id del cliente
                    usuario_id = self._obtener_cliente_usuario_id(db_background, servicio_id)
                    
                    if not usuario_id:
                        logger.info(f"No se encontró usuario cliente para servicio transporte {servicio_id}")
                        return
                    
                    # Importar aquí para evitar importación circular
                    from services.notifications.fcm_push_service import FCMPushService
                    
                    # Crear servicio de notificaciones con nueva sesión
                    push_service = FCMPushService(db_background)
                    
                    destino_actualizado = servicio_completo.destino or destino
                    
                    # Enviar notificación
                    push_service.send_to_user(
                        usuario_id=usuario_id,
                        title="Tu viaje ha finalizado",
                        body=f"El viaje a {destino_actualizado} ha sido completado. Puedes calificar el servicio.",
                        data={
                            "tipo": "transporte_terminado",
                            "servicio_id": str(servicio_id),
                            "destino": destino_actualizado,
                            "screen": "transporte_detail"
                        }
                    )
                    
                    logger.info(f"✅ Notificación de fin de viaje enviada al cliente {usuario_id} por servicio {servicio_id}")
                    
                finally:
                    # Cerrar sesión de BD del hilo
                    db_background.close()
                    
            except Exception as e:
                # No fallar la operación principal si falla la notificación
                logger.error(f"❌ Error enviando notificación de fin de viaje: {e}", exc_info=True)
        
        # Iniciar hilo en background sin esperar
        thread = threading.Thread(target=enviar_en_background, daemon=True)
        thread.start()

    def eliminar(self, db: Session, id_servicio: int):
        return self.dao.delete(db, id_servicio)

    def obtener_servicio_hotel(self, db: Session, id_hotel: int, estatus: int):
        servicio = self.dao.obtener_servicios_por_hotel(db, id_hotel, estatus)
        
        if not servicio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Servicio no encontrado o no tienes acceso a este servicio"
            )
        
        return servicio