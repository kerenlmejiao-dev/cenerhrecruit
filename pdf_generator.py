"""
PDF Generator - Generar fichas de candidatos con ReportLab
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from datetime import datetime
from sqlalchemy.orm import Session
from models import Candidato, ScoreCandidata, TestPsicometrico
import io


class GeneradorPDF:
    """Generador de fichas PDF de candidatos"""
    
    # Colores CENERH
    AZUL_INSTITUCIONAL = HexColor("#0050A0")
    ROJO = HexColor("#D62828")
    GRIS_OSCURO = HexColor("#0D0D0D")
    ORO = HexColor("#C9A14A")
    GRIS_PLATA = HexColor("#B8BFC7")
    
    # Ancho de página
    PAGE_WIDTH = letter[0]  # 8.5 inches
    PAGE_HEIGHT = letter[1]  # 11 inches
    
    @staticmethod
    def generar_ficha_candidato(db: Session, candidato_id: str) -> bytes:
        """
        Generar PDF con ficha completa del candidato
        
        Retorna: bytes del PDF
        """
        
        # Obtener datos
        candidato = db.query(Candidato).filter_by(id=candidato_id).first()
        if not candidato:
            raise ValueError(f"Candidato '{candidato_id}' no encontrado")
        
        scores = db.query(ScoreCandidata).filter_by(candidato_id=candidato_id).all()
        
        # Crear buffer en memoria
        buffer = io.BytesIO()
        
        # Crear PDF
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=0.4*inch,
            leftMargin=0.4*inch,
            topMargin=0.35*inch,
            bottomMargin=0.35*inch,
        )
        
        # Estilos
        styles = getSampleStyleSheet()
        
        titulo_style = ParagraphStyle(
            'Titulo',
            parent=styles['Heading1'],
            fontSize=20,
            textColor=GeneradorPDF.AZUL_INSTITUCIONAL,
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
        )
        
        subtitulo_style = ParagraphStyle(
            'Subtitulo',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=GeneradorPDF.ROJO,
            spaceAfter=10,
            alignment=TA_LEFT,
            fontName='Helvetica-Bold',
        )
        
        normal_style = ParagraphStyle(
            'Normal',
            parent=styles['Normal'],
            fontSize=10,
            textColor=GeneradorPDF.GRIS_OSCURO,
            alignment=TA_LEFT,
            fontName='Helvetica',
        )
        
        # Contenido del PDF
        elements = []
        
        # HEADER CON LOGO (simulado)
        header_data = [
            [
                Paragraph("<b>CENERH</b>", ParagraphStyle(
                    'Header',
                    parent=styles['Normal'],
                    fontSize=18,
                    textColor=GeneradorPDF.AZUL_INSTITUCIONAL,
                    fontName='Helvetica-Bold',
                )),
                Paragraph("CONSULTING", ParagraphStyle(
                    'Header2',
                    parent=styles['Normal'],
                    fontSize=10,
                    textColor=GeneradorPDF.ORO,
                    fontName='Helvetica',
                    alignment=TA_RIGHT,
                )),
            ]
        ]
        
        header_table = Table(header_data, colWidths=[3.5*inch, 3.5*inch])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        
        elements.append(header_table)
        elements.append(Spacer(1, 0.15*inch))
        
        # TÍTULO
        elements.append(Paragraph("FICHA TÉCNICA DE EVALUACIÓN", titulo_style))
        elements.append(Spacer(1, 0.1*inch))
        
        # INFORMACIÓN GENERAL
        elements.append(Paragraph("INFORMACIÓN DEL CANDIDATO", subtitulo_style))
        
        info_candidato = [
            [Paragraph("<b>Nombre:</b>", normal_style), Paragraph(candidato.nombre, normal_style)],
            [Paragraph("<b>Email:</b>", normal_style), Paragraph(candidato.email, normal_style)],
            [Paragraph("<b>Vacante:</b>", normal_style), Paragraph(candidato.vacante_id, normal_style)],
            [Paragraph("<b>Fecha de Evaluación:</b>", normal_style), Paragraph(datetime.now().strftime("%d/%m/%Y"), normal_style)],
        ]
        
        info_table = Table(info_candidato, colWidths=[1.5*inch, 5*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), HexColor("#F5F5F5")),
            ('GRID', (0, 0), (-1, -1), 0.5, GeneradorPDF.GRIS_PLATA),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elements.append(info_table)
        elements.append(Spacer(1, 0.2*inch))
        
        # SCORES POR TEST
        elements.append(Paragraph("RESULTADOS POR TEST", subtitulo_style))
        
        if scores:
            scores_data = [
                [
                    Paragraph("<b>Test</b>", normal_style),
                    Paragraph("<b>Score</b>", normal_style),
                    Paragraph("<b>Percentil</b>", normal_style),
                    Paragraph("<b>Clasificación</b>", normal_style),
                ]
            ]
            
            for score in scores:
                test = db.query(TestPsicometrico).filter_by(id=score.test_id).first()
                test_nombre = test.nombre if test else score.test_id
                
                clasificacion = score.clasificacion_test
                color_clasificacion = {
                    "PRIORITARIO": GeneradorPDF.ROJO,
                    "VIABLE": GeneradorPDF.AZUL_INSTITUCIONAL,
                    "CONSIDERAR": GeneradorPDF.ORO,
                    "NO RECOMENDADO": HexColor("#CC0000"),
                }.get(clasificacion, GeneradorPDF.GRIS_OSCURO)
                
                scores_data.append([
                    Paragraph(test_nombre, normal_style),
                    Paragraph(f"{score.score_normalizado:.1f}", normal_style),
                    Paragraph(f"{score.percentil:.0f}%", normal_style),
                    Paragraph(
                        f"<font color='{color_clasificacion.hexval()}'><b>{clasificacion}</b></font>",
                        normal_style
                    ),
                ])
            
            scores_table = Table(scores_data, colWidths=[2.5*inch, 1.2*inch, 1.2*inch, 1.6*inch])
            scores_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), GeneradorPDF.AZUL_INSTITUCIONAL),
                ('TEXTCOLOR', (0, 0), (-1, 0), white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 0.5, GeneradorPDF.GRIS_PLATA),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor("#F9F9F9")]),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            
            elements.append(scores_table)
        else:
            elements.append(Paragraph("Sin evaluaciones completadas aún.", normal_style))
        
        elements.append(Spacer(1, 0.2*inch))
        
        # SCORE FINAL
        if scores:
            # Calcular score final ponderado
            categorias = {
                "competencias": [],
                "psicometricos": [],
                "cognitivos": [],
            }
            
            categoria_map = {
                "verbal": "cognitivos",
                "numerico": "cognitivos",
                "big_five": "psicometricos",
                "ie": "psicometricos",
                "motivacion": "psicometricos",
                "valores": "psicometricos",
                "liderazgo": "psicometricos",
                "competencias": "competencias",
                "atencion": "cognitivos",
            }
            
            for score in scores:
                cat = categoria_map.get(score.test_id, "otros")
                if cat in categorias:
                    categorias[cat].append(score.score_normalizado)
            
            pesos = {"competencias": 0.35, "psicometricos": 0.35, "cognitivos": 0.30}
            
            score_final = (
                (sum(categorias.get("competencias", [0])) / len(categorias["competencias"]) if categorias["competencias"] else 0) * pesos["competencias"] +
                (sum(categorias.get("psicometricos", [0])) / len(categorias["psicometricos"]) if categorias["psicometricos"] else 0) * pesos["psicometricos"] +
                (sum(categorias.get("cognitivos", [0])) / len(categorias["cognitivos"]) if categorias["cognitivos"] else 0) * pesos["cognitivos"]
            )
            
            score_final = round(score_final, 1)
            
            # Clasificación final
            if score_final >= 81:
                clasificacion_final = "PRIORITARIO"
                color_final = GeneradorPDF.ROJO
            elif score_final >= 61:
                clasificacion_final = "VIABLE"
                color_final = GeneradorPDF.AZUL_INSTITUCIONAL
            elif score_final >= 41:
                clasificacion_final = "CONSIDERAR"
                color_final = GeneradorPDF.ORO
            else:
                clasificacion_final = "NO RECOMENDADO"
                color_final = HexColor("#CC0000")
            
            score_final_data = [
                [
                    Paragraph("<b>SCORE FINAL</b>", subtitulo_style),
                    Paragraph(f"<font size='16'><b>{score_final}/100</b></font>", normal_style),
                    Paragraph(f"<font color='{color_final.hexval()}'><b>{clasificacion_final}</b></font>", normal_style),
                ]
            ]
            
            score_final_table = Table(score_final_data, colWidths=[2*inch, 2*inch, 2.5*inch])
            score_final_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), HexColor("#F0F0F0")),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('GRID', (0, 0), (-1, -1), 1, GeneradorPDF.AZUL_INSTITUCIONAL),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 12),
                ('TOPPADDING', (0, 0), (-1, -1), 12),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ]))
            
            elements.append(score_final_table)
        
        elements.append(Spacer(1, 0.3*inch))
        
        # FOOTER
        footer = Paragraph(
            f"<i>CENERH Consulting - Evaluación Estratégica de RRHH<br/>Documento confidencial - {datetime.now().strftime('%d de %B de %Y')}</i>",
            ParagraphStyle(
                'Footer',
                parent=styles['Normal'],
                fontSize=8,
                textColor=GeneradorPDF.GRIS_PLATA,
                alignment=TA_CENTER,
            )
        )
        elements.append(footer)
        
        # Build PDF
        doc.build(elements)
        
        # Retornar bytes
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes


# Test rápido
if __name__ == "__main__":
    print("✅ PDF Generator listo para usar")
    print("   Usar: GeneradorPDF.generar_ficha_candidato(db, candidato_id)")
