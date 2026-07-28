"""
api.py - FastAPI para CENERH RECRUIT OS
4 endpoints de lectura iniciales
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import List, Optional
from models import Base, TestPsicometrico, PreguntaTest, Vacante, Candidato, RespuestaCandidata, ScoreCandidata
import json
import os

# ============================================================================
# CONFIG
# ============================================================================
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./cenerh_recruit.db")
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CENERH RECRUIT OS",
    description="Platform de Reclutamiento y Evaluación Psicométrica",
    version="1.0.0"
)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
        CORSMiddleware,
        allow_origins=["https://cenerhrecruit-frontend.vercel.app"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
)

# ============================================================================
# DEPENDENCY: Get DB Session
# ============================================================================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================================================================
# ENDPOINT 1: GET /api/tests/disponibles
# Retorna lista de 9 tests disponibles
# ============================================================================
@app.get("/api/tests/disponibles")
async def tests_disponibles(db: Session = Depends(get_db)):
    """
    Retorna lista de todos los tests disponibles (9 tests)
    
    Response:
    {
        "status": "success",
        "total_tests": 9,
        "total_preguntas": 300,
        "tests": [
            {
                "id": "verbal",
                "nombre": "Razonamiento Verbal",
                "num_preguntas": 20,
                "tipo": "cognitivo",
                "calidad": 94.0,
                "tiempo_estimado": 600
            },
            ...
        ]
    }
    """
    try:
        tests = db.query(TestPsicometrico).all()
        
        if not tests:
            raise HTTPException(status_code=404, detail="No tests encontrados")
        
        total_preguntas = sum(t.num_preguntas for t in tests)
        
        return {
            "status": "success",
            "total_tests": len(tests),
            "total_preguntas": total_preguntas,
            "tests": [
                {
                    "id": t.id,
                    "nombre": t.nombre,
                    "descripcion": t.descripcion,
                    "num_preguntas": t.num_preguntas,
                    "tipo": t.tipo,
                    "calidad": t.calidad_psicometrica,
                    "tiempo_estimado": t.tiempo_estimado,
                }
                for t in tests
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ENDPOINT 2: GET /api/tests/{test_id}/info
# Retorna información detallada de un test
# ============================================================================
@app.get("/api/tests/{test_id}/info")
async def test_info(test_id: str, db: Session = Depends(get_db)):
    """
    Retorna información detallada de un test específico
    
    Response:
    {
        "id": "verbal",
        "nombre": "Razonamiento Verbal",
        "num_preguntas": 20,
        "calidad": 94.0,
        "preguntas_cargadas": 1,
        ...
    }
    """
    try:
        test = db.query(TestPsicometrico).filter_by(id=test_id).first()
        
        if not test:
            raise HTTPException(status_code=404, detail=f"Test '{test_id}' no encontrado")
        
        num_preguntas_cargadas = db.query(PreguntaTest).filter_by(test_id=test_id).count()
        
        return {
            "id": test.id,
            "nombre": test.nombre,
            "descripcion": test.descripcion,
            "num_preguntas_esperadas": test.num_preguntas,
            "num_preguntas_cargadas": num_preguntas_cargadas,
            "tipo": test.tipo,
            "calidad": test.calidad_psicometrica,
            "tiempo_estimado": test.tiempo_estimado,
            "creado_en": test.creado_en.isoformat(),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ENDPOINT 3: GET /api/vacantes/{vacante_id}/config
# Retorna configuración de una vacante (qué tests aplica + pesos)
# ============================================================================
@app.get("/api/vacantes/{vacante_id}/config")
async def vacante_config(vacante_id: str, db: Session = Depends(get_db)):
    """
    Retorna configuración de scoring para una vacante
    
    Response:
    {
        "vacante_id": "contador_paraiso",
        "nombre": "Contador General",
        "cliente": "Paraíso Punta Cana",
        "tests_a_aplicar": ["verbal", "numerico", "competencias", ...],
        "pesos_scoring": {
            "competencias": 0.35,
            "psicometricos": 0.35,
            "cognitivos": 0.30
        }
    }
    """
    try:
        vacante = db.query(Vacante).filter_by(id=vacante_id).first()
        
        if not vacante:
            raise HTTPException(status_code=404, detail=f"Vacante '{vacante_id}' no encontrada")
        
        # Validar que pesos sumen 1.0
        peso_total = sum(vacante.pesos_scoring.values())
        
        return {
            "vacante_id": vacante.id,
            "nombre": vacante.nombre,
            "cliente": vacante.cliente,
            "descripcion": vacante.descripcion,
            "tests_a_aplicar": vacante.tests_a_aplicar,
            "pesos_scoring": vacante.pesos_scoring,
            "peso_total": peso_total,
            "pesos_validos": abs(peso_total - 1.0) < 0.01,  # Permitir pequeño error de redondeo
            "creado_en": vacante.creado_en.isoformat(),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ENDPOINT 4: GET /api/tests/{test_id}/{candidato_id}
# Retorna las preguntas de un test para un candidato
# ============================================================================
@app.get("/api/tests/{test_id}/{candidato_id}")
async def obtener_preguntas_test(
    test_id: str,
    candidato_id: str,
    db: Session = Depends(get_db)
):
    """
    Retorna todas las preguntas de un test para que el candidato las responda
    
    Response:
    {
        "test_id": "verbal",
        "candidato_id": "cand_001",
        "total_preguntas": 20,
        "tiempo_estimado": 600,
        "preguntas": [
            {
                "id": "verbal_1",
                "numero": 1,
                "pregunta": "¿Cuál es...",
                "tipo_respuesta": "multiple_choice",
                "opciones": {"A": "...", "B": "...", ...}
            },
            ...
        ]
    }
    """
    try:
        # Verificar que test existe
        test = db.query(TestPsicometrico).filter_by(id=test_id).first()
        if not test:
            raise HTTPException(status_code=404, detail=f"Test '{test_id}' no encontrado")
        
        # Obtener preguntas
        preguntas = db.query(PreguntaTest).filter_by(test_id=test_id).all()
        
        if not preguntas:
            raise HTTPException(status_code=404, detail=f"No hay preguntas cargadas para '{test_id}'")
        
        return {
            "test_id": test_id,
            "candidato_id": candidato_id,
            "test_nombre": test.nombre,
            "total_preguntas": len(preguntas),
            "tiempo_estimado": test.tiempo_estimado,
            "preguntas": [
                {
                    "id": p.id,
                    "numero": p.numero_pregunta,
                    "pregunta": p.pregunta,
                    "tipo_respuesta": p.tipo_respuesta,
                    "opciones": p.opciones if p.opciones else {},
                }
                for p in preguntas
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# HEALTH CHECK
# ============================================================================
@app.get("/health")
async def health_check():
    """Verificar que la API está funcionando"""
    return {
        "status": "ok",
        "service": "CENERH RECRUIT OS",
        "version": "1.0.0"
    }


# ============================================================================
# ROOT
# ============================================================================
@app.post("/api/tests/{test_id}/{candidato_id}/respuestas")
async def guardar_respuestas(
    test_id: str,
    candidato_id: str,
    payload: dict,
    db: Session = Depends(get_db)
):
    """Guardar respuestas y calcular score del test"""
    try:
        from scoring import SistemaScoring
        
        test = db.query(TestPsicometrico).filter_by(id=test_id).first()
        if not test:
            raise HTTPException(status_code=404, detail=f"Test '{test_id}' no encontrado")
        
        preguntas = db.query(PreguntaTest).filter_by(test_id=test_id).all()
        respuestas = payload.get("respuestas", {})
        
        aciertos = 0
        for pregunta in preguntas:
            respuesta_dada = respuestas.get(pregunta.id, "")
            if respuesta_dada:
                es_correcta = respuesta_dada.upper() == pregunta.respuesta_correcta.upper()
                if es_correcta:
                    aciertos += 1
                
                from models import RespuestaCandidata
                import uuid
                resp_obj = RespuestaCandidata(
                    id=f"resp_{candidato_id}_{pregunta.id}_{uuid.uuid4().hex[:8]}",
                    candidato_id=candidato_id,
                    pregunta_id=pregunta.id,
                    respuesta=respuesta_dada,
                    es_correcta=es_correcta,
                )
                db.add(resp_obj)
        
        db.commit()
        
        score_obj = SistemaScoring.calcular_score_test(db, candidato_id, test_id)
        db.add(score_obj)
        db.commit()
        
        return {
            "status": "success",
            "candidato_id": candidato_id,
            "test_id": test_id,
            "test_nombre": test.nombre,
            "score": round(score_obj.score_normalizado, 1),
            "clasificacion": score_obj.clasificacion_test,
            "mensaje": f"Test '{test.nombre}' completado. Score: {round(score_obj.score_normalizado, 1)}/100"
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/candidatos/{candidato_id}/resultados")
async def obtener_resultados(
    candidato_id: str,
    db: Session = Depends(get_db)
):
    """Retorna todos los scores y score final ponderado"""
    try:
        from scoring import SistemaScoring
        
        scores = db.query(ScoreCandidata).filter_by(candidato_id=candidato_id).all()
        
        if not scores:
            raise HTTPException(status_code=404, detail=f"No hay scores para '{candidato_id}'")
        
        categorias = {
            "competencias": [],
            "psicometricos": [],
            "cognitivos": [],
        }
        
        scores_detalle = []
        
        for score in scores:
            test = db.query(TestPsicometrico).filter_by(id=score.test_id).first()
            categoria = SistemaScoring.CATEGORIA_TEST.get(score.test_id, "otros")
            
            if categoria in categorias:
                categorias[categoria].append(score.score_normalizado)
            
            scores_detalle.append({
                "test_id": score.test_id,
                "test_nombre": test.nombre if test else score.test_id,
                "score": round(score.score_normalizado, 1),
                "clasificacion": score.clasificacion_test,
            })
        
        promedios = {}
        for cat, valores in categorias.items():
            if valores:
                promedios[cat] = round(sum(valores) / len(valores), 1)
        
        pesos = {"competencias": 0.35, "psicometricos": 0.35, "cognitivos": 0.30}
        score_final = (
            promedios.get("competencias", 0) * pesos["competencias"] +
            promedios.get("psicometricos", 0) * pesos["psicometricos"] +
            promedios.get("cognitivos", 0) * pesos["cognitivos"]
        )
        score_final = round(score_final, 1)
        
        clasificacion_final = SistemaScoring._clasificar_score(score_final)
        
        return {
            "status": "success",
            "candidato_id": candidato_id,
            "score_final": score_final,
            "clasificacion_final": clasificacion_final,
            "scores_por_test": scores_detalle,
            "promedios": promedios,
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/candidatos")
async def crear_candidato(
    datos: dict,
    db: Session = Depends(get_db)
):
    """Crear nuevo candidato"""
    try:
        import uuid
        
        vacante_id = datos.get("vacante_id")
        nombre = datos.get("nombre")
        email = datos.get("email")
        
        if not all([vacante_id, nombre, email]):
            raise HTTPException(status_code=400, detail="Faltan campos: vacante_id, nombre, email")
        
        vacante = db.query(Vacante).filter_by(id=vacante_id).first()
        if not vacante:
            raise HTTPException(status_code=404, detail=f"Vacante '{vacante_id}' no encontrada")
        
        candidato = Candidato(
            id=f"cand_{uuid.uuid4().hex[:12]}",
            vacante_id=vacante_id,
            nombre=nombre,
            email=email,
            estado="iniciado",
        )
        
        db.add(candidato)
        db.commit()
        
        return {
            "status": "success",
            "candidato_id": candidato.id,
            "nombre": candidato.nombre,
            "tests_a_responder": vacante.tests_a_aplicar,
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/candidatos/{candidato_id}/ficha.pdf")
async def generar_ficha_pdf(
    candidato_id: str,
    db: Session = Depends(get_db)
):
    """Generar PDF con ficha técnica del candidato"""
    try:
        from pdf_generator import GeneradorPDF
        
        candidato = db.query(Candidato).filter_by(id=candidato_id).first()
        if not candidato:
            raise HTTPException(status_code=404, detail=f"Candidato '{candidato_id}' no encontrado")
        
        pdf_bytes = GeneradorPDF.generar_ficha_candidato(db, candidato_id)
        
        return {
            "status": "success",
            "candidato_id": candidato_id,
            "nombre": candidato.nombre,
            "tamaño_kb": round(len(pdf_bytes) / 1024, 2),
            "mensaje": "PDF generado exitosamente",
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/candidatos/{candidato_id}/email")
async def enviar_email_candidato(
    candidato_id: str,
    db: Session = Depends(get_db)
):
    """Generar PDF y enviar por email automáticamente"""
    try:
        from pdf_generator import GeneradorPDF
        from email_sender import EnviadorEmail
        
        candidato = db.query(Candidato).filter_by(id=candidato_id).first()
        if not candidato:
            raise HTTPException(status_code=404, detail=f"Candidato '{candidato_id}' no encontrado")
        
        # Generar PDF
        pdf_bytes = GeneradorPDF.generar_ficha_candidato(db, candidato_id)
        
        # Enviar email
        resultado_email = EnviadorEmail.enviar_ficha_candidato(
            email_destinatario=candidato.email,
            nombre_candidato=candidato.nombre,
            pdf_bytes=pdf_bytes,
            vacante_id=candidato.vacante_id,
        )
        
        if resultado_email["status"] == "success":
            return {
                "status": "success",
                "candidato_id": candidato_id,
                "nombre": candidato.nombre,
                "email": candidato.email,
                "mensaje": f"Ficha PDF enviada a {candidato.email}",
                "modo_envio": resultado_email.get("modo", "producción"),
            }
        else:
            raise HTTPException(status_code=500, detail=resultado_email["mensaje"])
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    """Información de la API"""
    return {
        "app": "CENERH RECRUIT OS",
        "version": "1.0.0",
        "fase": "3 - PDF + Email (COMPLETADA)",
        "endpoints_totales": 10,
        "endpoints": {
            "lectura": {
                "health": "GET /health",
                "tests_disponibles": "GET /api/tests/disponibles",
                "test_info": "GET /api/tests/{test_id}/info",
                "vacante_config": "GET /api/vacantes/{vacante_id}/config",
                "obtener_preguntas": "GET /api/tests/{test_id}/{candidato_id}",
            },
            "escritura": {
                "crear_candidato": "POST /api/candidatos",
                "guardar_respuestas": "POST /api/tests/{test_id}/{candidato_id}/respuestas",
                "obtener_resultados": "GET /api/candidatos/{candidato_id}/resultados",
            },
            "exportar": {
                "generar_pdf": "GET /api/candidatos/{candidato_id}/ficha.pdf (NUEVA)",
                "enviar_email": "POST /api/candidatos/{candidato_id}/email (NUEVA)",
            }
        },
        "status": "🚀 OPERACIONAL - LISTO PARA PRODUCCIÓN"
    }


# ============================================================================
# RUN
# ============================================================================
if __name__ == "__main__":
    import uvicorn
    print("🚀 Iniciando CENERH RECRUIT OS API")
    print("   URL: http://localhost:8000")
    print("   Docs: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
