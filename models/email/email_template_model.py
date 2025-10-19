"""
Modelo SQLAlchemy para plantillas de email
Permite almacenar y gestionar plantillas de correo personalizables
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, SmallInteger
from sqlalchemy.sql import func
from core.base import Base


class EmailTemplate(Base):
    """
    Modelo para plantillas de email
    Almacena plantillas HTML personalizables para diferentes tipos de correo
    """
    __tablename__ = "Tb_email_template"
    __table_args__ = {'schema': 'EMAIL'}
    
    # Campos principales
    id_template = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nombre = Column(String(100), nullable=False, unique=True, index=True)
    descripcion = Column(String(255), nullable=True)
    tipo_template = Column(String(50), nullable=False, index=True)  # welcome_user, password_reset, etc.
    
    # Contenido de la plantilla
    asunto = Column(String(255), nullable=False)
    contenido_html = Column(Text, nullable=False)
    contenido_texto = Column(Text, nullable=True)  # Versión texto plano
    
    # Variables disponibles (JSON string)
    variables_disponibles = Column(Text, nullable=True)  # JSON con variables como {nombre}, {email}, etc.
    
    # Configuración
    idioma = Column(String(5), nullable=False, default='es')  # es, en, fr, etc.
    activo = Column(Boolean, nullable=False, default=True)
    es_default = Column(Boolean, nullable=False, default=False)  # Plantilla por defecto para el tipo
    
    # Metadatos
    creado_por = Column(Integer, nullable=True)  # ID del usuario que creó
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now())
    estatus_id = Column(SmallInteger, nullable=False, default=1)  # 1=Activo, 0=Inactivo
    
    def __repr__(self):
        return f"<EmailTemplate(id={self.id_template}, nombre='{self.nombre}', tipo='{self.tipo_template}')>"
    
    def to_dict(self):
        """
        Convierte el modelo a diccionario para fácil serialización
        """
        return {
            'id_template': self.id_template,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'tipo_template': self.tipo_template,
            'asunto': self.asunto,
            'contenido_html': self.contenido_html,
            'contenido_texto': self.contenido_texto,
            'variables_disponibles': self.variables_disponibles,
            'idioma': self.idioma,
            'activo': self.activo,
            'es_default': self.es_default,
            'creado_por': self.creado_por,
            'fecha_creacion': self.fecha_creacion,
            'fecha_actualizacion': self.fecha_actualizacion,
            'estatus_id': self.estatus_id
        }
