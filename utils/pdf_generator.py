"""
Utilidad para generar PDFs de cotización usando reportlab
"""

import logging
from typing import Optional
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from io import BytesIO

logger = logging.getLogger(__name__)


def generate_quotation_pdf(
    codigo_reservacion: str,
    fecha_entrada: str,
    fecha_salida: str,
    duracion_dias: int,
    hotel_nombre: str,
    hotel_direccion: Optional[str],
    hotel_telefono: Optional[str],
    hotel_email: Optional[str],
    habitacion_nombre: str,
    habitacion_descripcion: Optional[str],
    tipo_habitacion: str,
    cliente_nombre: str,
    cliente_rfc: Optional[str],
    cliente_identificacion: Optional[str],
    cliente_email: Optional[str],
    precio_unitario: float,
    periodicidad_nombre: str,
    precio_total: float,
    output_path: Optional[str] = None
) -> BytesIO:
    """
    Genera un PDF de cotización usando reportlab
    
    Args:
        codigo_reservacion: Código de la reservación
        fecha_entrada: Fecha de entrada formateada
        fecha_salida: Fecha de salida formateada
        duracion_dias: Duración en días
        hotel_nombre: Nombre del hotel
        hotel_direccion: Dirección del hotel
        hotel_telefono: Teléfono del hotel
        hotel_email: Email del hotel
        habitacion_nombre: Nombre/clave de la habitación
        habitacion_descripcion: Descripción de la habitación
        tipo_habitacion: Tipo de habitación
        cliente_nombre: Nombre completo del cliente
        cliente_rfc: RFC del cliente
        cliente_identificacion: Documento de identificación
        cliente_email: Email del cliente
        precio_unitario: Precio unitario
        periodicidad_nombre: Nombre de la periodicidad
        precio_total: Precio total calculado
        output_path: Ruta opcional para guardar el archivo
    
    Returns:
        BytesIO: Contenido del PDF en memoria
    """
    try:
        # Crear buffer para el PDF
        pdf_bytes = BytesIO()
        
        # Crear documento PDF
        doc = SimpleDocTemplate(
            pdf_bytes,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        # Contenedor para elementos del PDF
        elements = []
        
        # Estilos
        styles = getSampleStyleSheet()
        
        # Estilo para el título principal
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#6B46C1'),
            spaceAfter=10,
            alignment=TA_LEFT
        )
        
        # Estilo para subtítulo
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Normal'],
            fontSize=14,
            textColor=colors.HexColor('#666666'),
            spaceAfter=30
        )
        
        # Estilo para secciones
        section_style = ParagraphStyle(
            'SectionTitle',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#6B46C1'),
            backColor=colors.HexColor('#F3F4F6'),
            spaceAfter=12,
            spaceBefore=12,
            leftIndent=10,
            borderWidth=0,
            borderColor=colors.HexColor('#6B46C1'),
            borderPadding=5
        )
        
        # Estilo para texto normal
        normal_style = styles['Normal']
        normal_style.fontSize = 12
        
        # Header
        elements.append(Paragraph("InnPulse 360", title_style))
        elements.append(Paragraph("Cotización de Reservación", subtitle_style))
        elements.append(Spacer(1, 0.5*cm))
        
        # Línea divisoria
        elements.append(Table(
            [[None]],
            colWidths=[doc.width],
            style=[('LINEBELOW', (0, 0), (-1, -1), 3, colors.HexColor('#6B46C1'))]
        ))
        elements.append(Spacer(1, 1*cm))
        
        # Información de la Reservación
        elements.append(Paragraph("Información de la Reservación", section_style))
        reservacion_data = [
            ['Código de Reservación:', codigo_reservacion],
            ['Fecha de Entrada:', fecha_entrada],
            ['Fecha de Salida:', fecha_salida],
            ['Duración:', f"{duracion_dias} {'día' if duracion_dias == 1 else 'días'}"]
        ]
        reservacion_table = Table(reservacion_data, colWidths=[6*cm, 10*cm])
        reservacion_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#666666')),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.black),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E5E7EB')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(reservacion_table)
        elements.append(Spacer(1, 0.8*cm))
        
        # Información del Hotel
        elements.append(Paragraph("Información del Hotel", section_style))
        hotel_data = [['Nombre:', hotel_nombre]]
        if hotel_direccion:
            hotel_data.append(['Dirección:', hotel_direccion])
        if hotel_telefono:
            hotel_data.append(['Teléfono:', hotel_telefono])
        if hotel_email:
            hotel_data.append(['Email:', hotel_email])
        
        hotel_table = Table(hotel_data, colWidths=[6*cm, 10*cm])
        hotel_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#666666')),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.black),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E5E7EB')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(hotel_table)
        elements.append(Spacer(1, 0.8*cm))
        
        # Información de la Habitación
        elements.append(Paragraph("Información de la Habitación", section_style))
        habitacion_data = [['Habitación:', habitacion_nombre]]
        if habitacion_descripcion:
            habitacion_data.append(['Descripción:', habitacion_descripcion])
        habitacion_data.append(['Tipo de Habitación:', tipo_habitacion])
        
        habitacion_table = Table(habitacion_data, colWidths=[6*cm, 10*cm])
        habitacion_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#666666')),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.black),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E5E7EB')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(habitacion_table)
        elements.append(Spacer(1, 0.8*cm))
        
        # Información del Cliente
        elements.append(Paragraph("Información del Cliente", section_style))
        cliente_data = [['Nombre Completo:', cliente_nombre]]
        if cliente_rfc:
            cliente_data.append(['RFC:', cliente_rfc])
        if cliente_identificacion:
            cliente_data.append(['Identificación:', cliente_identificacion])
        if cliente_email:
            cliente_data.append(['Email:', cliente_email])
        
        cliente_table = Table(cliente_data, colWidths=[6*cm, 10*cm])
        cliente_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#666666')),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.black),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E5E7EB')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(cliente_table)
        elements.append(Spacer(1, 0.8*cm))
        
        # Detalles de Precio
        elements.append(Paragraph("Detalles de Precio", section_style))
        precio_data = [
            ['Precio Unitario:', f"${precio_unitario:,.2f}"],
            ['Periodicidad:', periodicidad_nombre],
            ['Duración:', f"{duracion_dias} {'día' if duracion_dias == 1 else 'días'}"]
        ]
        
        precio_table = Table(precio_data, colWidths=[6*cm, 10*cm])
        precio_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#666666')),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.black),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E5E7EB')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(precio_table)
        elements.append(Spacer(1, 1*cm))
        
        # Total destacado - "Total a Pagar" a la izquierda, monto a la derecha
        total_table = Table(
            [
                ['Total a Pagar:', f"${precio_total:,.2f}"]
            ],
            colWidths=[10*cm, 6*cm]
        )
        total_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F9FAFB')),
            ('TEXTCOLOR', (0, 0), (0, 0), colors.HexColor('#666666')),
            ('TEXTCOLOR', (1, 0), (1, 0), colors.HexColor('#6B46C1')),
            ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (0, 0), 16),
            ('FONTSIZE', (1, 0), (1, 0), 28),
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),  # "Total a Pagar" alineado a la izquierda
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),  # Monto alineado a la derecha
            ('BORDER', (0, 0), (-1, -1), 2, colors.HexColor('#6B46C1')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (0, 0), 20),  # Padding izquierdo para "Total a Pagar"
            ('RIGHTPADDING', (0, 0), (0, 0), 10),
            ('LEFTPADDING', (1, 0), (1, 0), 10),
            ('RIGHTPADDING', (1, 0), (1, 0), 20),  # Padding derecho para el monto
            ('TOPPADDING', (0, 0), (-1, -1), 20),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 20),
        ]))
        elements.append(total_table)
        elements.append(Spacer(1, 2*cm))
        
        # Footer
        footer_style = ParagraphStyle(
            'FooterStyle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#999999'),
            alignment=TA_CENTER
        )
        
        elements.append(Table(
            [[None]],
            colWidths=[doc.width],
            style=[('LINEABOVE', (0, 0), (-1, -1), 1, colors.HexColor('#E5E7EB'))]
        ))
        elements.append(Spacer(1, 0.5*cm))
        elements.append(Paragraph(
            "Este documento es una cotización generada automáticamente por InnPulse 360",
            footer_style
        ))
        elements.append(Paragraph(
            f"Para consultas, contacte a: {hotel_email if hotel_email else 'support@innpulse360.com'}",
            footer_style
        ))
        
        # Construir PDF
        doc.build(elements)
        
        pdf_bytes.seek(0)
        
        # Si se proporciona output_path, guardar también en archivo
        if output_path:
            with open(output_path, 'wb') as f:
                f.write(pdf_bytes.getvalue())
            logger.info(f"PDF generado y guardado en: {output_path}")
            pdf_bytes.seek(0)  # Resetear posición para lectura
        
        return pdf_bytes
            
    except Exception as e:
        logger.error(f"Error al generar PDF: {str(e)}")
        raise



