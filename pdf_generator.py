"""
PDF Generator - Generar fichas de candidatos con ReportLab
"""
import sys
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from datetime import datetime
from sqlalchemy.orm import Session
from models import AssessmentCenter, AssessmentScore, Candidato, CandidatoPerfil, CompatibilidadCandidato, ScoreCandidata, TestPsicometrico
from scoring import SistemaScoring, scoring_final
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
        assessment_scores = db.query(AssessmentScore).filter_by(candidato_id=candidato_id).all()
        compatibilidad = db.query(CompatibilidadCandidato).filter_by(candidato_id=candidato_id).first()

        # Score final: se calcula una sola vez aquí y se reutiliza tanto en el
        # resumen ejecutivo (arriba) como en la sección detallada (abajo).
        score_final = None
        clasificacion_final = None
        if scores:
            score_tests, _ = scoring_final(db, candidato_id, candidato.vacante_id)
            if assessment_scores:
                promedio_assessments = sum(a.score_normalizado for a in assessment_scores) / len(assessment_scores)
                score_final = round(score_tests * 0.8 + promedio_assessments * 0.2, 1)
            else:
                score_final = score_tests
            clasificacion_final = SistemaScoring._clasificar_score(score_final)

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

        # RESUMEN EJECUTIVO: para que la empresa lo lea en segundos, sin tener
        # que buscar el score entre el resto de la ficha.
        if score_final is not None:
            color_resumen = {
                "PRIORITARIO": GeneradorPDF.ROJO,
                "VIABLE": GeneradorPDF.AZUL_INSTITUCIONAL,
                "CONSIDERAR": GeneradorPDF.ORO,
                "NO_RECOMENDADO": HexColor("#CC0000"),
            }.get(clasificacion_final, GeneradorPDF.GRIS_OSCURO)

            resumen_lineas = [
                f"<font size='22' color='{color_resumen.hexval()}'><b>{score_final}/100</b></font> "
                f"&nbsp;&nbsp;<font color='{color_resumen.hexval()}'><b>{clasificacion_final}</b></font>"
            ]
            if compatibilidad:
                resumen_lineas.append(
                    f"<b>Compatibilidad con la vacante:</b> {round(compatibilidad.score_compatibilidad)}/100"
                )
                if compatibilidad.resumen:
                    resumen_lineas.append(compatibilidad.resumen)

            resumen_data = [[Paragraph("<br/>".join(resumen_lineas), normal_style)]]
            resumen_table = Table(resumen_data, colWidths=[7*inch])
            resumen_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), HexColor("#F0F4F9")),
                ('BOX', (0, 0), (-1, -1), 1, GeneradorPDF.AZUL_INSTITUCIONAL),
                ('LEFTPADDING', (0, 0), (-1, -1), 14),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ]))
            elements.append(Paragraph("RESUMEN EJECUTIVO", subtitulo_style))
            elements.append(resumen_table)
            elements.append(Spacer(1, 0.2*inch))

        # INFORMACIÓN GENERAL
        elements.append(Paragraph("INFORMACIÓN DEL CANDIDATO", subtitulo_style))
        
        info_candidato = [
            [Paragraph("<b>Nombre:</b>", normal_style), Paragraph(candidato.nombre, normal_style)],
            [Paragraph("<b>Email:</b>", normal_style), Paragraph(candidato.email, normal_style)],
            [Paragraph("<b>Vacante:</b>", normal_style), Paragraph(candidato.vacante_id or "Bolsa de talento (sin vacante)", normal_style)],
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

        # PERFIL DEL CANDIDATO (datos personales, domicilio, formación, experiencia)
        perfil = db.query(CandidatoPerfil).filter_by(candidato_id=candidato_id).first()
        if perfil:
            filas_perfil = [
                ("Cédula", perfil.cedula),
                ("Edad", perfil.edad),
                ("Estado civil", perfil.estado_civil),
                ("Hijos", f"{perfil.cantidad_hijos} (edades: {perfil.edades_hijos})" if perfil.cantidad_hijos else None),
                ("Ciudad/Provincia", perfil.ciudad_provincia or perfil.ubicacion),
                ("Dirección exacta", perfil.direccion_exacta),
                ("Contacto de emergencia", f"{perfil.contacto_emergencia_nombre} - {perfil.contacto_emergencia_telefono}" if perfil.contacto_emergencia_nombre or perfil.contacto_emergencia_telefono else None),
                ("Nivel académico", perfil.nivel_academico),
                ("Carrera", perfil.carrera),
                ("Universidad", perfil.universidad),
                ("Años de experiencia", perfil.anos_experiencia),
                ("Último cargo", perfil.ultimo_cargo),
                ("Último salario", perfil.ultimo_salario),
                ("Funciones último empleo", perfil.funciones_ultimo_empleo),
                ("Expectativa salarial", perfil.pretension_salarial),
                ("Disponibilidad", perfil.disponibilidad),
                ("Cómo se enteró de la vacante", perfil.fuente_reclutamiento),
                ("Otras posiciones de interés", perfil.posiciones_interes),
            ]
            filas_con_datos = [(etiqueta, valor) for etiqueta, valor in filas_perfil if valor not in (None, "")]

            if filas_con_datos:
                elements.append(Paragraph("PERFIL DEL CANDIDATO", subtitulo_style))
                perfil_data = [
                    [Paragraph(f"<b>{etiqueta}:</b>", normal_style), Paragraph(str(valor), normal_style)]
                    for etiqueta, valor in filas_con_datos
                ]
                perfil_table = Table(perfil_data, colWidths=[1.8*inch, 4.7*inch])
                perfil_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), HexColor("#F5F5F5")),
                    ('GRID', (0, 0), (-1, -1), 0.5, GeneradorPDF.GRIS_PLATA),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('TOPPADDING', (0, 0), (-1, -1), 6),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ]))
                elements.append(perfil_table)
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
        
        # ASSESSMENT CENTERS (evaluados por IA)
        if assessment_scores:
            elements.append(Paragraph("ASSESSMENT CENTERS (Evaluación por IA)", subtitulo_style))

            assessment_data = [[
                Paragraph("<b>Escenario</b>", normal_style),
                Paragraph("<b>Score</b>", normal_style),
                Paragraph("<b>Feedback</b>", normal_style),
            ]]
            for a_score in assessment_scores:
                assessment = db.query(AssessmentCenter).filter_by(id=a_score.assessment_id).first()
                assessment_data.append([
                    Paragraph(assessment.nombre if assessment else str(a_score.assessment_id), normal_style),
                    Paragraph(f"{a_score.score_normalizado:.1f}", normal_style),
                    Paragraph(a_score.feedback_llm or "", normal_style),
                ])

            assessment_table = Table(assessment_data, colWidths=[2.5*inch, 1*inch, 3*inch])
            assessment_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), GeneradorPDF.AZUL_INSTITUCIONAL),
                ('TEXTCOLOR', (0, 0), (-1, 0), white),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 0.5, GeneradorPDF.GRIS_PLATA),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            elements.append(assessment_table)
            elements.append(Spacer(1, 0.2*inch))

        # SCORE FINAL (ya calculado arriba, junto con el resumen ejecutivo)
        if score_final is not None:
            color_final = {
                "PRIORITARIO": GeneradorPDF.ROJO,
                "VIABLE": GeneradorPDF.AZUL_INSTITUCIONAL,
                "CONSIDERAR": GeneradorPDF.ORO,
                "NO_RECOMENDADO": HexColor("#CC0000"),
            }.get(clasificacion_final, GeneradorPDF.GRIS_OSCURO)

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
