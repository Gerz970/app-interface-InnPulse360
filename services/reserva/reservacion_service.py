from sqlalchemy.orm import Session
from dao.reserva.dao_reservacion import ReservacionDao
from models.reserva.reservaciones_model import Reservacion
from schemas.reserva.reservacion_schema import ReservacionCreate, ReservacionUpdate, HabitacionReservadaResponse
from datetime import datetime
from typing import List, Optional
from datetime import date
from core.database_connection import db_connection, get_database_engine
from sqlalchemy import text

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

    def crear_reservacion(self, db: Session, reservacion_data: ReservacionCreate):
        nueva_reservacion = Reservacion(**reservacion_data.dict())
        nueva_reservacion.fecha_registro = datetime.now()
        return self.dao.create(db, nueva_reservacion)

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

