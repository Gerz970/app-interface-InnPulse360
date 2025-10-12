"""
Servicio para manejo de plantillas de email
Procesa plantillas HTML con variables dinámicas y genera contenido personalizado
"""

import os
import json
from typing import Dict, Any, Optional
from jinja2 import Template, Environment, FileSystemLoader
from datetime import datetime

from core.email_config import EmailTemplateConfig, EmailSettings


class EmailTemplateService:
    """
    Servicio para procesamiento de plantillas de email
    Maneja la carga, procesamiento y renderizado de plantillas HTML
    """
    
    def __init__(self):
        """
        Inicializa el servicio con la configuración de plantillas
        """
        self.template_dir = EmailSettings.template_dir
        self.default_language = EmailSettings.default_language
        
        # Configurar Jinja2
        self.jinja_env = Environment(
            loader=FileSystemLoader(self.template_dir),
            autoescape=True
        )
        
        # Variables globales disponibles en todas las plantillas
        self.global_variables = EmailTemplateConfig.get_template_variables()
    
    def render_template(self, template_name: str, variables: Dict[str, Any]) -> str:
        """
        Renderiza una plantilla con las variables proporcionadas
        
        Args:
            template_name (str): Nombre del archivo de plantilla
            variables (Dict[str, Any]): Variables para reemplazar
            
        Returns:
            str: HTML renderizado
            
        Raises:
            FileNotFoundError: Si la plantilla no existe
            Exception: Si hay error en el renderizado
        """
        try:
            # Cargar plantilla
            template = self.jinja_env.get_template(template_name)
            
            # Combinar variables globales con las específicas
            render_vars = {**self.global_variables, **variables}
            
            # Agregar variables del sistema
            render_vars.update({
                'current_year': datetime.now().year,
                'current_date': datetime.now().strftime('%d/%m/%Y'),
                'current_datetime': datetime.now().strftime('%d/%m/%Y %H:%M')
            })
            
            # Renderizar plantilla
            return template.render(**render_vars)
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Plantilla '{template_name}' no encontrada en {self.template_dir}")
        except Exception as e:
            raise Exception(f"Error al renderizar plantilla '{template_name}': {str(e)}")
    
    def render_base_template(self, variables: Dict[str, Any]) -> str:
        """
        Renderiza la plantilla base con contenido personalizado
        
        Args:
            variables (Dict[str, Any]): Variables para el contenido
            
        Returns:
            str: HTML renderizado de la plantilla base
        """
        return self.render_template('base_template.html', variables)
    
    def create_welcome_email(self, destinatario_nombre: str, usuario_email: str, 
                           codigo_activacion: Optional[str] = None) -> str:
        """
        Crea email de bienvenida usando la plantilla base
        
        Args:
            destinatario_nombre (str): Nombre del destinatario
            usuario_email (str): Email del usuario
            codigo_activacion (Optional[str]): Código de activación si aplica
            
        Returns:
            str: HTML del email de bienvenida
        """
        contenido_principal = f"""
        <p>¡Bienvenido a InnPulse 360! Tu cuenta ha sido creada exitosamente.</p>
        
        <p>Ya puedes acceder al sistema con las siguientes credenciales:</p>
        
        <div class="info-box">
            <h3>Información de tu cuenta</h3>
            <p><strong>Email:</strong> <span class="highlight">{usuario_email}</span></p>
            <p><strong>Estado:</strong> Cuenta activa</p>
            {f'<p><strong>Código de activación:</strong> <span class="code">{codigo_activacion}</span></p>' if codigo_activacion else ''}
        </div>
        
        <p>Para comenzar a usar el sistema, inicia sesión con tus credenciales.</p>
        """
        
        variables = {
            'destinatario_nombre': destinatario_nombre,
            'contenido_principal': contenido_principal,
            'boton_url': 'https://innpulse360.com/login',
            'boton_texto': 'Iniciar Sesión',
            'boton_estilo': 'button-secondary',
            'contenido_secundario': '''
            <p>Si tienes alguna pregunta o necesitas ayuda, no dudes en contactar a nuestro equipo de soporte.</p>
            '''
        }
        
        return self.render_base_template(variables)
    
    def create_password_reset_email(self, destinatario_nombre: str, reset_token: str) -> str:
        """
        Crea email de restablecimiento de contraseña
        
        Args:
            destinatario_nombre (str): Nombre del destinatario
            reset_token (str): Token para restablecer contraseña
            
        Returns:
            str: HTML del email de restablecimiento
        """
        contenido_principal = f"""
        <p>Recibimos una solicitud para restablecer la contraseña de tu cuenta.</p>
        
        <p>Si realizaste esta solicitud, haz clic en el botón de abajo para crear una nueva contraseña:</p>
        
        <div class="info-box">
            <h3>Información importante</h3>
            <p>Este enlace expirará en 24 horas por seguridad.</p>
            <p>Si no solicitaste este cambio, puedes ignorar este correo.</p>
        </div>
        """
        
        variables = {
            'destinatario_nombre': destinatario_nombre,
            'contenido_principal': contenido_principal,
            'boton_url': f'https://innpulse360.com/reset-password?token={reset_token}',
            'boton_texto': 'Restablecer Contraseña',
            'contenido_secundario': '''
            <p><strong>Por seguridad:</strong></p>
            <ul style="margin-left: 20px; color: #6B7280;">
                <li>Nunca compartas este enlace con nadie</li>
                <li>El enlace expira automáticamente</li>
                <li>Si no solicitaste este cambio, contacta soporte</li>
            </ul>
            '''
        }
        
        return self.render_base_template(variables)
    
    def create_role_assignment_email(self, destinatario_nombre: str, rol_asignado: str, 
                                   asignado_por: str) -> str:
        """
        Crea email de asignación de rol
        
        Args:
            destinatario_nombre (str): Nombre del destinatario
            rol_asignado (str): Rol que se asignó
            asignado_por (str): Quién asignó el rol
            
        Returns:
            str: HTML del email de asignación
        """
        contenido_principal = f"""
        <p>Se ha asignado un nuevo rol a tu cuenta en InnPulse 360.</p>
        
        <div class="info-box">
            <h3>Detalles de la asignación</h3>
            <p><strong>Rol asignado:</strong> <span class="highlight">{rol_asignado}</span></p>
            <p><strong>Asignado por:</strong> {asignado_por}</p>
            <p><strong>Fecha:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
        </div>
        
        <p>Los cambios en permisos serán efectivos inmediatamente. Inicia sesión para ver las nuevas funcionalidades disponibles.</p>
        """
        
        variables = {
            'destinatario_nombre': destinatario_nombre,
            'contenido_principal': contenido_principal,
            'boton_url': 'https://innpulse360.com/login',
            'boton_texto': 'Acceder al Sistema',
            'boton_estilo': 'button-secondary',
            'contenido_secundario': '''
            <p>Si tienes alguna pregunta sobre los nuevos permisos o necesitas capacitación adicional, contacta a tu administrador o al equipo de soporte.</p>
            '''
        }
        
        return self.render_base_template(variables)
    
    def create_hotel_notification_email(self, destinatario_nombre: str, hotel_nombre: str, 
                                      tipo_notificacion: str, mensaje: str) -> str:
        """
        Crea email de notificación de hotel
        
        Args:
            destinatario_nombre (str): Nombre del destinatario
            hotel_nombre (str): Nombre del hotel
            tipo_notificacion (str): Tipo de notificación
            mensaje (str): Mensaje específico
            
        Returns:
            str: HTML del email de notificación
        """
        contenido_principal = f"""
        <p>Has recibido una notificación relacionada con el hotel <span class="highlight">{hotel_nombre}</span>.</p>
        
        <div class="info-box">
            <h3>Detalles de la notificación</h3>
            <p><strong>Tipo:</strong> {tipo_notificacion}</p>
            <p><strong>Hotel:</strong> {hotel_nombre}</p>
            <p><strong>Fecha:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
        </div>
        
        <p>{mensaje}</p>
        """
        
        variables = {
            'destinatario_nombre': destinatario_nombre,
            'contenido_principal': contenido_principal,
            'boton_url': 'https://innpulse360.com/hotels',
            'boton_texto': 'Ver Hoteles',
            'boton_estilo': 'button-secondary',
            'contenido_secundario': '''
            <p>Accede al sistema para ver más detalles y tomar las acciones necesarias.</p>
            '''
        }
        
        return self.render_base_template(variables)
    
    def create_booking_confirmation_email(self, destinatario_nombre: str, hotel_nombre: str,
                                        fecha_llegada: str, fecha_salida: str,
                                        numero_reserva: str) -> str:
        """
        Crea email de confirmación de reserva
        
        Args:
            destinatario_nombre (str): Nombre del destinatario
            hotel_nombre (str): Nombre del hotel
            fecha_llegada (str): Fecha de llegada
            fecha_salida (str): Fecha de salida
            numero_reserva (str): Número de reserva
            
        Returns:
            str: HTML del email de confirmación
        """
        contenido_principal = f"""
        <p>Tu reserva ha sido confirmada exitosamente.</p>
        
        <div class="info-box">
            <h3>Detalles de la reserva</h3>
            <p><strong>Número de reserva:</strong> <span class="code">{numero_reserva}</span></p>
            <p><strong>Hotel:</strong> {hotel_nombre}</p>
            <p><strong>Fecha de llegada:</strong> {fecha_llegada}</p>
            <p><strong>Fecha de salida:</strong> {fecha_salida}</p>
        </div>
        
        <p>Presenta este número de reserva al llegar al hotel. ¡Esperamos brindarte una excelente experiencia!</p>
        """
        
        variables = {
            'destinatario_nombre': destinatario_nombre,
            'contenido_principal': contenido_principal,
            'boton_url': 'https://innpulse360.com/my-bookings',
            'boton_texto': 'Ver Mis Reservas',
            'boton_estilo': 'button-secondary',
            'contenido_secundario': '''
            <p>Si necesitas hacer cambios en tu reserva o tienes alguna pregunta, contacta al hotel directamente o utiliza nuestro sistema de soporte.</p>
            '''
        }
        
        return self.render_base_template(variables)
    
    def create_custom_email(self, destinatario_nombre: Optional[str], asunto: str,
                          contenido_html: str, boton_url: Optional[str] = None,
                          boton_texto: Optional[str] = None) -> str:
        """
        Crea email personalizado usando la plantilla base
        
        Args:
            destinatario_nombre (Optional[str]): Nombre del destinatario
            asunto (str): Asunto del email
            contenido_html (str): Contenido HTML personalizado
            boton_url (Optional[str]): URL del botón si aplica
            boton_texto (Optional[str]): Texto del botón si aplica
            
        Returns:
            str: HTML del email personalizado
        """
        variables = {
            'destinatario_nombre': destinatario_nombre,
            'contenido_principal': contenido_html,
            'boton_url': boton_url,
            'boton_texto': boton_texto
        }
        
        return self.render_base_template(variables)
    
    def validate_template(self, template_name: str) -> bool:
        """
        Valida que una plantilla existe y es válida
        
        Args:
            template_name (str): Nombre de la plantilla
            
        Returns:
            bool: True si la plantilla es válida
        """
        try:
            template_path = os.path.join(self.template_dir, template_name)
            if not os.path.exists(template_path):
                return False
            
            # Intentar cargar la plantilla
            self.jinja_env.get_template(template_name)
            return True
            
        except Exception:
            return False
    
    def get_available_templates(self) -> list:
        """
        Obtiene lista de plantillas disponibles
        
        Returns:
            list: Lista de nombres de plantillas
        """
        try:
            templates = []
            if os.path.exists(self.template_dir):
                for file in os.listdir(self.template_dir):
                    if file.endswith('.html'):
                        templates.append(file)
            return templates
        except Exception:
            return []
