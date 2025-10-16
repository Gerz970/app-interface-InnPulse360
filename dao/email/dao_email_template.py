"""
DAO (Data Access Object) para operaciones CRUD de EmailTemplate
Maneja todas las interacciones con la base de datos para plantillas de email
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_

from models.email.email_template_model import EmailTemplate
from schemas.email.email_schemas import EmailTemplateCreate, EmailTemplateUpdate


class EmailTemplateDAO:
    """
    Clase DAO para manejar operaciones CRUD de EmailTemplate en la base de datos
    """
    
    def __init__(self, db_session: Session):
        """
        Inicializa el DAO con una sesión de base de datos
        
        Args:
            db_session (Session): Sesión de SQLAlchemy
        """
        self.db = db_session
    
    def create(self, template_data: EmailTemplateCreate) -> EmailTemplate:
        """
        Crea una nueva plantilla de email
        
        Args:
            template_data (EmailTemplateCreate): Datos de la plantilla
            
        Returns:
            EmailTemplate: Plantilla creada
            
        Raises:
            SQLAlchemyError: Si hay error en la base de datos
        """
        try:
            # Si es plantilla por defecto, desactivar otras del mismo tipo
            if template_data.es_default:
                self._unset_default_for_type(template_data.tipo_template)
            
            db_template = EmailTemplate(
                nombre=template_data.nombre,
                descripcion=template_data.descripcion,
                tipo_template=template_data.tipo_template,
                asunto=template_data.asunto,
                contenido_html=template_data.contenido_html,
                contenido_texto=template_data.contenido_texto,
                variables_disponibles=template_data.variables_disponibles,
                idioma=template_data.idioma,
                es_default=template_data.es_default,
                activo=True,
                estatus_id=1
            )
            
            self.db.add(db_template)
            self.db.commit()
            self.db.refresh(db_template)
            
            return db_template
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def get_by_id(self, template_id: int) -> Optional[EmailTemplate]:
        """
        Obtiene una plantilla por ID
        
        Args:
            template_id (int): ID de la plantilla
            
        Returns:
            Optional[EmailTemplate]: Plantilla encontrada o None
        """
        return self.db.query(EmailTemplate).filter(
            and_(
                EmailTemplate.id_template == template_id,
                EmailTemplate.estatus_id == 1
            )
        ).first()
    
    def get_by_name(self, nombre: str) -> Optional[EmailTemplate]:
        """
        Obtiene una plantilla por nombre
        
        Args:
            nombre (str): Nombre de la plantilla
            
        Returns:
            Optional[EmailTemplate]: Plantilla encontrada o None
        """
        return self.db.query(EmailTemplate).filter(
            and_(
                EmailTemplate.nombre == nombre,
                EmailTemplate.estatus_id == 1
            )
        ).first()
    
    def get_by_type(self, tipo_template: str, idioma: str = "es") -> List[EmailTemplate]:
        """
        Obtiene plantillas por tipo e idioma
        
        Args:
            tipo_template (str): Tipo de plantilla
            idioma (str): Idioma de la plantilla
            
        Returns:
            List[EmailTemplate]: Lista de plantillas
        """
        return self.db.query(EmailTemplate).filter(
            and_(
                EmailTemplate.tipo_template == tipo_template,
                EmailTemplate.idioma == idioma,
                EmailTemplate.activo == True,
                EmailTemplate.estatus_id == 1
            )
        ).order_by(EmailTemplate.es_default.desc()).all()
    
    def get_default_by_type(self, tipo_template: str, idioma: str = "es") -> Optional[EmailTemplate]:
        """
        Obtiene la plantilla por defecto para un tipo e idioma
        
        Args:
            tipo_template (str): Tipo de plantilla
            idioma (str): Idioma de la plantilla
            
        Returns:
            Optional[EmailTemplate]: Plantilla por defecto o None
        """
        return self.db.query(EmailTemplate).filter(
            and_(
                EmailTemplate.tipo_template == tipo_template,
                EmailTemplate.idioma == idioma,
                EmailTemplate.es_default == True,
                EmailTemplate.activo == True,
                EmailTemplate.estatus_id == 1
            )
        ).first()
    
    def get_all_active(self, skip: int = 0, limit: int = 100) -> List[EmailTemplate]:
        """
        Obtiene todas las plantillas activas
        
        Args:
            skip (int): Registros a saltar
            limit (int): Límite de registros
            
        Returns:
            List[EmailTemplate]: Lista de plantillas
        """
        return self.db.query(EmailTemplate).filter(
            and_(
                EmailTemplate.activo == True,
                EmailTemplate.estatus_id == 1
            )
        ).offset(skip).limit(limit).all()
    
    def update(self, template_id: int, template_data: EmailTemplateUpdate) -> Optional[EmailTemplate]:
        """
        Actualiza una plantilla existente
        
        Args:
            template_id (int): ID de la plantilla
            template_data (EmailTemplateUpdate): Datos a actualizar
            
        Returns:
            Optional[EmailTemplate]: Plantilla actualizada o None
        """
        try:
            db_template = self.get_by_id(template_id)
            if not db_template:
                return None
            
            # Si se está marcando como default, desactivar otras del mismo tipo
            if template_data.es_default and not db_template.es_default:
                self._unset_default_for_type(db_template.tipo_template)
            
            # Actualizar campos proporcionados
            update_data = template_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_template, field, value)
            
            self.db.commit()
            self.db.refresh(db_template)
            
            return db_template
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def delete_logical(self, template_id: int) -> bool:
        """
        Eliminación lógica de una plantilla
        
        Args:
            template_id (int): ID de la plantilla
            
        Returns:
            bool: True si se eliminó correctamente
        """
        try:
            db_template = self.get_by_id(template_id)
            if not db_template:
                return False
            
            db_template.estatus_id = 0
            db_template.activo = False
            
            self.db.commit()
            return True
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def exists_by_name(self, nombre: str, exclude_id: Optional[int] = None) -> bool:
        """
        Verifica si existe una plantilla con el nombre dado
        
        Args:
            nombre (str): Nombre a verificar
            exclude_id (Optional[int]): ID a excluir de la búsqueda
            
        Returns:
            bool: True si existe
        """
        query = self.db.query(EmailTemplate).filter(
            and_(
                EmailTemplate.nombre == nombre,
                EmailTemplate.estatus_id == 1
            )
        )
        
        if exclude_id:
            query = query.filter(EmailTemplate.id_template != exclude_id)
        
        return query.first() is not None
    
    def _unset_default_for_type(self, tipo_template: str):
        """
        Desactiva el flag es_default para todas las plantillas del tipo dado
        
        Args:
            tipo_template (str): Tipo de plantilla
        """
        self.db.query(EmailTemplate).filter(
            and_(
                EmailTemplate.tipo_template == tipo_template,
                EmailTemplate.es_default == True,
                EmailTemplate.estatus_id == 1
            )
        ).update({"es_default": False})
    
    def get_types_count(self) -> dict:
        """
        Obtiene el conteo de plantillas por tipo
        
        Returns:
            dict: Diccionario con tipos y conteos
        """
        from sqlalchemy import func
        
        result = self.db.query(
            EmailTemplate.tipo_template,
            func.count(EmailTemplate.id_template).label('count')
        ).filter(
            and_(
                EmailTemplate.activo == True,
                EmailTemplate.estatus_id == 1
            )
        ).group_by(EmailTemplate.tipo_template).all()
        
        return {row.tipo_template: row.count for row in result}
