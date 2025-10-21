"""
Servicio de Usuario
Maneja la lógica de negocio para usuarios, incluyendo encriptación de contraseñas
"""

from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status

from dao.seguridad.dao_usuario import UsuarioDAO
from dao.seguridad.dao_roles import RolesDAO
from dao.seguridad.dao_rol_usuario import RolUsuarioDAO
from dao.seguridad.dao_usuario_asignacion import UsuarioAsignacionDAO
from dao.cliente.dao_cliente import ClienteDAO
from models.seguridad.usuario_model import Usuario
from schemas.seguridad.usuario_create import UsuarioCreate
from schemas.seguridad.usuario_update import UsuarioUpdate
from schemas.seguridad.usuario_response import UsuarioResponse
from schemas.seguridad.auth_schemas import UsuarioLogin, Token, TokenData
from schemas.seguridad.usuario_rol_schemas import RolSimpleResponse
from schemas.seguridad.registro_cliente_schemas import (
    VerificarDisponibilidadRequest,
    VerificarDisponibilidadResponse,
    RegistroClienteRequest,
    RegistroClienteResponse,
    CambiarPasswordTemporalRequest,
    CambiarPasswordTemporalResponse,
    ClienteEncontradoInfo
)
from schemas.cliente.cliente_formulario import ClienteFormularioData
from core.config import AuthSettings
from utils.password_generator import generar_password_temporal, validar_fortaleza_password

# Configuración para encriptación de contraseñas
# Argon2 es más moderno y seguro que bcrypt, sin limitaciones de longitud
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


class UsuarioService:
    """
    Servicio para manejar la lógica de negocio de usuarios
    Incluye encriptación de contraseñas y autenticación
    """
    
    def __init__(self, db_session: Session):
        """
        Inicializa el servicio con una sesión de base de datos
        
        Args:
            db_session (Session): Sesión de SQLAlchemy
        """
        self.db = db_session
        self.dao = UsuarioDAO(db_session)
        self.roles_dao = RolesDAO(db_session)
        self.rol_usuario_dao = RolUsuarioDAO(db_session)
        self.asignacion_dao = UsuarioAsignacionDAO(db_session)
        self.cliente_dao = ClienteDAO(db_session)
    
    def _hash_password(self, password: str) -> str:
        """
        Encripta una contraseña usando Argon2
        
        Args:
            password (str): Contraseña en texto plano (sin límite de longitud)
            
        Returns:
            str: Contraseña encriptada
        """
        return pwd_context.hash(password)
    
    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verifica si una contraseña coincide con su hash usando Argon2
        
        Args:
            plain_password (str): Contraseña en texto plano
            hashed_password (str): Contraseña encriptada
            
        Returns:
            bool: True si coinciden, False si no
        """
        return pwd_context.verify(plain_password, hashed_password)
    
    def _get_usuario_roles(self, usuario_id: int) -> List[RolSimpleResponse]:
        """
        Obtiene los roles de un usuario
        
        Args:
            usuario_id (int): ID del usuario
            
        Returns:
            List[RolSimpleResponse]: Lista de roles del usuario
        """
        roles = self.rol_usuario_dao.get_user_roles(usuario_id)
        return [
            RolSimpleResponse(
                id_rol=rol.id_rol,
                rol=rol.rol
            )
            for rol in roles
        ]
    
    def _create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Crea un token JWT de acceso
        
        Args:
            data (dict): Datos a incluir en el token
            expires_delta (Optional[timedelta]): Tiempo de expiración personalizado
            
        Returns:
            str: Token JWT
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=AuthSettings.access_token_expire_minutes)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, AuthSettings.secret_key, algorithm=AuthSettings.algorithm)
        return encoded_jwt
    
    def create_usuario(self, usuario_data: UsuarioCreate) -> UsuarioResponse:
        """
        Crea un nuevo usuario con contraseña encriptada
        
        Args:
            usuario_data (UsuarioCreate): Datos del usuario
            
        Returns:
            UsuarioResponse: Usuario creado (sin contraseña)
            
        Raises:
            HTTPException: Si el login o email ya existen
        """
        # Verificar si el login ya existe
        if self.dao.exists_by_login(usuario_data.login):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El login ya está en uso"
            )
        
        # Verificar si el email ya existe
        if self.dao.exists_by_email(usuario_data.correo_electronico):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo electrónico ya está en uso"
            )
        
        # Verificar que todos los roles existen y están activos (si se proporcionan)
        if usuario_data.roles_ids:
            for rol_id in usuario_data.roles_ids:
                rol = self.roles_dao.get_by_id(rol_id)
                if not rol or rol.estatus_id != 1:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Rol con ID {rol_id} no encontrado o inactivo"
                    )
        
        # Encriptar la contraseña
        hashed_password = self._hash_password(usuario_data.password)
        
        # Crear el usuario con contraseña encriptada
        usuario_data.password = hashed_password
        db_usuario = self.dao.create(usuario_data)
        
        # Asignar roles si se proporcionaron
        if usuario_data.roles_ids:
            self.rol_usuario_dao.bulk_assign_roles_to_usuario(db_usuario.id_usuario, usuario_data.roles_ids)
        
        # Obtener roles asignados
        roles = self._get_usuario_roles(db_usuario.id_usuario)
        
        # Retornar con los roles
        return UsuarioResponse(
            id_usuario=db_usuario.id_usuario,
            login=db_usuario.login,
            correo_electronico=db_usuario.correo_electronico,
            estatus_id=db_usuario.estatus_id,
            roles=roles
        )
    
    def get_usuario_by_id(self, id_usuario: int) -> Optional[UsuarioResponse]:
        """
        Obtiene un usuario por ID
        
        Args:
            id_usuario (int): ID del usuario
            
        Returns:
            Optional[UsuarioResponse]: Usuario encontrado o None
        """
        db_usuario = self.dao.get_by_id(id_usuario)
        if not db_usuario:
            return None
        
        # Obtener roles del usuario
        roles = self._get_usuario_roles(id_usuario)
        
        return UsuarioResponse(
            id_usuario=db_usuario.id_usuario,
            login=db_usuario.login,
            correo_electronico=db_usuario.correo_electronico,
            estatus_id=db_usuario.estatus_id,
            roles=roles
        )
    
    def get_usuario_by_login(self, login: str) -> Optional[UsuarioResponse]:
        """
        Obtiene un usuario por login
        
        Args:
            login (str): Login del usuario
            
        Returns:
            Optional[UsuarioResponse]: Usuario encontrado o None
        """
        db_usuario = self.dao.get_by_login(login)
        if not db_usuario:
            return None
        
        # Obtener roles del usuario
        roles = self._get_usuario_roles(db_usuario.id_usuario)
        
        return UsuarioResponse(
            id_usuario=db_usuario.id_usuario,
            login=db_usuario.login,
            correo_electronico=db_usuario.correo_electronico,
            estatus_id=db_usuario.estatus_id,
            roles=roles
        )
    
    def get_all_usuarios(self, skip: int = 0, limit: int = 100) -> List[UsuarioResponse]:
        """
        Obtiene una lista de usuarios
        
        Args:
            skip (int): Registros a saltar
            limit (int): Límite de registros
            
        Returns:
            List[UsuarioResponse]: Lista de usuarios
        """
        db_usuarios = self.dao.get_active_users(skip, limit)
        return [
            UsuarioResponse(
                id_usuario=usuario.id_usuario,
                login=usuario.login,
                correo_electronico=usuario.correo_electronico,
                estatus_id=usuario.estatus_id,
                roles=self._get_usuario_roles(usuario.id_usuario)
            )
            for usuario in db_usuarios
        ]
    
    def update_usuario(self, id_usuario: int, usuario_data: UsuarioUpdate) -> Optional[UsuarioResponse]:
        """
        Actualiza un usuario existente
        
        Args:
            id_usuario (int): ID del usuario
            usuario_data (UsuarioUpdate): Datos a actualizar
            
        Returns:
            Optional[UsuarioResponse]: Usuario actualizado o None
            
        Raises:
            HTTPException: Si hay conflictos de login o email
        """
        # Verificar si el usuario existe
        existing_usuario = self.dao.get_by_id(id_usuario)
        if not existing_usuario:
            return None
        
        # Verificar conflictos de login si se está actualizando
        if usuario_data.login and usuario_data.login != existing_usuario.login:
            if self.dao.exists_by_login(usuario_data.login, exclude_id=id_usuario):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El login ya está en uso"
                )
        
        # Verificar conflictos de email si se está actualizando
        if usuario_data.correo_electronico and usuario_data.correo_electronico != existing_usuario.correo_electronico:
            if self.dao.exists_by_email(usuario_data.correo_electronico, exclude_id=id_usuario):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El correo electrónico ya está en uso"
                )
        
        # Encriptar nueva contraseña si se proporciona
        if usuario_data.password:
            usuario_data.password = self._hash_password(usuario_data.password)
        
        # Actualizar el usuario
        db_usuario = self.dao.update(id_usuario, usuario_data)
        if not db_usuario:
            return None
        
        # Obtener roles del usuario
        roles = self._get_usuario_roles(id_usuario)
        
        return UsuarioResponse(
            id_usuario=db_usuario.id_usuario,
            login=db_usuario.login,
            correo_electronico=db_usuario.correo_electronico,
            estatus_id=db_usuario.estatus_id,
            roles=roles
        )
    
    def delete_usuario(self, id_usuario: int) -> bool:
        """
        Eliminación lógica de un usuario
        
        Args:
            id_usuario (int): ID del usuario
            
        Returns:
            bool: True si se eliminó correctamente
        """
        return self.dao.delete_logical(id_usuario)
    
    def authenticate_user(self, login: str, password: str) -> Optional[Usuario]:
        """
        Autentica un usuario verificando login y contraseña
        
        Args:
            login (str): Login del usuario
            password (str): Contraseña en texto plano
            
        Returns:
            Optional[Usuario]: Usuario autenticado o None
        """
        usuario = self.dao.get_by_login(login)
        if not usuario:
            return None
        
        if not self._verify_password(password, usuario.password):
            return None
        
        return usuario
    
    def login(self, login_data: UsuarioLogin) -> Token:
        """
        Realiza el login del usuario y retorna un token JWT
        
        Args:
            login_data (UsuarioLogin): Datos de login
            
        Returns:
            Token: Token JWT con información del usuario
            
        Raises:
            HTTPException: Si las credenciales son inválidas
        """
        # Autenticar usuario
        usuario = self.authenticate_user(login_data.login, login_data.password)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Verificar que el usuario esté activo
        if usuario.estatus_id != 1:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario inactivo",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # ⚠️ VALIDAR SI TIENE PASSWORD TEMPORAL
        password_temporal_info = None
        if usuario.password_temporal:
            # Verificar si la password temporal ha expirado
            if usuario.password_expira and datetime.utcnow() > usuario.password_expira:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="La contraseña temporal ha expirado. Por favor, contacte al administrador.",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            # Calcular días restantes
            dias_restantes = 0
            if usuario.password_expira:
                dias_restantes = (usuario.password_expira - datetime.utcnow()).days
            
            password_temporal_info = {
                "requiere_cambio": True,
                "password_expira": usuario.password_expira.isoformat() if usuario.password_expira else None,
                "dias_restantes": dias_restantes,
                "mensaje": f"Debe cambiar su contraseña temporal. Expira en {dias_restantes} días."
            }
        
        # Crear token de acceso
        access_token_expires = timedelta(minutes=AuthSettings.access_token_expire_minutes)
        access_token = self._create_access_token(
            data={
                "sub": str(usuario.id_usuario),
                "login": usuario.login,
                "correo_electronico": usuario.correo_electronico
            },
            expires_delta=access_token_expires
        )
        
        # Preparar respuesta del token
        token_response = Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=AuthSettings.access_token_expire_minutes * 60,  # En segundos
            user_info={
                "id_usuario": usuario.id_usuario,
                "login": usuario.login,
                "correo_electronico": usuario.correo_electronico
            }
        )
        
        # Agregar información de password temporal si aplica
        if password_temporal_info:
            token_response.user_info["password_temporal"] = password_temporal_info
        
        return token_response
    
    def get_current_user(self, token: str) -> Optional[UsuarioResponse]:
        """
        Obtiene el usuario actual desde un token JWT
        
        Args:
            token (str): Token JWT
            
        Returns:
            Optional[UsuarioResponse]: Usuario actual o None
            
        Raises:
            HTTPException: Si el token es inválido
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudieron validar las credenciales",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            payload = jwt.decode(token, AuthSettings.secret_key, algorithms=[AuthSettings.algorithm])
            id_usuario: str = payload.get("sub")
            if id_usuario is None:
                raise credentials_exception
            
            token_data = TokenData(
                id_usuario=int(id_usuario),
                login=payload.get("login"),
                correo_electronico=payload.get("correo_electronico")
            )
        except JWTError:
            raise credentials_exception
        
        # Verificar que el usuario aún existe y está activo
        usuario = self.dao.get_by_id(token_data.id_usuario)
        if usuario is None or usuario.estatus_id != 1:
            raise credentials_exception
        
        # Obtener roles del usuario
        roles = self._get_usuario_roles(usuario.id_usuario)
        
        return UsuarioResponse(
            id_usuario=usuario.id_usuario,
            login=usuario.login,
            correo_electronico=usuario.correo_electronico,
            estatus_id=usuario.estatus_id,
            roles=roles
        )
    
    # ==================== MÉTODOS PARA REGISTRO DE CLIENTES ====================
    
    def verificar_disponibilidad_registro(
        self, 
        request: VerificarDisponibilidadRequest
    ) -> VerificarDisponibilidadResponse:
        """
        Verifica disponibilidad de login y si existe cliente con el correo
        
        Args:
            request (VerificarDisponibilidadRequest): Datos a verificar
            
        Returns:
            VerificarDisponibilidadResponse: Resultado de verificación
        """
        # Verificar si el login ya existe
        login_existe = self.dao.exists_by_login(request.login)
        login_disponible = not login_existe
        
        # Buscar cliente por correo
        cliente = self.cliente_dao.get_by_correo_electronico(request.correo_electronico)
        correo_en_clientes = cliente is not None
        
        # Preparar datos del cliente si existe
        cliente_data = None
        if cliente:
            # Crear datos completos del cliente usando **data - ¡Automático!
            cliente_data = ClienteFormularioData.model_validate(cliente)
        
        # Determinar si puede registrar
        puede_registrar = login_disponible and correo_en_clientes
        
        # Generar mensaje
        if not login_disponible:
            mensaje = f"El login '{request.login}' ya está en uso"
        elif not correo_en_clientes:
            mensaje = f"No se encontró cliente con el correo '{request.correo_electronico}'"
        else:
            mensaje = f"Login disponible. Se encontró cliente '{cliente.nombre_razon_social}'"
        
        return VerificarDisponibilidadResponse(
            login_disponible=login_disponible,
            correo_en_clientes=correo_en_clientes,
            cliente=cliente_data,
            puede_registrar=puede_registrar,
            mensaje=mensaje
        )
    
    def registrar_usuario_cliente(
        self,
        request: RegistroClienteRequest
    ) -> RegistroClienteResponse:
        """
        Registra un nuevo usuario asociado a un cliente
        
        Args:
            request (RegistroClienteRequest): Datos del registro
            
        Returns:
            RegistroClienteResponse: Resultado del registro
            
        Raises:
            ValueError: Si hay errores de validación
        """
        # 1. Verificar que login no exista
        if self.dao.exists_by_login(request.login):
            raise ValueError(f"El login '{request.login}' ya está en uso")
        
        # 2. Verificar que cliente existe
        cliente = self.cliente_dao.get_by_id(request.cliente_id)
        if not cliente:
            raise ValueError(f"No se encontró cliente con ID {request.cliente_id}")
        
        # 3. Verificar que el correo coincide con el del cliente
        if cliente.correo_electronico != request.correo_electronico:
            raise ValueError("El correo no coincide con el del cliente")
        
        # 4. Generar o validar password
        password_temporal_generada = False
        password_temp = None
        password_expira = None
        
        if request.password:
            # Validar fortaleza de password proporcionada
            es_valida, mensaje = validar_fortaleza_password(request.password)
            if not es_valida:
                raise ValueError(mensaje)
            password_final = request.password
        else:
            # Generar password temporal
            password_temp = generar_password_temporal()
            password_final = password_temp
            password_temporal_generada = True
            password_expira = datetime.utcnow() + timedelta(days=7)
        
        # 5. Crear usuario
        usuario_data = UsuarioCreate(
            login=request.login,
            correo_electronico=request.correo_electronico,
            password=password_final,
            estatus_id=1,
            roles_ids=[]  # Se asignará el rol después
        )
        
        usuario_creado = self.create_usuario(usuario_data)
        
        # 6. Actualizar campos de password temporal si aplica
        if password_temporal_generada:
            usuario_db = self.dao.get_by_id(usuario_creado.id_usuario)
            usuario_db.password_temporal = True
            usuario_db.password_expira = password_expira
            self.db.commit()
        
        # 7. Obtener rol "Cliente"
        rol_cliente = self.roles_dao.get_by_nombre("Cliente")
        if not rol_cliente:
            raise ValueError("No se encontró el rol 'Cliente'. Debe crearse en la base de datos.")
        
        # 8. Asignar rol "Cliente"
        self.rol_usuario_dao.assign_role_to_user(usuario_creado.id_usuario, rol_cliente.id_rol)
        
        # 9. Crear asignación usuario-cliente
        self.asignacion_dao.crear_asignacion_cliente(usuario_creado.id_usuario, cliente.id_cliente)
        
        # 10. Enviar credenciales por email si se generó password temporal
        email_enviado = self._enviar_credenciales_email(
            password_temporal_generada=password_temporal_generada,
            cliente=cliente,
            login=request.login,
            password_temp=password_temp,
            password_expira=password_expira
        )
        
        # 11. Preparar respuesta
        cliente_info = ClienteEncontradoInfo(
            id_cliente=cliente.id_cliente,
            nombre_razon_social=cliente.nombre_razon_social,
            rfc=cliente.rfc,
            tipo_persona=cliente.tipo_persona,
            correo_electronico=cliente.correo_electronico
        )
        
        # Preparar mensaje basado en el resultado
        if password_temporal_generada:
            if email_enviado:
                mensaje = "Usuario creado exitosamente. Se han enviado las credenciales al correo electrónico proporcionado."
            else:
                mensaje = "Usuario creado exitosamente. ADVERTENCIA: No se pudo enviar el email con las credenciales. Contacte al administrador."
        else:
            mensaje = "Usuario creado y asociado al cliente exitosamente."
        
        # IMPORTANTE: NO devolver password_temporal ni password_expira por seguridad
        # Las credenciales se envían ÚNICAMENTE por email
        return RegistroClienteResponse(
            usuario_creado=True,
            id_usuario=usuario_creado.id_usuario,
            login=usuario_creado.login,
            correo_electronico=usuario_creado.correo_electronico,
            cliente_asociado=cliente_info,
            rol_asignado="Cliente",
            password_temporal_generada=password_temporal_generada,
            email_enviado=email_enviado,
            mensaje=mensaje
        )
    
    def cambiar_password_temporal(
        self,
        request: CambiarPasswordTemporalRequest
    ) -> CambiarPasswordTemporalResponse:
        """
        Cambia una contraseña temporal por una definitiva
        
        Args:
            request (CambiarPasswordTemporalRequest): Datos del cambio
            
        Returns:
            CambiarPasswordTemporalResponse: Resultado del cambio
            
        Raises:
            ValueError: Si hay errores de validación
        """
        # 1. Buscar usuario por login
        usuario = self.dao.get_by_login(request.login)
        if not usuario:
            raise ValueError("Usuario no encontrado")
        
        # 2. Verificar que la password actual es correcta
        if not self._verify_password(request.password_actual, usuario.password):
            raise ValueError("Contraseña actual incorrecta")
        
        # 3. Verificar que tiene password temporal
        if not usuario.password_temporal:
            raise ValueError("Este usuario no tiene una contraseña temporal")
        
        # 4. Verificar que no ha expirado
        if usuario.password_expira and datetime.utcnow() > usuario.password_expira:
            raise ValueError("La contraseña temporal ha expirado. Solicite una nueva.")
        
        # 5. Validar nueva password
        es_valida, mensaje = validar_fortaleza_password(request.password_nueva)
        if not es_valida:
            raise ValueError(mensaje)
        
        # 6. Actualizar password
        usuario.password = self._hash_password(request.password_nueva)
        usuario.password_temporal = False
        usuario.password_expira = None
        usuario.fecha_ultimo_cambio_password = datetime.utcnow()
        
        self.db.commit()
        
        return CambiarPasswordTemporalResponse(
            success=True,
            mensaje="Contraseña actualizada exitosamente. Por favor, inicie sesión con su nueva contraseña.",
            requiere_login=True
        )
    
    def _enviar_credenciales_email(self, password_temporal_generada: bool, cliente, 
                                   login: str, password_temp: str, password_expira) -> bool:
        """
        Envía las credenciales de acceso por email al cliente
        
        Este método está separado para mantener el código del registro más limpio
        y enfocado en su responsabilidad principal.
        
        Args:
            password_temporal_generada: Si se generó una contraseña temporal
            cliente: Objeto del cliente con sus datos
            login: Usuario del sistema
            password_temp: Contraseña temporal generada
            password_expira: Fecha de expiración de la contraseña
            
        Returns:
            bool: True si el email se envió correctamente, False si falló
        """
        # Si no se generó password temporal, no enviar email
        if not password_temporal_generada:
            return False
        
        try:
            from services.email.email_service import EmailService
            
            # 1. Formatear la fecha de expiración
            fecha_expira_formateada = self._formatear_fecha_expiracion(password_expira)
            
            # 2. Enviar email con las credenciales
            email_service = EmailService()
            email_result = email_service.send_client_credentials_email_sync(
                destinatario_email=cliente.correo_electronico,
                destinatario_nombre=cliente.nombre_razon_social,
                login=login,
                password_temporal=password_temp,
                fecha_expiracion=fecha_expira_formateada
            )
            
            # 3. Retornar el resultado
            return email_result.success
            
        except Exception as e:
            # Si falla el envío, loguear pero NO fallar el registro
            print(f"Error al enviar email con credenciales: {e}")
            return False
    
    def _formatear_fecha_expiracion(self, password_expira) -> str:
        """
        Formatea la fecha de expiración en formato legible en español
        
        Args:
            password_expira: datetime o None
            
        Returns:
            str: Fecha formateada o 'No definida'
        """
        if not password_expira:
            return 'No definida'
        
        return password_expira.strftime('%d/%m/%Y a las %H:%M')
