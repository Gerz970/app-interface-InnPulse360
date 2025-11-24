from sqlalchemy.orm import Session, joinedload
from dao.reserva.dao_reservacion import ReservacionDao
from models.reserva.reservaciones_model import Reservacion
from schemas.reserva.reservacion_schema import ReservacionCreate, ReservacionUpdate, HabitacionReservadaResponse
from datetime import datetime
from typing import List, Optional
from datetime import date
from core.database_connection import db_connection, get_database_engine
from sqlalchemy import text
import logging
import uuid

logger = logging.getLogger(__name__)

class ReservacionService:
    def __init__(self):
        self.dao = ReservacionDao()

    def listar_reservaciones(self, db: Session):
        return self.dao.get_all(db)

    def obtener_reservacion(self, db: Session, id_reservacion: int):
        return self.dao.get_by_id(db, id_reservacion)

    def obtener_por_cliente(self, db: Session, id_cliente: int) -> List[Reservacion]:
        return self.dao.get_by_cliente(db, id_cliente)

    def obtener_por_habitacion(self, db: Session, habitacion_area_id: int) -> List[Reservacion]:
        return self.dao.get_by_habitacion(db, habitacion_area_id)
    
    def obtener_por_estatus(self, db: Session, estatus: int) -> List[Reservacion]:
        return self.dao.get_by_estatus(db, estatus)

    def obtener_por_fechas(self, db: Session, fecha_inicio: datetime, fecha_fin: datetime) -> List[Reservacion]:
        return self.dao.get_by_fechas(db, fecha_inicio, fecha_fin)

    def _generar_codigo_reservacion_unico(self, db: Session) -> str:
        """
        Genera un código de reservación único usando GUID reducido
        
        Args:
            db: Sesión de base de datos
        
        Returns:
            str: Código de reservación único en formato RES-XXXXXXXX
        """
        max_intentos = 10
        
        for intento in range(max_intentos):
            # Generar GUID y tomar primeros 8 caracteres (sin guiones)
            guid = uuid.uuid4()
            guid_str = str(guid).replace('-', '')  # Remover guiones
            codigo_sufijo = guid_str[:8].upper()  # Primeros 8 caracteres en mayúsculas
            codigo = f"RES-{codigo_sufijo}"
            
            # Verificar que no exista en la base de datos
            reserva_existente = db.query(Reservacion).filter(
                Reservacion.codigo_reservacion == codigo
            ).first()
            
            if not reserva_existente:
                logger.info(f"Código de reservación único generado: {codigo}")
                return codigo
        
        # Si después de varios intentos no se encuentra uno único (muy improbable),
        # usar timestamp + GUID como fallback
        timestamp_suffix = str(int(datetime.now().timestamp() * 1000))[-6:]  # Últimos 6 dígitos
        guid_fallback = str(uuid.uuid4()).replace('-', '')[:2].upper()  # Primeros 2 caracteres
        codigo_fallback = f"RES-{timestamp_suffix}{guid_fallback}"
        logger.warning(f"Usando código fallback después de {max_intentos} intentos: {codigo_fallback}")
        return codigo_fallback

    def crear_reservacion(self, db: Session, reservacion_data: ReservacionCreate):
        """
        Crea una nueva reservación y envía email de cotización con PDF adjunto y notificación push
        
        Args:
            db: Sesión de base de datos
            reservacion_data: Datos de la reservación a crear
        
        Returns:
            Reservacion: Reservación creada
        """
        # Generar código de reservación único si no se proporciona o está vacío
        codigo_reservacion = reservacion_data.codigo_reservacion
        if not codigo_reservacion or codigo_reservacion.strip() == "":
            codigo_reservacion = self._generar_codigo_reservacion_unico(db)
            logger.info(f"Código de reservación generado automáticamente: {codigo_reservacion}")
        else:
            # Si se proporciona un código, verificar que sea único
            reserva_existente = db.query(Reservacion).filter(
                Reservacion.codigo_reservacion == codigo_reservacion
            ).first()
            if reserva_existente:
                logger.warning(f"El código {codigo_reservacion} ya existe, generando uno nuevo")
                codigo_reservacion = self._generar_codigo_reservacion_unico(db)
        
        # Asignar el código generado/validado
        reservacion_dict = reservacion_data.dict()
        reservacion_dict['codigo_reservacion'] = codigo_reservacion
        
        # Crear la reservación
        nueva_reservacion = Reservacion(**reservacion_dict)
        nueva_reservacion.fecha_registro = datetime.now()
        reservacion_creada = self.dao.create(db, nueva_reservacion)
        
        # Enviar email y notificación push de forma asíncrona (no bloquear creación)
        try:
            self._enviar_cotizacion_y_notificacion(db, reservacion_creada)
        except Exception as e:
            # Registrar error pero no fallar la creación de la reserva
            logger.error(f"Error al enviar cotización/notificación para reservación {reservacion_creada.id_reservacion}: {str(e)}")
        
        return reservacion_creada
    
    def _enviar_cotizacion_y_notificacion(self, db: Session, reservacion: Reservacion):
        """
        Envía email de cotización con PDF adjunto y notificación push al cliente
        
        Args:
            db: Sesión de base de datos
            reservacion: Reservación creada
        """
        try:
            # Cargar relaciones necesarias
            from models.hotel.habitacionArea_model import HabitacionArea
            from models.hotel.piso_model import Piso
            from models.hotel.hotel_model import Hotel
            from models.hotel.tipo_habitacion_model import TipoHabitacion
            from models.cliente.cliente_model import Cliente
            
            # Cargar habitación con piso y hotel
            habitacion = db.query(HabitacionArea).options(
                joinedload(HabitacionArea.piso).joinedload(Piso.hotel),
                joinedload(HabitacionArea.tipo_habitacion).joinedload(TipoHabitacion.periodicidad)
            ).filter(
                HabitacionArea.id_habitacion_area == reservacion.habitacion_area_id
            ).first()
            
            if not habitacion:
                logger.error(f"Habitación {reservacion.habitacion_area_id} no encontrada")
                return
            
            # Cargar cliente
            cliente = db.query(Cliente).filter(
                Cliente.id_cliente == reservacion.cliente_id
            ).first()
            
            if not cliente:
                logger.error(f"Cliente {reservacion.cliente_id} no encontrado")
                return
            
            # Obtener información del hotel
            hotel = habitacion.piso.hotel if habitacion.piso else None
            if not hotel:
                logger.error(f"Hotel no encontrado para habitación {habitacion.id_habitacion_area}")
                return
            
            # Obtener tipo de habitación y periodicidad
            tipo_habitacion = habitacion.tipo_habitacion
            if not tipo_habitacion:
                logger.error(f"Tipo de habitación no encontrado para habitación {habitacion.id_habitacion_area}")
                return
            
            periodicidad = tipo_habitacion.periodicidad
            # El modelo Periodicidad usa el atributo 'periodicidad', no 'nombre'
            periodicidad_nombre = periodicidad.periodicidad if periodicidad else "Por noche"
            
            # Calcular precio total
            duracion_dias = reservacion.duracion or 1
            precio_unitario = tipo_habitacion.precio_unitario or 0.0
            
            # Lógica de cálculo de precio (igual que en Flutter)
            if periodicidad and periodicidad.id_periodicidad == 1:  # Por noche
                precio_total = precio_unitario * duracion_dias
            else:  # Por estadía u otra periodicidad
                precio_total = precio_unitario
            
            # Obtener usuario_id desde cliente_id
            from dao.seguridad.dao_usuario_asignacion import UsuarioAsignacionDAO
            usuario_asignacion_dao = UsuarioAsignacionDAO(db)
            
            # Buscar asignación por cliente_id
            asignaciones = usuario_asignacion_dao.get_usuarios_por_cliente(reservacion.cliente_id)
            asignacion = asignaciones[0] if asignaciones else None
            usuario_id = asignacion.usuario_id if asignacion else None
            
            # Formatear fechas
            fecha_entrada_str = reservacion.fecha_reserva.strftime("%d/%m/%Y") if reservacion.fecha_reserva else ""
            fecha_salida_str = reservacion.fecha_salida.strftime("%d/%m/%Y") if reservacion.fecha_salida else ""
            
            # Obtener nombre completo del cliente
            if cliente.tipo_persona == 1:  # Persona física
                nombre_completo = f"{cliente.nombre_razon_social} {cliente.apellido_paterno or ''} {cliente.apellido_materno or ''}".strip()
            else:  # Persona moral
                nombre_completo = cliente.nombre_razon_social or ""
            
            # Obtener y validar email del cliente
            cliente_email = cliente.correo_electronico
            if not cliente_email:
                logger.warning(f"Cliente {reservacion.cliente_id} no tiene correo electrónico registrado. No se enviará email de cotización.")
                logger.warning(f"Nombre del cliente: {nombre_completo}")
            else:
                # Limpiar espacios y convertir a string si es necesario
                cliente_email = str(cliente_email).strip()
                logger.info(f"📧 [Reservación {reservacion.id_reservacion}] Preparando envío de cotización a: {cliente_email}")
                logger.info(f"📧 [Reservación {reservacion.id_reservacion}] Cliente: {nombre_completo} (ID: {reservacion.cliente_id})")
                
                # Validar formato básico de email
                if '@' not in cliente_email or len(cliente_email) < 5:
                    logger.error(f"Email inválido para cliente {reservacion.cliente_id}: '{cliente_email}'. No se enviará correo.")
                else:
                    # Enviar email de cotización
                    try:
                        from services.email.email_service import EmailService
                        email_service = EmailService()
                        
                        logger.info(f"📧 [Reservación {reservacion.id_reservacion}] Enviando email de cotización a: {cliente_email}")
                        
                        resultado = email_service.send_quotation_email(
                            destinatario_email=cliente_email,
                            destinatario_nombre=nombre_completo,
                            codigo_reservacion=reservacion.codigo_reservacion or "",
                            fecha_entrada=fecha_entrada_str,
                            fecha_salida=fecha_salida_str,
                            duracion_dias=duracion_dias,
                            hotel_nombre=hotel.nombre or "",
                            hotel_direccion=hotel.direccion,
                            hotel_telefono=hotel.telefono,
                            hotel_email=hotel.email_contacto,
                            habitacion_nombre=habitacion.nombre_clave or "",
                            habitacion_descripcion=habitacion.descripcion,
                            tipo_habitacion=tipo_habitacion.tipo_habitacion or "",
                            cliente_rfc=cliente.rfc,
                            cliente_identificacion=cliente.documento_identificacion,
                            precio_unitario=precio_unitario,
                            periodicidad_nombre=periodicidad_nombre,
                            precio_total=precio_total
                        )
                        
                        if resultado.success:
                            logger.info(f"✅ [Reservación {reservacion.id_reservacion}] Email de cotización enviado exitosamente a: {cliente_email}")
                        else:
                            logger.error(f"❌ [Reservación {reservacion.id_reservacion}] Error al enviar email a {cliente_email}: {resultado.error}")
                    except Exception as e:
                        logger.error(f"❌ [Reservación {reservacion.id_reservacion}] Excepción al enviar email de cotización a {cliente_email}: {str(e)}")
                        import traceback
                        logger.error(f"Traceback: {traceback.format_exc()}")
            
            # Enviar notificación push
            if usuario_id:
                try:
                    from services.notifications.fcm_push_service import FCMPushService
                    fcm_service = FCMPushService(db)
                    
                    titulo = f"Reservación Confirmada - {reservacion.codigo_reservacion or ''}"
                    mensaje = f"Tu reservación ha sido confirmada. Fecha de entrada: {fecha_entrada_str}"
                    
                    resultado = fcm_service.send_to_user(
                        usuario_id=usuario_id,
                        title=titulo,
                        body=mensaje,
                        data={
                            "tipo": "reservacion_confirmada",
                            "id_reservacion": str(reservacion.id_reservacion),
                            "codigo_reservacion": reservacion.codigo_reservacion or ""
                        }
                    )
                    logger.info(f"Notificación push enviada para reservación {reservacion.id_reservacion}: {resultado}")
                except Exception as e:
                    logger.error(f"Error al enviar notificación push: {str(e)}")
            else:
                logger.warning(f"No se encontró usuario_id para cliente {reservacion.cliente_id}, no se enviará notificación push")
                
        except Exception as e:
            logger.error(f"Error en _enviar_cotizacion_y_notificacion: {str(e)}")
            raise

    def actualizar_reservacion(self, db: Session, id_reservacion: int, reservacion_data: ReservacionUpdate):
        reservacion = self.dao.get_by_id(db, id_reservacion)
        if not reservacion:
            return None
        for key, value in reservacion_data.dict(exclude_unset=True).items():
            setattr(reservacion, key, value)
        return self.dao.update(db, reservacion)

    def eliminar_reservacion(self, db: Session, id_reservacion: int):
        return self.dao.delete(db, id_reservacion)

    def obtener_habitaciones_reservadas_por_cliente(self, db: Session, id_cliente: int) -> List[HabitacionReservadaResponse]:
        resultados = self.dao.get_habitaciones_reservadas_por_cliente(db, id_cliente)
        return [
            HabitacionReservadaResponse(
                id_habitacion_area=row[0],
                nombre_clave=row[1]
            )
            for row in resultados
        ]
    
    def obtener_habitaciones_disponibles(self, fecha_inicio_reservacion: date, fecha_salida: date, limit: int):
        query = text("""
        EXEC Sp_DisponibilidadHabitaciones_Obt 
            :fecha_inicio_reservacion, 
            :fecha_salida
        """)
        engine = get_database_engine()
        with engine.connect() as conn:
            result = conn.execute(query, {
                "fecha_inicio_reservacion": fecha_inicio_reservacion,
                "fecha_salida": fecha_salida
            })
            rows = result.mappings().all() 
        rows = rows[:limit] if limit else rows
        return rows
    
    def listar_reservaciones_filtradas(self, db: Session, incluir_todos_estatus: bool = False, id_hotel: Optional[int] = None) -> List[Reservacion]:
        """
        Lista reservaciones con filtros opcionales.
        
        Args:
            db: Sesión de base de datos
            incluir_todos_estatus: Si True, incluye todas las reservaciones sin importar estatus
            id_hotel: ID del hotel para filtrar. Si es None, trae de todos los hoteles
        
        Returns:
            Lista de reservaciones filtradas
        """
        return self.dao.get_all_with_filters(db, incluir_todos_estatus, id_hotel)
    
    def checkout(self, db: Session, id_reservacion: int):
        return self.dao.checkout(db, id_reservacion)
    
    def obtener_tipos_habitacion_disponibles(self, db: Session, fecha_inicio_reservacion: date, fecha_salida: date, id_hotel: Optional[int] = None):
        """
        Obtiene tipos de habitación disponibles agrupados por tipo con cantidad disponible
        
        Args:
            db: Sesión de base de datos
            fecha_inicio_reservacion: Fecha de inicio de la reservación
            fecha_salida: Fecha de salida
            id_hotel: ID del hotel (opcional, si es None trae de todos los hoteles)
        
        Returns:
            Lista de tipos de habitación con cantidad disponible
        """
        from collections import defaultdict
        from services.hotel.tipo_habitacion_service import TipoHabitacionService
        from schemas.reserva.tipo_habitacion_disponible_schema import TipoHabitacionDisponibleResponse
        
        # Obtener habitaciones disponibles usando el stored procedure existente
        query = text("""
        EXEC Sp_DisponibilidadHabitaciones_Obt 
            :fecha_inicio_reservacion, 
            :fecha_salida
        """)
        engine = get_database_engine()
        with engine.connect() as conn:
            result = conn.execute(query, {
                "fecha_inicio_reservacion": fecha_inicio_reservacion,
                "fecha_salida": fecha_salida
            })
            rows = result.mappings().all()
        
        # Agrupar por tipo_habitacion_id y contar
        habitaciones_por_tipo = defaultdict(int)
        tipo_ids = set()
        
        for row in rows:
            tipo_id = row.get('tipo_habitacion_id')
            if tipo_id:
                # Si se especifica id_hotel, necesitamos obtenerlo de la habitación
                # Por ahora, si no hay filtro de hotel, incluimos todas
                # Si hay filtro, necesitaríamos hacer join con tabla de habitaciones
                # Por simplicidad, si hay filtro de hotel, lo ignoramos por ahora
                # TODO: Implementar filtrado por hotel si el stored procedure no lo devuelve
                habitaciones_por_tipo[tipo_id] += 1
                tipo_ids.add(tipo_id)
        
        # Obtener detalles de cada tipo de habitación con galería
        tipos_disponibles = []
        tipo_service = TipoHabitacionService(db)
        
        for tipo_id in tipo_ids:
            try:
                # Obtener el modelo TipoHabitacion directamente del DAO con periodicidad cargada
                from dao.hotel.dao_tipo_habitacion import TipoHabitacionDAO
                from sqlalchemy.orm import joinedload
                from models.hotel.tipo_habitacion_model import TipoHabitacion
                
                # Obtener tipo con periodicidad cargada usando joinedload
                tipo_modelo = db.query(TipoHabitacion).options(
                    joinedload(TipoHabitacion.periodicidad)
                ).filter(
                    TipoHabitacion.id_tipoHabitacion == tipo_id
                ).first()
                
                if tipo_modelo and tipo_modelo.estatus_id == 1:  # Solo activos
                    # Construir respuesta con galería incluida
                    tipo_response = tipo_service._build_tipo_habitacion_response(
                        tipo_modelo, 
                        incluir_galeria=True
                    )
                    
                    tipos_disponibles.append(
                        TipoHabitacionDisponibleResponse(
                            tipo_habitacion=tipo_response,
                            cantidad_disponible=habitaciones_por_tipo[tipo_id]
                        )
                    )
            except Exception as e:
                print(f"Error al obtener tipo de habitación {tipo_id}: {e}")
                continue
        
        return tipos_disponibles

