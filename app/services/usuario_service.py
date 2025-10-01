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

from dao.dao_usuario import UsuarioDAO
from models.seguridad.usuario_model import Usuario
from schemas.seguridad.usuario_create import UsuarioCreate
from schemas.seguridad.usuario_update import UsuarioUpdate
from schemas.seguridad.usuario_response import UsuarioResponse
from schemas.seguridad.auth_schemas import UsuarioLogin, Token, TokenData
from core.config import AuthSettings

# Configuración para encriptación de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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
    
    def _hash_password(self, password: str) -> str:
        """
        Encripta una contraseña usando bcrypt
        
        Args:
            password (str): Contraseña en texto plano
            
        Returns:
            str: Contraseña encriptada
        """
        return pwd_context.hash(password)
    
    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verifica si una contraseña coincide con su hash
        
        Args:
            plain_password (str): Contraseña en texto plano
            hashed_password (str): Contraseña encriptada
            
        Returns:
            bool: True si coinciden, False si no
        """
        return pwd_context.verify(plain_password, hashed_password)
    
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
        
        # Encriptar la contraseña
        hashed_password = self._hash_password(usuario_data.password)
        
        # Crear el usuario con contraseña encriptada
        usuario_data.password = hashed_password
        db_usuario = self.dao.create(usuario_data)
        
        # Retornar sin la contraseña
        return UsuarioResponse(
            id_usuario=db_usuario.id_usuario,
            login=db_usuario.login,
            correo_electronico=db_usuario.correo_electronico,
            estatus_id=db_usuario.estatus_id
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
        
        return UsuarioResponse(
            id_usuario=db_usuario.id_usuario,
            login=db_usuario.login,
            correo_electronico=db_usuario.correo_electronico,
            estatus_id=db_usuario.estatus_id
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
        
        return UsuarioResponse(
            id_usuario=db_usuario.id_usuario,
            login=db_usuario.login,
            correo_electronico=db_usuario.correo_electronico,
            estatus_id=db_usuario.estatus_id
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
                estatus_id=usuario.estatus_id
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
        
        return UsuarioResponse(
            id_usuario=db_usuario.id_usuario,
            login=db_usuario.login,
            correo_electronico=db_usuario.correo_electronico,
            estatus_id=db_usuario.estatus_id
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
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=AuthSettings.access_token_expire_minutes * 60,  # En segundos
            user_info={
                "id_usuario": usuario.id_usuario,
                "login": usuario.login,
                "correo_electronico": usuario.correo_electronico
            }
        )
    
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
        
        return UsuarioResponse(
            id_usuario=usuario.id_usuario,
            login=usuario.login,
            correo_electronico=usuario.correo_electronico,
            estatus_id=usuario.estatus_id
        )
