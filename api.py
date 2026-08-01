"""
api.py - FastAPI para CENERH RECRUIT OS
4 endpoints de lectura iniciales
"""

import sys
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

import json
import os
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()  # Debe ejecutarse antes de importar módulos que leen os.getenv() al cargarse

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.responses import JSONResponse, FileResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict
from models import (
    AssessmentCenter,
    AssessmentScore,
    Base,
    Candidato,
    CandidatoPerfil,
    PreguntaTest,
    Referencia,
    RespuestaCandidata,
    ScoreCandidata,
    TestPsicometrico,
    Usuario,
    Vacante,
)
from auth import require_admin
from auth_users import require_membresia_activa, require_role
from database import engine, get_db
from migraciones import aplicar_migraciones

# ============================================================================
# CONFIG
# ============================================================================
Base.metadata.create_all(bind=engine)
aplicar_migraciones(engine)

app = FastAPI(
    title="CENERH RECRUIT OS",
    description="Platform de Reclutamiento y Evaluación Psicométrica",
    version="1.0.0"
)

from fastapi.middleware.cors import CORSMiddleware

# Orígenes permitidos: configurables por variable de entorno (coma-separados).
# Por defecto solo se permite desarrollo local.
_default_origins = "http://localhost:5173,http://127.0.0.1:5173"
ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("ALLOWED_ORIGINS", _default_origins).split(",")
    if origin.strip()
]

app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Content-Disposition"],
)

import auth_router
import reclutador_router
import empresa_router
import candidato_router
import pagos_router
import admin_router

app.include_router(auth_router.router)
app.include_router(reclutador_router.router)
app.include_router(empresa_router.router)
app.include_router(candidato_router.router)
app.include_router(pagos_router.router)
app.include_router(admin_router.router)

# ============================================================================
# MODELOS DE ENTRADA (validación de payloads)
# ============================================================================
class CandidatoCreate(BaseModel):
    # Nulo/omitido = se registra en la bolsa de talento, sin aplicar a una
    # vacante puntual todavía.
    vacante_id: Optional[str] = None
    nombre: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    telefono: Optional[str] = Field(default=None, max_length=30)
    # Crea (o inicia sesión en) su cuenta de candidato, para que pueda volver
    # a entrar después con email+contraseña en vez de depender del navegador.
    password: str = Field(..., min_length=8)


class RespuestasPayload(BaseModel):
    respuestas: Dict[str, str] = Field(default_factory=dict)


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
# ENDPOINT: GET /api/vacantes
# Lista pública de vacantes activas (para el formulario de postulación)
# ============================================================================
@app.get("/api/vacantes")
async def listar_vacantes_publico(db: Session = Depends(get_db)):
    vacantes = db.query(Vacante).filter_by(estado="activa").order_by(Vacante.creado_en.desc()).all()
    return {
        "vacantes": [
            {"id": v.id, "nombre": v.nombre, "cliente": v.cliente, "descripcion": v.descripcion}
            for v in vacantes
        ]
    }


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
            "estado": vacante.estado,
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
    payload: RespuestasPayload,
    db: Session = Depends(get_db)
):
    """Guardar respuestas y calcular score del test"""
    try:
        from scoring import SistemaScoring

        candidato = db.query(Candidato).filter_by(id=candidato_id).first()
        if not candidato:
            raise HTTPException(status_code=404, detail=f"Candidato '{candidato_id}' no encontrado")

        test = db.query(TestPsicometrico).filter_by(id=test_id).first()
        if not test:
            raise HTTPException(status_code=404, detail=f"Test '{test_id}' no encontrado")

        preguntas = db.query(PreguntaTest).filter_by(test_id=test_id).all()
        respuestas = payload.respuestas
        
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
    """Retorna todos los scores, puntúa assessments pendientes, y persiste el score final ponderado"""
    try:
        from scoring import SistemaScoring, scoring_final
        from assessment_service import puntuar_todos_los_assessments_candidato

        candidato = db.query(Candidato).filter_by(id=candidato_id).first()
        if not candidato:
            raise HTTPException(status_code=404, detail=f"Candidato '{candidato_id}' no encontrado")

        scores = db.query(ScoreCandidata).filter_by(candidato_id=candidato_id).all()
        if not scores:
            raise HTTPException(status_code=404, detail=f"No hay scores para '{candidato_id}'")

        scores_detalle = []
        categorias_display = {"competencias": [], "psicometricos": [], "cognitivos": []}
        for score in scores:
            test = db.query(TestPsicometrico).filter_by(id=score.test_id).first()
            scores_detalle.append({
                "test_id": score.test_id,
                "test_nombre": test.nombre if test else score.test_id,
                "score": round(score.score_normalizado, 1),
                "clasificacion": score.clasificacion_test,
            })
            categoria = SistemaScoring.CATEGORIA_TEST.get(score.test_id)
            if categoria in categorias_display:
                categorias_display[categoria].append(score.score_normalizado)

        # Solo para exhibición (desglose por categoría); el score final ponderado
        # se calcula una única vez en scoring.py (scoring_final), sin duplicar la fórmula.
        promedios = {
            cat: round(sum(valores) / len(valores), 1)
            for cat, valores in categorias_display.items()
            if valores
        }

        score_tests, _clasificacion_tests = scoring_final(db, candidato_id, candidato.vacante_id)

        # Puntuar (o recuperar) los assessment centers respondidos por el candidato
        puntuar_todos_los_assessments_candidato(db, candidato_id)
        assessment_scores = db.query(AssessmentScore).filter_by(candidato_id=candidato_id).all()

        assessments_detalle = [
            {
                "assessment_id": a.assessment_id,
                "nombre": db.query(AssessmentCenter).filter_by(id=a.assessment_id).first().nombre,
                "score": round(a.score_normalizado, 1),
                "feedback": a.feedback_llm,
                "revisado_por_humano": a.revisado_por_humano,
            }
            for a in assessment_scores
        ]

        if assessment_scores:
            promedio_assessments = sum(a.score_normalizado for a in assessment_scores) / len(assessment_scores)
            # Score final: 80% tests tradicionales + 20% assessment centers
            score_final = round(score_tests * 0.8 + promedio_assessments * 0.2, 1)
        else:
            score_final = score_tests

        clasificacion_final = SistemaScoring._clasificar_score(score_final)

        candidato.score_final = score_final
        candidato.clasificacion = clasificacion_final
        candidato.estado = "completado"
        candidato.fecha_completitud = candidato.fecha_completitud or datetime.utcnow()
        db.commit()

        # El candidato nunca ve su score, clasificación ni desglose -- eso es
        # solo para el reclutador (ver /api/reclutador/candidatos/{id}/assessments
        # en reclutador_router.py). Esta respuesta pública solo confirma que el
        # proceso de evaluación terminó y en qué etapa de reclutamiento va.
        return {
            "status": "success",
            "candidato_id": candidato_id,
            "status_reclutamiento": candidato.status_reclutamiento,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/candidatos")
async def crear_candidato(
    datos: CandidatoCreate,
    db: Session = Depends(get_db)
):
    """Crear nuevo candidato"""
    try:
        import uuid
        from auth_users import create_access_token, hash_password, verify_password

        vacante = None
        if datos.vacante_id:
            vacante = db.query(Vacante).filter_by(id=datos.vacante_id).first()
            if not vacante:
                raise HTTPException(status_code=404, detail=f"Vacante '{datos.vacante_id}' no encontrada")
            if vacante.estado != "activa":
                raise HTTPException(status_code=400, detail="Esta vacante no está disponible para aplicar")

        # Cuenta de candidato (email + contraseña), separada de cada aplicación
        # individual -- un mismo candidato puede tener varias aplicaciones
        # (una por vacante) pero una sola cuenta para iniciar sesión.
        cuenta = db.query(Usuario).filter_by(email=datos.email).first()
        if cuenta and cuenta.rol != "candidato":
            raise HTTPException(status_code=400, detail="Este correo ya está en uso. Usa otro correo.")
        if cuenta:
            if not verify_password(datos.password, cuenta.password_hash):
                raise HTTPException(
                    status_code=401,
                    detail="Ya existe una cuenta con este correo. Ingresa la contraseña de tu cuenta para continuar.",
                )
        else:
            cuenta = Usuario(
                email=datos.email,
                password_hash=hash_password(datos.password),
                nombre=datos.nombre,
                rol="candidato",
            )
            db.add(cuenta)
            db.commit()

        candidato = Candidato(
            id=f"cand_{uuid.uuid4().hex[:12]}",
            vacante_id=datos.vacante_id,
            nombre=datos.nombre,
            email=datos.email,
            telefono=datos.telefono,
            estado="iniciado",
        )

        db.add(candidato)
        db.commit()

        # Candidato recurrente: si ya aplicó antes con este mismo email, reutiliza
        # los datos de su perfil más reciente (precargados, editables para esta
        # aplicación sin afectar la aplicación anterior).
        aplicacion_anterior = (
            db.query(Candidato)
            .filter(Candidato.email == datos.email, Candidato.id != candidato.id)
            .order_by(Candidato.fecha_inicio.desc())
            .first()
        )
        if aplicacion_anterior and aplicacion_anterior.perfil:
            perfil_anterior = aplicacion_anterior.perfil
            nuevo_perfil = CandidatoPerfil(candidato_id=candidato.id)
            for columna in CandidatoPerfil.__table__.columns:
                if columna.name in ("id", "candidato_id", "actualizado_en"):
                    continue
                setattr(nuevo_perfil, columna.name, getattr(perfil_anterior, columna.name))
            db.add(nuevo_perfil)
            db.commit()

        # Prioriza vacante_tests (selector del portal reclutador); si la vacante
        # no tiene ninguno asignado (vacantes de ejemplo del seed), usa el JSON legado.
        # Sin vacante (bolsa de talento) no hay tests que responder todavía.
        tests_a_responder = []
        if vacante:
            tests_desde_relacion = [
                vt.test_id
                for vt in sorted(vacante.vacante_tests, key=lambda vt: (vt.orden if vt.orden is not None else 0))
            ]
            tests_a_responder = tests_desde_relacion or vacante.tests_a_aplicar

        if vacante and vacante.creado_por_usuario_id:
            reclutador_dueno = db.query(Usuario).filter_by(id=vacante.creado_por_usuario_id).first()
            if reclutador_dueno and reclutador_dueno.telefono:
                import whatsapp_service

                whatsapp_service.notificar_nueva_aplicacion(reclutador_dueno.telefono, candidato.nombre, vacante.nombre)

        return {
            "status": "success",
            "candidato_id": candidato.id,
            "nombre": candidato.nombre,
            "es_bolsa_talento": vacante is None,
            "tests_a_responder": tests_a_responder,
            "access_token": create_access_token(cuenta),
            "token_type": "bearer",
            "usuario": {
                "id": cuenta.id,
                "email": cuenta.email,
                "nombre": cuenta.nombre,
                "rol": cuenta.rol,
            },
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/candidatos/mis-aplicaciones")
async def mis_aplicaciones(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_role("candidato")),
):
    """Todas las aplicaciones del candidato autenticado (una por vacante a la
    que aplicó, más el perfil de bolsa de talento si lo tiene). Nunca incluye
    score ni clasificación -- solo el estado del proceso, igual que
    /api/candidatos/{id}/resultados."""
    candidatos = (
        db.query(Candidato)
        .filter(Candidato.email == usuario.email)
        .order_by(Candidato.fecha_inicio.desc())
        .all()
    )
    return {
        "aplicaciones": [
            {
                "candidato_id": c.id,
                "vacante_id": c.vacante_id,
                "vacante_nombre": c.vacante.nombre if c.vacante else None,
                "vacante_cliente": c.vacante.cliente if c.vacante else None,
                "estado": c.estado,
                "status_reclutamiento": c.status_reclutamiento,
                "fecha_inicio": c.fecha_inicio.isoformat() if c.fecha_inicio else None,
            }
            for c in candidatos
        ]
    }


@app.get("/api/candidatos/{candidato_id}/ficha.pdf")
async def generar_ficha_pdf(
    candidato_id: str,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_membresia_activa),
):
    """Generar y descargar el PDF con la ficha técnica del candidato.

    La ficha incluye datos personales sensibles (cédula, salario, dirección,
    contacto de emergencia), así que solo el reclutador dueño de la vacante
    (o el owner) puede descargarla."""
    try:
        from fastapi import Response
        from pdf_generator import GeneradorPDF

        candidato = db.query(Candidato).filter_by(id=candidato_id).first()
        if not candidato:
            raise HTTPException(status_code=404, detail=f"Candidato '{candidato_id}' no encontrado")

        # Bolsa de talento (sin vacante): no pertenece a ningún reclutador en
        # particular, cualquiera con sesión puede descargar la ficha.
        if candidato.vacante_id is not None:
            vacante = db.query(Vacante).filter_by(id=candidato.vacante_id).first()
            if usuario.rol != "owner" and (not vacante or vacante.creado_por_usuario_id != usuario.id):
                raise HTTPException(status_code=403, detail="No autorizado para ver la ficha de este candidato")

        pdf_bytes = GeneradorPDF.generar_ficha_candidato(db, candidato_id)

        nombre_archivo = f"Ficha_{candidato.nombre.replace(' ', '_')}.pdf"
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{nombre_archivo}"'},
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# NOTA: existió aquí un endpoint público POST /api/candidatos/{id}/email que
# generaba la ficha PDF (con score y clasificación) y la enviaba por correo
# directamente al candidato. Se eliminó: el candidato no debe recibir sus
# resultados por ningún medio, ni en pantalla ni por email -- esa información
# es solo para el reclutador.


# ============================================================================
# VERIFICACIÓN DE REFERENCIAS - formulario público (token-based, sin login)
#
# El token es la capacidad de acceso, igual que candidato_id en el resto del
# flujo del candidato: quien tiene el link puede responder, nadie más.
# ============================================================================
class RespuestaReferenciaPayload(BaseModel):
    calificacion_general: int = Field(..., ge=1, le=5)
    recontrataria: bool
    comentarios: Optional[str] = Field(default=None, max_length=2000)


@app.get("/api/referencias/{token}")
async def obtener_referencia(token: str, db: Session = Depends(get_db)):
    """Contexto mínimo para mostrar el formulario: a quién de referencia y
    sobre qué candidato -- nunca datos sensibles del candidato (cédula,
    salario, dirección, etc.)."""
    referencia = db.query(Referencia).filter_by(token=token).first()
    if not referencia:
        raise HTTPException(status_code=404, detail="Este link no es válido")

    candidato = db.query(Candidato).filter_by(id=referencia.candidato_id).first()
    return {
        "nombre_referencia": referencia.nombre,
        "nombre_candidato": candidato.nombre if candidato else "el candidato",
        "ya_respondida": referencia.respondido_en is not None,
    }


@app.post("/api/referencias/{token}/responder")
async def responder_referencia(
    token: str,
    payload: RespuestaReferenciaPayload,
    db: Session = Depends(get_db),
):
    referencia = db.query(Referencia).filter_by(token=token).first()
    if not referencia:
        raise HTTPException(status_code=404, detail="Este link no es válido")
    if referencia.respondido_en is not None:
        raise HTTPException(status_code=400, detail="Esta referencia ya fue respondida")

    referencia.calificacion_general = payload.calificacion_general
    referencia.recontrataria = payload.recontrataria
    referencia.comentarios = payload.comentarios
    referencia.respondido_en = datetime.utcnow()
    db.commit()

    return {"status": "success"}


@app.get("/api/info")
async def info():
    """Información de la API"""
    return {
        "app": "CENERH RECRUIT OS",
        "version": "1.0.0",
        "status": "OPERACIONAL",
    }


# ============================================================================
# FRONTEND (servido desde el mismo backend cuando existe un build de producción)
#
# En desarrollo (npm run dev) el frontend corre aparte en :5173 y esta sección
# no hace nada (dist/ no existe). Para exponer la app por un solo túnel/puerto,
# genera el build (`npm run build`) antes de arrancar la API.
# ============================================================================
_FRONTEND_DIST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist")

if os.path.isdir(_FRONTEND_DIST):
    from fastapi.staticfiles import StaticFiles

    _assets_dir = os.path.join(_FRONTEND_DIST, "assets")
    if os.path.isdir(_assets_dir):
        app.mount("/assets", StaticFiles(directory=_assets_dir), name="frontend-assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    async def servir_frontend(full_path: str):
        """Catch-all: cualquier ruta que no sea de la API sirve el index.html
        del frontend, para que las rutas de React Router (ej. /reclutador,
        /empresa/vacantes/123) funcionen al recargar o entrar por link directo."""
        return FileResponse(os.path.join(_FRONTEND_DIST, "index.html"))


# ============================================================================
# RUN
# ============================================================================
if __name__ == "__main__":
    import uvicorn

    # Hay que escuchar en 0.0.0.0 (no 127.0.0.1) para que el proxy de Railway
    # pueda llegar al contenedor. El puerto se queda fijo en 8000 a propósito
    # -- no leemos $PORT porque el "Public Networking" de este servicio en
    # Railway ya está configurado para enrutar al 8000, y $PORT resultó traer
    # un valor distinto (8080) que no coincide, causando 502.
    # API_HOST/API_PORT siguen mandando si están definidas explícitamente
    # (como en el .env local), para no cambiar el comportamiento en desarrollo.
    api_host = os.getenv("API_HOST", "0.0.0.0")
    api_port = int(os.getenv("API_PORT", "8000"))

    print("🚀 Iniciando CENERH RECRUIT OS API")
    print(f"   URL: http://{api_host}:{api_port}")
    print(f"   Docs: http://{api_host}:{api_port}/docs")
    uvicorn.run(app, host=api_host, port=api_port)
