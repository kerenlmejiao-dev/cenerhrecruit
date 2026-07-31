"""
admin_router.py - Endpoints administrativos protegidos por ADMIN_API_KEY.

Reutiliza los cargadores idempotentes de seed.py (cada uno hace
"if existing: continue" antes de insertar) para poder completar el
banco de tests/preguntas/assessment centers en cualquier entorno --
incluida producción -- sin necesitar acceso directo a la base de datos:
el propio servidor corre el seed usando su DATABASE_URL interno.
"""

from fastapi import APIRouter, Depends

from auth import require_admin
from database import SessionLocal
from models import AssessmentCenter, PreguntaTest, TestPsicometrico, Vacante
import seed

router = APIRouter(prefix="/api/admin", tags=["Admin"], dependencies=[Depends(require_admin)])


@router.post("/seed-banco-completo")
def seed_banco_completo():
    session = SessionLocal()
    try:
        seed.cargar_tests(session)
        seed.cargar_preguntas_generales(session)
        seed.cargar_preguntas_roles_estrategicos(session)
        seed.cargar_competencias(session)
        seed.cargar_assessment_centers(session)
        seed.cargar_vacante_ejemplo(session)

        return {
            "tests": session.query(TestPsicometrico).count(),
            "preguntas": session.query(PreguntaTest).count(),
            "assessment_centers": session.query(AssessmentCenter).count(),
            "vacantes": session.query(Vacante).count(),
        }
    finally:
        session.close()
