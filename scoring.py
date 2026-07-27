"""
scoring.py - Sistema de scoring ponderado para candidatos
Calcula scores por test y score final con pesos personalizables
"""

import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from models import ScoreCandidata, RespuestaCandidata, TestPsicometrico, PreguntaTest, Candidato, Vacante, PesoVacante
from typing import Dict, List, Tuple


class SistemaScoring:
    """Sistema de scoring ponderado para CENERH RECRUIT OS"""
    
    # Mapeo de tipos de test a categorías de peso
    CATEGORIA_TEST = {
        "verbal": "cognitivo",
        "numerico": "cognitivo",
        "big_five": "psicometrico",
        "ie": "psicometrico",
        "motivacion": "psicometrico",
        "valores": "psicometrico",
        "liderazgo": "psicometrico",
        "competencias": "competencias",
        "atencion": "atencion",  # Puede ir en cognitivo o atencion (flexible)
    }
    
    # Pesos por defecto (Opción A)
    PESOS_DEFAULT = {
        "competencias": 0.35,
        "psicometricos": 0.35,
        "cognitivos": 0.30,
    }
    
    @staticmethod
    def calcular_score_test(
        db: Session,
        candidato_id: str,
        test_id: str,
    ) -> ScoreCandidata:
        """
        Calcula el score de un test para un candidato
        
        Returns: ScoreCandidata object con todos los scores
        """
        
        # Obtener test y preguntas
        test = db.query(TestPsicometrico).filter_by(id=test_id).first()
        if not test:
            raise ValueError(f"Test {test_id} no encontrado")
        
        preguntas = db.query(PreguntaTest).filter_by(test_id=test_id).all()
        if not preguntas:
            raise ValueError(f"No hay preguntas para test {test_id}")
        
        # Obtener respuestas del candidato
        respuestas = db.query(RespuestaCandidata).filter_by(
            candidato_id=candidato_id
        ).join(PreguntaTest).filter(
            PreguntaTest.test_id == test_id
        ).all()
        
        if not respuestas:
            raise ValueError(f"Candidato {candidato_id} sin respuestas para {test_id}")
        
        # ====================================================================
        # CALCULAR PUNTUACIÓN DIRECTA (PD)
        # ====================================================================
        
        if test.tipo == "cognitivo" or test.tipo == "atencion":
            # Tests cognitivos: Contar aciertos
            aciertos = sum(1 for r in respuestas if r.es_correcta)
            errores = len(respuestas) - aciertos
            
            # PD con corrección por azar (1/4 de errores)
            pd = aciertos - (errores / 3)  # Corrección estándar
            
            # T-Score: Estandarización lineal
            # Media: 50, DE: 10
            # T = 50 + (X - media_poblacion) / DE_poblacion * 10
            # Simplificado: T = 50 + ((aciertos / total) - 0.5) * 20
            t_score = 50 + ((aciertos / len(respuestas)) - 0.5) * 20
            t_score = max(0, min(100, t_score))  # Limitar a 0-100
            
            score_normalizado = (aciertos / len(respuestas)) * 100  # 0-100
            
        else:
            # Tests Likert (Psicométricos, Competencias)
            # Suma de respuestas Likert (1-5)
            suma_respuestas = sum(int(r.respuesta) for r in respuestas if r.respuesta.isdigit())
            maximo_posible = len(respuestas) * 5
            
            # PD: suma directa
            pd = suma_respuestas
            
            # T-Score para Likert
            media_escala = 3.0  # Punto medio Likert
            media_respuestas = suma_respuestas / len(respuestas)
            
            # T = 50 + ((media - 3) / 1.5) * 10
            t_score = 50 + ((media_respuestas - media_escala) / 1.5) * 10
            t_score = max(0, min(100, t_score))
            
            # Score normalizado: % de máximo posible
            score_normalizado = (suma_respuestas / maximo_posible) * 100
            aciertos = None
        
        # ====================================================================
        # CALCULAR PERCENTIL (simulado)
        # ====================================================================
        percentil = SistemaScoring._calcular_percentil(score_normalizado)
        
        # ====================================================================
        # CREAR SCORE_CANDIDATA
        # ====================================================================
        score_obj = ScoreCandidata(
            id=f"score_{candidato_id}_{test_id}_{uuid.uuid4().hex[:8]}",
            candidato_id=candidato_id,
            test_id=test_id,
            puntuacion_directa=pd,
            t_score=t_score,
            percentil=percentil,
            score_normalizado=score_normalizado,
            clasificacion_test=SistemaScoring._clasificar_score(score_normalizado),
            aciertos=aciertos,
            total_preguntas=len(respuestas),
        )
        
        return score_obj
    
    @staticmethod
    def calcular_score_final(
        db: Session,
        candidato_id: str,
        vacante_id: str,
    ) -> Tuple[float, str]:
        """
        Calcula el score final ponderado de un candidato para una vacante
        
        Returns: (score_final, clasificacion)
        """
        
        # Obtener vacante y pesos
        vacante = db.query(Vacante).filter_by(id=vacante_id).first()
        if not vacante:
            raise ValueError(f"Vacante {vacante_id} no encontrada")
        
        peso_vac = db.query(PesoVacante).filter_by(vacante_id=vacante_id).first()
        if peso_vac:
            pesos = {
                "competencias": peso_vac.peso_competencias,
                "psicometricos": peso_vac.peso_psicometricos,
                "cognitivos": peso_vac.peso_cognitivos,
            }
        else:
            # Usar pesos default si no hay configuración
            pesos = SistemaScoring.PESOS_DEFAULT
        
        # Obtener scores por categoría
        scores = db.query(ScoreCandidata).filter_by(candidato_id=candidato_id).all()
        
        if not scores:
            raise ValueError(f"No hay scores para candidato {candidato_id}")
        
        # Agrupar por categoría
        categorias = {
            "competencias": [],
            "psicometricos": [],
            "cognitivos": [],
        }
        
        for score in scores:
            categoria = SistemaScoring.CATEGORIA_TEST.get(score.test_id, "otros")
            if categoria in categorias:
                categorias[categoria].append(score.score_normalizado)
        
        # Calcular promedio por categoría
        promedios = {}
        for cat, valores in categorias.items():
            if valores:
                promedios[cat] = sum(valores) / len(valores)
            else:
                promedios[cat] = 0
        
        # ====================================================================
        # CALCULAR SCORE FINAL PONDERADO
        # ====================================================================
        score_final = (
            promedios.get("competencias", 0) * pesos["competencias"] +
            promedios.get("psicometricos", 0) * pesos["psicometricos"] +
            promedios.get("cognitivos", 0) * pesos["cognitivos"]
        )
        
        # Redondear a 1 decimal
        score_final = round(score_final, 1)
        
        # Clasificación
        clasificacion = SistemaScoring._clasificar_score(score_final)
        
        return score_final, clasificacion
    
    @staticmethod
    def _clasificar_score(score: float) -> str:
        """Clasificar score en categoría"""
        if score >= 81:
            return "PRIORITARIO"
        elif score >= 61:
            return "VIABLE"
        elif score >= 41:
            return "CONSIDERAR"
        else:
            return "NO_RECOMENDADO"
    
    @staticmethod
    def _calcular_percentil(score: float) -> float:
        """
        Calcula percentil basado en score normalizado
        Simulación simple (en producción usar distribución normal)
        """
        # Aproximación: score 0-100 → percentil 0-100
        return score
    
    @staticmethod
    def generar_perfil_psicologico(
        db: Session,
        candidato_id: str,
    ) -> Dict:
        """
        Genera perfil psicológico del candidato basado en sus scores
        """
        
        scores = db.query(ScoreCandidata).filter_by(candidato_id=candidato_id).all()
        
        if not scores:
            return {"error": "Sin scores"}
        
        perfil = {
            "fortalezas": [],
            "areas_desarrollo": [],
            "recomendaciones": [],
        }
        
        # Analizar scores
        for score in scores:
            test = db.query(TestPsicometrico).filter_by(id=score.test_id).first()
            
            if score.score_normalizado >= 75:
                perfil["fortalezas"].append(f"{test.nombre}: {score.score_normalizado:.1f}/100")
            elif score.score_normalizado <= 50:
                perfil["areas_desarrollo"].append(f"{test.nombre}: {score.score_normalizado:.1f}/100")
        
        # Generar recomendaciones basadas en áreas de desarrollo
        if perfil["areas_desarrollo"]:
            perfil["recomendaciones"].append(
                "Considerar entrenamiento en áreas de menor desempeño"
            )
        
        return perfil


# ============================================================================
# FUNCIONES HELPER
# ============================================================================

def scoring_por_test(db: Session, candidato_id: str, test_id: str) -> ScoreCandidata:
    """Helper: Calcular score de un test"""
    return SistemaScoring.calcular_score_test(db, candidato_id, test_id)


def scoring_final(db: Session, candidato_id: str, vacante_id: str) -> Tuple[float, str]:
    """Helper: Calcular score final"""
    return SistemaScoring.calcular_score_final(db, candidato_id, vacante_id)


def perfil_psicologico(db: Session, candidato_id: str) -> Dict:
    """Helper: Generar perfil"""
    return SistemaScoring.generar_perfil_psicologico(db, candidato_id)
