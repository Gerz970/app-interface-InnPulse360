"""
Servicio de Conversación
Maneja la lógica de negocio para conversaciones
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime

from dao.mensajeria.dao_conversacion import ConversacionDAO
from dao.mensajeria.dao_mensaje import MensajeDAO
from dao.seguridad.dao_usuario import UsuarioDAO
from dao.seguridad.dao_rol_usuario import RolUsuarioDAO
from dao.cliente.dao_cliente import ClienteDAO
from dao.empleado.dao_empleado import EmpleadoDAO
from dao.seguridad.dao_usuario_asignacion import UsuarioAsignacionDAO
from models.mensajeria.conversacion_model import Conversacion
from schemas.mensajeria.conversacion_schema import (
    ConversacionCreateClienteAdmin,
    ConversacionCreateEmpleadoEmpleado,
    ConversacionResponse,
    ConversacionListResponse
)
from schemas.mensajeria.mensaje_schema import MensajeResponse
from core.config import SupabaseSettings


class ConversacionService:
    """
    Servicio para manejar la lógica de negocio de conversaciones
    """
    
    def __init__(self, db_session: Session):
        """
        Inicializa el servicio con una sesión de base de datos
        
        Args:
            db_session (Session): Sesión de SQLAlchemy
        """
        self.db = db_session
        self.dao = ConversacionDAO(db_session)
        self.mensaje_dao = MensajeDAO(db_session)
        self.usuario_dao = UsuarioDAO(db_session)
        self.rol_usuario_dao = RolUsuarioDAO(db_session)
        self.cliente_dao = ClienteDAO(db_session)
        self.empleado_dao = EmpleadoDAO(db_session)
        self.asignacion_dao = UsuarioAsignacionDAO(db_session)
        self.supabase_settings = SupabaseSettings()
    
    def _tiene_rol(self, usuario_id: int, nombre_rol: str) -> bool:
        """
        Verifica si un usuario tiene un rol específico
        
        Args:
            usuario_id (int): ID del usuario
            nombre_rol (str): Nombre del rol a verificar
            
        Returns:
            bool: True si tiene el rol, False si no
        """
        roles = self.rol_usuario_dao.get_user_roles(usuario_id)
        return any(rol.rol.lower() == nombre_rol.lower() for rol in roles)
    
    def _es_cliente(self, usuario_id: int) -> bool:
        """Verifica si un usuario es cliente"""
        return self._tiene_rol(usuario_id, "Cliente")
    
    def _es_administrador(self, usuario_id: int) -> bool:
        """Verifica si un usuario es administrador"""
        return self._tiene_rol(usuario_id, "Administrador")
    
    def _obtener_cliente_id(self, usuario_id: int) -> Optional[int]:
        """Obtiene el ID del cliente asociado a un usuario"""
        asignacion = self.asignacion_dao.get_by_usuario_id(usuario_id)
        if asignacion and asignacion.tipo_asignacion == UsuarioAsignacionDAO.TIPO_CLIENTE:
            return asignacion.cliente_id
        return None
    
    def _obtener_empleado_id(self, usuario_id: int) -> Optional[int]:
        """Obtiene el ID del empleado asociado a un usuario"""
        asignacion = self.asignacion_dao.get_by_usuario_id(usuario_id)
        if asignacion and asignacion.tipo_asignacion == UsuarioAsignacionDAO.TIPO_EMPLEADO:
            return asignacion.empleado_id
        return None
    
    def _obtener_hoteles_empleado(self, empleado_id: int) -> List[int]:
        """
        Obtiene los IDs de hoteles asociados a un empleado
        
        Args:
            empleado_id (int): ID del empleado
            
        Returns:
            List[int]: Lista de IDs de hoteles asociados al empleado
        """
        try:
            hoteles = self.empleado_dao.get_hoteles_by_empleado(empleado_id)
            hotel_ids = [hotel.id_hotel for hotel in hoteles] if hoteles else []
            print(f"🔵 ConversacionService: Empleado {empleado_id} tiene {len(hotel_ids)} hoteles asignados: {hotel_ids}")
            return hotel_ids
        except Exception as e:
            print(f"❌ ConversacionService: Error obteniendo hoteles del empleado {empleado_id}: {e}")
            import traceback
            print(f"❌ ConversacionService: Traceback: {traceback.format_exc()}")
            return []
    
    def crear_conversacion_cliente_admin(
        self, 
        cliente_id: int, 
        admin_id: int,
        usuario_actual_id: int
    ) -> ConversacionResponse:
        """
        Crea una conversación entre un cliente y un administrador
        
        Args:
            cliente_id (int): ID del cliente
            admin_id (int): ID del administrador
            usuario_actual_id (int): ID del usuario que realiza la acción (para validación)
            
        Returns:
            ConversacionResponse: Conversación creada
            
        Raises:
            HTTPException: Si hay error de validación
        """
        # Validar que el usuario actual es el cliente o un admin
        cliente_asignacion = self.asignacion_dao.get_by_cliente_id(cliente_id)
        if not cliente_asignacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente no encontrado"
            )
        
        cliente_usuario_id = cliente_asignacion.usuario_id
        
        if usuario_actual_id != cliente_usuario_id and not self._es_administrador(usuario_actual_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para crear esta conversación"
            )
        
        # Validar que el admin existe y es administrador
        admin = self.usuario_dao.get_by_id(admin_id)
        if not admin:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Administrador no encontrado"
            )
        
        if not self._es_administrador(admin_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario especificado no es un administrador"
            )
        
        # Verificar si ya existe una conversación entre estos usuarios
        conversacion_existente = self.dao.get_by_usuarios(cliente_usuario_id, admin_id)
        if conversacion_existente:
            return ConversacionResponse(
                id_conversacion=conversacion_existente.id_conversacion,
                tipo_conversacion=conversacion_existente.tipo_conversacion,
                usuario1_id=conversacion_existente.usuario1_id,
                usuario2_id=conversacion_existente.usuario2_id,
                cliente_id=conversacion_existente.cliente_id,
                empleado1_id=conversacion_existente.empleado1_id,
                empleado2_id=conversacion_existente.empleado2_id,
                fecha_creacion=conversacion_existente.fecha_creacion,
                fecha_ultimo_mensaje=conversacion_existente.fecha_ultimo_mensaje,
                id_estatus=conversacion_existente.id_estatus
            )
        
        # Crear nueva conversación
        conversacion_data = {
            'tipo_conversacion': 'cliente_admin',
            'usuario1_id': cliente_usuario_id,
            'usuario2_id': admin_id,
            'cliente_id': cliente_id,
            'empleado1_id': None,
            'empleado2_id': None,
            'fecha_creacion': datetime.now(),
            'id_estatus': 1
        }
        
        conversacion = self.dao.create(conversacion_data)
        
        return ConversacionResponse(
            id_conversacion=conversacion.id_conversacion,
            tipo_conversacion=conversacion.tipo_conversacion,
            usuario1_id=conversacion.usuario1_id,
            usuario2_id=conversacion.usuario2_id,
            cliente_id=conversacion.cliente_id,
            empleado1_id=conversacion.empleado1_id,
            empleado2_id=conversacion.empleado2_id,
            fecha_creacion=conversacion.fecha_creacion,
            fecha_ultimo_mensaje=conversacion.fecha_ultimo_mensaje,
            id_estatus=conversacion.id_estatus
        )
    
    def crear_conversacion_empleado_empleado(
        self,
        empleado1_id: int,
        empleado2_id: int,
        usuario_actual_id: int
    ) -> ConversacionResponse:
        """
        Crea una conversación entre dos empleados
        
        Args:
            empleado1_id (int): ID del primer empleado
            empleado2_id (int): ID del segundo empleado
            usuario_actual_id (int): ID del usuario que realiza la acción
            
        Returns:
            ConversacionResponse: Conversación creada
            
        Raises:
            HTTPException: Si hay error de validación
        """
        # Validar que el usuario actual es uno de los empleados
        empleado1_asignacion = self.asignacion_dao.get_by_empleado_id(empleado1_id)
        empleado2_asignacion = self.asignacion_dao.get_by_empleado_id(empleado2_id)
        
        if not empleado1_asignacion or not empleado2_asignacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Uno o ambos empleados no encontrados"
            )
        
        empleado1_usuario_id = empleado1_asignacion.usuario_id
        empleado2_usuario_id = empleado2_asignacion.usuario_id
        
        if usuario_actual_id != empleado1_usuario_id and usuario_actual_id != empleado2_usuario_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para crear esta conversación"
            )
        
        # Verificar si ya existe una conversación entre estos usuarios
        conversacion_existente = self.dao.get_by_usuarios(empleado1_usuario_id, empleado2_usuario_id)
        if conversacion_existente:
            return ConversacionResponse(
                id_conversacion=conversacion_existente.id_conversacion,
                tipo_conversacion=conversacion_existente.tipo_conversacion,
                usuario1_id=conversacion_existente.usuario1_id,
                usuario2_id=conversacion_existente.usuario2_id,
                cliente_id=conversacion_existente.cliente_id,
                empleado1_id=conversacion_existente.empleado1_id,
                empleado2_id=conversacion_existente.empleado2_id,
                fecha_creacion=conversacion_existente.fecha_creacion,
                fecha_ultimo_mensaje=conversacion_existente.fecha_ultimo_mensaje,
                id_estatus=conversacion_existente.id_estatus
            )
        
        # Crear nueva conversación
        conversacion_data = {
            'tipo_conversacion': 'empleado_empleado',
            'usuario1_id': empleado1_usuario_id,
            'usuario2_id': empleado2_usuario_id,
            'cliente_id': None,
            'empleado1_id': empleado1_id,
            'empleado2_id': empleado2_id,
            'fecha_creacion': datetime.now(),
            'id_estatus': 1
        }
        
        conversacion = self.dao.create(conversacion_data)
        
        return ConversacionResponse(
            id_conversacion=conversacion.id_conversacion,
            tipo_conversacion=conversacion.tipo_conversacion,
            usuario1_id=conversacion.usuario1_id,
            usuario2_id=conversacion.usuario2_id,
            cliente_id=conversacion.cliente_id,
            empleado1_id=conversacion.empleado1_id,
            empleado2_id=conversacion.empleado2_id,
            fecha_creacion=conversacion.fecha_creacion,
            fecha_ultimo_mensaje=conversacion.fecha_ultimo_mensaje,
            id_estatus=conversacion.id_estatus
        )
    
    def obtener_conversaciones_usuario(
        self,
        usuario_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[ConversacionListResponse]:
        """
        Obtiene todas las conversaciones de un usuario con información adicional
        Solo retorna conversaciones que tienen al menos un mensaje
        
        Args:
            usuario_id (int): ID del usuario
            skip (int): Número de registros a saltar
            limit (int): Número máximo de registros
            
        Returns:
            List[ConversacionListResponse]: Lista de conversaciones con último mensaje y contador
        """
        try:
            print(f"🔵 ConversacionService: Obteniendo conversaciones para usuario_id={usuario_id}")
            conversaciones = self.dao.get_by_usuario(usuario_id, skip, limit)
            print(f"🔵 ConversacionService: Encontradas {len(conversaciones)} conversaciones en BD")
            
            resultado = []
            conversaciones_sin_mensajes = 0
            
            for idx, conv in enumerate(conversaciones):
                # Obtener último mensaje
                ultimos_mensajes = self.mensaje_dao.get_by_conversacion(conv.id_conversacion, 0, 1)
                
                # FILTRO: Solo incluir conversaciones que tienen al menos un mensaje
                if not ultimos_mensajes:
                    conversaciones_sin_mensajes += 1
                    print(f"🔵 ConversacionService: Conversación {conv.id_conversacion} sin mensajes, omitiendo")
                    continue
                
                ultimo_mensaje = None
                if ultimos_mensajes:
                    msg = ultimos_mensajes[0]
                    ultimo_mensaje = MensajeResponse(
                        id_mensaje=msg.id_mensaje,
                        conversacion_id=msg.conversacion_id,
                        remitente_id=msg.remitente_id,
                        contenido=msg.contenido,
                        fecha_envio=msg.fecha_envio,
                        fecha_leido=msg.fecha_leido,
                        id_estatus=msg.id_estatus,
                        adjuntos=[]
                    )
                
                # Contar mensajes no leídos
                no_leidos = self.mensaje_dao.get_no_leidos(conv.id_conversacion, usuario_id)
                contador_no_leidos = len(no_leidos)
                
                # Obtener información del otro usuario
                otro_usuario_id = conv.usuario2_id if conv.usuario1_id == usuario_id else conv.usuario1_id
                otro_usuario = self.usuario_dao.get_by_id(otro_usuario_id)
                otro_usuario_nombre = otro_usuario.login if otro_usuario else None
                
                # Construir URL completa de foto de perfil si existe
                otro_usuario_foto = None
                if otro_usuario and otro_usuario.url_foto_perfil:
                    # Construir URL completa desde la ruta almacenada
                    ruta_storage = otro_usuario.url_foto_perfil
                    if self.supabase_settings.public_base_url:
                        base_url = self.supabase_settings.public_base_url.rstrip('/')
                        bucket = self.supabase_settings.bucket_images
                        otro_usuario_foto = f"{base_url}/storage/v1/object/public/{bucket}/{ruta_storage}"
                    else:
                        otro_usuario_foto = ruta_storage
                
                try:
                    resultado.append(ConversacionListResponse(
                        id_conversacion=conv.id_conversacion,
                        tipo_conversacion=conv.tipo_conversacion,
                        usuario1_id=conv.usuario1_id,
                        usuario2_id=conv.usuario2_id,
                        cliente_id=conv.cliente_id,
                        empleado1_id=conv.empleado1_id,
                        empleado2_id=conv.empleado2_id,
                        fecha_creacion=conv.fecha_creacion,
                        fecha_ultimo_mensaje=conv.fecha_ultimo_mensaje,
                        id_estatus=conv.id_estatus,
                        ultimo_mensaje=ultimo_mensaje,
                        contador_no_leidos=contador_no_leidos,
                        otro_usuario_id=otro_usuario_id,
                        otro_usuario_nombre=otro_usuario_nombre,
                        otro_usuario_foto=otro_usuario_foto
                    ))
                except Exception as e:
                    print(f"❌ ConversacionService: Error procesando conversación {idx}: {e}")
                    import traceback
                    print(f"❌ ConversacionService: Traceback: {traceback.format_exc()}")
                    raise
            
            print(f"🔵 ConversacionService: Omitidas {conversaciones_sin_mensajes} conversaciones sin mensajes")
            print(f"🔵 ConversacionService: Retornando {len(resultado)} conversaciones procesadas")
            return resultado
        except Exception as e:
            print(f"❌ ConversacionService: Error en obtener_conversaciones_usuario: {e}")
            import traceback
            print(f"❌ ConversacionService: Traceback: {traceback.format_exc()}")
            raise
    
    def obtener_conversacion_por_id(
        self,
        conversacion_id: int,
        usuario_id: int
    ) -> ConversacionResponse:
        """
        Obtiene una conversación por ID con validación de permisos
        
        Args:
            conversacion_id (int): ID de la conversación
            usuario_id (int): ID del usuario que solicita
            
        Returns:
            ConversacionResponse: Conversación encontrada
            
        Raises:
            HTTPException: Si no existe o no tiene permisos
        """
        conversacion = self.dao.get_by_id(conversacion_id)
        
        if not conversacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversación no encontrada"
            )
        
        # Validar que el usuario es participante
        if conversacion.usuario1_id != usuario_id and conversacion.usuario2_id != usuario_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para ver esta conversación"
            )
        
        return ConversacionResponse(
            id_conversacion=conversacion.id_conversacion,
            tipo_conversacion=conversacion.tipo_conversacion,
            usuario1_id=conversacion.usuario1_id,
            usuario2_id=conversacion.usuario2_id,
            cliente_id=conversacion.cliente_id,
            empleado1_id=conversacion.empleado1_id,
            empleado2_id=conversacion.empleado2_id,
            fecha_creacion=conversacion.fecha_creacion,
            fecha_ultimo_mensaje=conversacion.fecha_ultimo_mensaje,
            id_estatus=conversacion.id_estatus
        )
    
    def buscar_usuarios_disponibles(
        self,
        usuario_actual_id: int,
        query: Optional[str] = None
    ) -> List[dict]:
        """
        Busca usuarios disponibles para iniciar conversación según el rol del usuario actual
        
        Reglas:
        - Si es Cliente: muestra solo Administradores
        - Si es Empleado (incluso si también es Admin): muestra solo Empleados del mismo hotel
        
        Args:
            usuario_actual_id (int): ID del usuario actual
            query (Optional[str]): Búsqueda por nombre/login
            
        Returns:
            List[dict]: Lista de usuarios disponibles con información básica
        """
        try:
            print(f"🔵 ConversacionService: Buscando usuarios para usuario_id={usuario_actual_id}, query={query}")
            
            es_cliente = self._es_cliente(usuario_actual_id)
            es_admin = self._es_administrador(usuario_actual_id)
            empleado_id_actual = self._obtener_empleado_id(usuario_actual_id)
            es_empleado = empleado_id_actual is not None
            
            usuarios_disponibles = []
            
            # Normalizar query - convertir string vacío a None
            query_normalizado = query.strip() if query and query.strip() else None
            
            if es_cliente:
                # Cliente puede buscar administradores
                print(f"🔵 ConversacionService: Usuario es Cliente, buscando Administradores")
                todos_usuarios = self.usuario_dao.get_all(0, 1000)
                administradores_encontrados = 0
                
                for usuario in todos_usuarios:
                    if usuario.id_usuario == usuario_actual_id:
                        continue
                    
                    if self._es_administrador(usuario.id_usuario):
                        administradores_encontrados += 1
                        nombre_completo = usuario.login
                        
                        # Aplicar filtro de búsqueda si existe
                        if query_normalizado:
                            if query_normalizado.lower() not in nombre_completo.lower():
                                continue
                        
                        # Construir URL completa de foto de perfil
                        url_foto_completa = None
                        if usuario.url_foto_perfil:
                            ruta_storage = usuario.url_foto_perfil
                            if self.supabase_settings.public_base_url:
                                base_url = self.supabase_settings.public_base_url.rstrip('/')
                                bucket = self.supabase_settings.bucket_images
                                url_foto_completa = f"{base_url}/storage/v1/object/public/{bucket}/{ruta_storage}"
                            else:
                                url_foto_completa = ruta_storage
                        
                        usuarios_disponibles.append({
                            'id_usuario': usuario.id_usuario,
                            'login': usuario.login,
                            'nombre': nombre_completo,
                            'url_foto_perfil': url_foto_completa,
                            'tipo_usuario': 'Administrador'
                        })
                
                print(f"🔵 ConversacionService: Encontrados {administradores_encontrados} administradores, {len(usuarios_disponibles)} después del filtro de query")
            
            elif es_empleado:
                # Empleado puede buscar otros empleados del mismo hotel
                # Si también es admin pero tiene asignación de empleado, usar lógica de empleado
                print(f"🔵 ConversacionService: Usuario es Empleado (empleado_id={empleado_id_actual}), buscando empleados del mismo hotel")
                
                # Obtener hoteles del empleado actual
                hoteles_empleado_actual = self._obtener_hoteles_empleado(empleado_id_actual)
                
                if not hoteles_empleado_actual:
                    print(f"⚠️ ConversacionService: Empleado {empleado_id_actual} no tiene hoteles asignados")
                    return []
                
                # Usar un set para evitar duplicados cuando un empleado está en múltiples hoteles
                empleados_encontrados_por_hotel = {}
                total_empleados_encontrados = 0
                
                # Buscar empleados en cada hotel del empleado actual
                for hotel_id in hoteles_empleado_actual:
                    print(f"🔵 ConversacionService: Buscando empleados en hotel_id={hotel_id}")
                    empleados_hotel = self.empleado_dao.get_all(hotel_id, 0, 1000)
                    print(f"🔵 ConversacionService: Encontrados {len(empleados_hotel)} empleados en hotel {hotel_id}")
                    
                    for empleado in empleados_hotel:
                        # Obtener usuario asociado al empleado
                        asignacion_empleado = self.asignacion_dao.get_by_empleado_id(empleado.id_empleado)
                        if not asignacion_empleado:
                            continue
                        
                        usuario_empleado = self.usuario_dao.get_by_id(asignacion_empleado.usuario_id)
                        if not usuario_empleado:
                            continue
                        
                        # Excluir el usuario actual
                        if usuario_empleado.id_usuario == usuario_actual_id:
                            continue
                        
                        # Evitar duplicados usando el id_usuario como clave
                        if usuario_empleado.id_usuario not in empleados_encontrados_por_hotel:
                            empleados_encontrados_por_hotel[usuario_empleado.id_usuario] = {
                                'empleado': empleado,
                                'usuario': usuario_empleado
                            }
                            total_empleados_encontrados += 1
                
                print(f"🔵 ConversacionService: Total de empleados únicos encontrados: {total_empleados_encontrados}")
                
                # Procesar empleados encontrados y aplicar filtro de query
                for usuario_id, datos in empleados_encontrados_por_hotel.items():
                    empleado = datos['empleado']
                    usuario = datos['usuario']
                    
                    nombre_completo = f"{empleado.nombre} {empleado.apellido_paterno}"
                    
                    # Aplicar filtro de búsqueda si existe
                    if query_normalizado:
                        if (query_normalizado.lower() not in nombre_completo.lower() and 
                            query_normalizado.lower() not in usuario.login.lower()):
                            continue
                    
                    # Construir URL completa de foto de perfil
                    url_foto_completa = None
                    if usuario.url_foto_perfil:
                        ruta_storage = usuario.url_foto_perfil
                        if self.supabase_settings.public_base_url:
                            base_url = self.supabase_settings.public_base_url.rstrip('/')
                            bucket = self.supabase_settings.bucket_images
                            url_foto_completa = f"{base_url}/storage/v1/object/public/{bucket}/{ruta_storage}"
                        else:
                            url_foto_completa = ruta_storage
                    
                    usuarios_disponibles.append({
                        'id_usuario': usuario.id_usuario,
                        'login': usuario.login,
                        'nombre': nombre_completo,
                        'url_foto_perfil': url_foto_completa,
                        'tipo_usuario': 'Empleado',
                        'empleado_id': empleado.id_empleado
                    })
                
                print(f"🔵 ConversacionService: {len(usuarios_disponibles)} empleados después del filtro de query")
            
            elif es_admin:
                # Admin sin asignación de empleado - podría necesitar lógica especial
                # Por ahora, retornar lista vacía o implementar lógica específica
                print(f"⚠️ ConversacionService: Usuario es Admin pero no tiene asignación de empleado")
                # Si es admin puro sin empleado, podría ver todos los empleados o todos los administradores
                # Por ahora retornamos lista vacía hasta definir el comportamiento esperado
                return []
            
            else:
                print(f"⚠️ ConversacionService: Usuario {usuario_actual_id} no tiene rol Cliente ni es Empleado")
                return []
            
            print(f"🔵 ConversacionService: Retornando {len(usuarios_disponibles)} usuarios disponibles")
            return usuarios_disponibles
            
        except Exception as e:
            print(f"❌ ConversacionService: Error en buscar_usuarios_disponibles: {e}")
            import traceback
            print(f"❌ ConversacionService: Traceback: {traceback.format_exc()}")
            raise
    
    def archivar_conversacion(
        self,
        conversacion_id: int,
        usuario_id: int
    ) -> ConversacionResponse:
        """
        Archiva una conversación
        
        Args:
            conversacion_id (int): ID de la conversación
            usuario_id (int): ID del usuario que realiza la acción
            
        Returns:
            ConversacionResponse: Conversación archivada
            
        Raises:
            HTTPException: Si no existe o no tiene permisos
        """
        conversacion = self.dao.get_by_id(conversacion_id)
        
        if not conversacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversación no encontrada"
            )
        
        # Validar que el usuario es participante
        if conversacion.usuario1_id != usuario_id and conversacion.usuario2_id != usuario_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para archivar esta conversación"
            )
        
        conversacion_archivada = self.dao.archivar(conversacion_id)
        
        return ConversacionResponse(
            id_conversacion=conversacion_archivada.id_conversacion,
            tipo_conversacion=conversacion_archivada.tipo_conversacion,
            usuario1_id=conversacion_archivada.usuario1_id,
            usuario2_id=conversacion_archivada.usuario2_id,
            cliente_id=conversacion_archivada.cliente_id,
            empleado1_id=conversacion_archivada.empleado1_id,
            empleado2_id=conversacion_archivada.empleado2_id,
            fecha_creacion=conversacion_archivada.fecha_creacion,
            fecha_ultimo_mensaje=conversacion_archivada.fecha_ultimo_mensaje,
            id_estatus=conversacion_archivada.id_estatus
        )

