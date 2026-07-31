"""
seed.py - Cargar el banco completo de tests + preguntas en BD
SQLite local (no requiere credenciales)
"""

import sys
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

import json
import os
from pathlib import Path

from database import SessionLocal, engine
from models import (
    AssessmentCenter,
    AssessmentPregunta,
    Base,
    PesoVacante,
    PreguntaTest,
    TestPsicometrico,
    Vacante,
)
import banco_preguntas

# Crear todas las tablas
Base.metadata.create_all(bind=engine)


# ============================================================================
# DATOS DE TESTS (9 tests base + 5 de roles estratégicos = 14 tests)
# ============================================================================
TESTS_CONFIG = [
    {"id": "verbal", "nombre": "Razonamiento Verbal", "descripcion": "Evaluación de capacidad de comprensión y razonamiento verbal", "num_preguntas": 20, "tipo": "cognitivo", "categoria_banco": "Cognitivo", "calidad_psicometrica": 94.0, "tiempo_estimado": 600},
    {"id": "numerico", "nombre": "Razonamiento Numérico", "descripcion": "Evaluación de razonamiento matemático y análisis numérico", "num_preguntas": 40, "tipo": "cognitivo", "categoria_banco": "Numérico", "calidad_psicometrica": 95.0, "tiempo_estimado": 1200},
    {"id": "big_five", "nombre": "Big Five - Personalidad", "descripcion": "Evaluación de los 5 grandes rasgos de personalidad", "num_preguntas": 20, "tipo": "psicometrico", "categoria_banco": "Personalidad", "calidad_psicometrica": 96.0, "tiempo_estimado": 600},
    {"id": "ie", "nombre": "Inteligencia Emocional", "descripcion": "Evaluación de competencias emocionales y sociales", "num_preguntas": 20, "tipo": "psicometrico", "categoria_banco": "Personalidad", "calidad_psicometrica": 95.0, "tiempo_estimado": 600},
    {"id": "motivacion", "nombre": "Motivación Laboral", "descripcion": "Evaluación de orientación y motivación en entorno laboral", "num_preguntas": 20, "tipo": "psicometrico", "categoria_banco": "Personalidad", "calidad_psicometrica": 98.0, "tiempo_estimado": 600},
    {"id": "valores", "nombre": "Valores Organizacionales", "descripcion": "Evaluación de alineación con valores organizacionales", "num_preguntas": 20, "tipo": "psicometrico", "categoria_banco": "Personalidad", "calidad_psicometrica": 94.0, "tiempo_estimado": 600},
    {"id": "liderazgo", "nombre": "Potencial de Liderazgo", "descripcion": "Evaluación de potencial y competencias directivas", "num_preguntas": 20, "tipo": "psicometrico", "categoria_banco": "Personalidad", "calidad_psicometrica": 96.0, "tiempo_estimado": 600},
    {"id": "competencias", "nombre": "Competencias Laborales", "descripcion": "Evaluación de 18 competencias clave (90 preguntas)", "num_preguntas": 90, "tipo": "competencias", "categoria_banco": "Personalidad", "calidad_psicometrica": 99.0, "tiempo_estimado": 1800},
    {"id": "atencion", "nombre": "Atención y Concentración", "descripcion": "Evaluación de atención sostenida, velocidad, seguimiento de instrucciones", "num_preguntas": 40, "tipo": "atencion", "categoria_banco": "Atención", "calidad_psicometrica": 94.0, "tiempo_estimado": 1800},
]

# Tests de Roles Estratégicos (categoria_banco="Roles Estratégicos", tipo="psicometrico" para scoring)
for test_id, config in banco_preguntas.roles_estrategicos_config().items():
    TESTS_CONFIG.append({
        "id": test_id,
        "nombre": config["nombre"],
        "descripcion": config["descripcion"],
        "num_preguntas": len(config["preguntas"]),
        "tipo": "psicometrico",
        "categoria_banco": "Roles Estratégicos",
        "calidad_psicometrica": 90.0,
        "tiempo_estimado": 300,
    })

# Tests de Banco por Industria (Fase 3) - opción múltiple con respuesta correcta,
# tipo="cognitivo" para que el scoring los cuente por aciertos (igual que verbal/numérico/atención)
for test_id, config in banco_preguntas.industria_config().items():
    TESTS_CONFIG.append({
        "id": test_id,
        "nombre": config["nombre"],
        "descripcion": config["descripcion"],
        "num_preguntas": len(config["preguntas"]),
        "tipo": "cognitivo",
        "categoria_banco": config["categoria_banco"],
        "calidad_psicometrica": 88.0,
        "tiempo_estimado": 600,
    })


def cargar_tests(session):
    """Cargar todos los tests del banco en BD"""
    print(f"📊 Cargando {len(TESTS_CONFIG)} tests...")

    for test_config in TESTS_CONFIG:
        existing = session.query(TestPsicometrico).filter_by(id=test_config["id"]).first()
        if existing:
            print(f"  ✓ {test_config['nombre']} ya existe")
            continue

        test = TestPsicometrico(**test_config)
        session.add(test)
        print(f"  ✓ {test_config['nombre']} ({test_config['num_preguntas']} preg)")

    session.commit()
    print("✅ Tests cargados\n")


def cargar_preguntas_generales(session):
    """Cargar el contenido real de verbal/numérico/atención/big_five/ie/motivación/valores/liderazgo"""
    print("❓ Cargando preguntas del banco general...")

    contador_total = 0
    preguntas_por_test = banco_preguntas.preguntas_por_test()

    for test_id, preguntas in preguntas_por_test.items():
        test = session.query(TestPsicometrico).filter_by(id=test_id).first()
        if not test:
            print(f"  ⚠️  Test {test_id} no encontrado, saltando")
            continue

        cargadas = 0
        for pregunta_data in preguntas:
            pregunta_id = f"{test_id}_{pregunta_data['numero']}"
            existing = session.query(PreguntaTest).filter_by(id=pregunta_id).first()
            if existing:
                continue

            pregunta = PreguntaTest(
                id=pregunta_id,
                test_id=test_id,
                numero_pregunta=pregunta_data["numero"],
                pregunta=pregunta_data["pregunta"],
                tipo_respuesta=pregunta_data["tipo_respuesta"],
                opciones=pregunta_data["opciones"],
                respuesta_correcta=pregunta_data["respuesta_correcta"],
                dificultad=pregunta_data.get("dificultad"),
            )
            session.add(pregunta)
            cargadas += 1
            contador_total += 1

        session.commit()
        print(f"  ✓ {test.nombre}: {cargadas} preguntas cargadas")

    print(f"✅ {contador_total} preguntas del banco general cargadas\n")


def cargar_preguntas_roles_estrategicos(session):
    """Cargar los 5 tests de Roles Estratégicos (10 preguntas Likert c/u)"""
    print("⭐ Cargando preguntas de Roles Estratégicos...")

    contador_total = 0

    for test_id, config in banco_preguntas.roles_estrategicos_config().items():
        test = session.query(TestPsicometrico).filter_by(id=test_id).first()
        if not test:
            print(f"  ⚠️  Test {test_id} no encontrado, saltando")
            continue

        cargadas = 0
        for numero, texto in enumerate(config["preguntas"], start=1):
            pregunta_id = f"{test_id}_{numero}"
            existing = session.query(PreguntaTest).filter_by(id=pregunta_id).first()
            if existing:
                continue

            pregunta = PreguntaTest(
                id=pregunta_id,
                test_id=test_id,
                numero_pregunta=numero,
                pregunta=texto,
                tipo_respuesta="likert",
                opciones=banco_preguntas.LIKERT_OPCIONES,
                respuesta_correcta="N/A",
                dificultad="media",
            )
            session.add(pregunta)
            cargadas += 1
            contador_total += 1

        session.commit()
        print(f"  ✓ {test.nombre}: {cargadas} preguntas cargadas")

    print(f"✅ {contador_total} preguntas de Roles Estratégicos cargadas\n")


def cargar_competencias(session):
    """Cargar las 90 preguntas de Competencias Laborales desde el JSON (18 competencias x 5 items Likert)"""
    print("🎯 Cargando Competencias Laborales (90 preguntas)...")

    ruta_json = Path(__file__).resolve().parent.parent / "competencias_90_preguntas.json"
    if not ruta_json.exists():
        # También buscar en el mismo directorio (por si el repo se reorganiza)
        ruta_json = Path(__file__).resolve().parent / "competencias_90_preguntas.json"
    if not ruta_json.exists():
        print("  ⚠️  competencias_90_preguntas.json no encontrado, saltando\n")
        return

    with open(ruta_json, encoding="utf-8") as f:
        competencias_data = json.load(f)

    test = session.query(TestPsicometrico).filter_by(id="competencias").first()
    if not test:
        print("  ⚠️  Test 'competencias' no encontrado, saltando\n")
        return

    contador_total = 0
    numero_global = 0

    for competencia_id, competencia in competencias_data.items():
        for texto in competencia["preguntas"]:
            numero_global += 1
            pregunta_id = f"competencias_{numero_global}"
            existing = session.query(PreguntaTest).filter_by(id=pregunta_id).first()
            if existing:
                continue

            pregunta = PreguntaTest(
                id=pregunta_id,
                test_id="competencias",
                numero_pregunta=numero_global,
                pregunta=texto,
                tipo_respuesta="likert",
                opciones=banco_preguntas.LIKERT_OPCIONES,
                respuesta_correcta="N/A",
                dificultad="facil",
            )
            session.add(pregunta)
            contador_total += 1

    session.commit()
    print(f"✅ {contador_total} preguntas de Competencias cargadas ({len(competencias_data)} competencias)\n")


def cargar_assessment_centers(session):
    """Cargar los 5 assessment centers (evaluados por IA) para los roles estratégicos"""
    print("🧩 Cargando Assessment Centers...")

    contador = 0
    for categoria, config in banco_preguntas.ASSESSMENT_CENTERS.items():
        existing = session.query(AssessmentCenter).filter_by(nombre=config["nombre"]).first()
        if existing:
            print(f"  ✓ {config['nombre']} ya existe")
            continue

        assessment = AssessmentCenter(
            nombre=config["nombre"],
            descripcion=config["descripcion"],
            categoria=categoria,
        )
        session.add(assessment)
        session.flush()  # Para obtener assessment.id

        pregunta = AssessmentPregunta(
            assessment_id=assessment.id,
            numero=1,
            escenario=config["escenario"],
            rubrica_json=config["rubrica"],
        )
        session.add(pregunta)
        contador += 1
        print(f"  ✓ {config['nombre']} ({categoria})")

    session.commit()
    print(f"✅ {contador} Assessment Centers cargados\n")


def cargar_vacante_ejemplo(session):
    """Cargar vacantes de ejemplo"""
    print("🎯 Cargando vacantes de ejemplo...")

    vacantes_data = [
        {
            "id": "contador_paraiso",
            "nombre": "Contador General",
            "cliente": "Paraíso Punta Cana",
            "descripcion": "Búsqueda de Contador General para Paraíso Punta Cana",
            "tests_a_aplicar": ["verbal", "numerico", "competencias", "ie", "motivacion"],
        },
        {
            "id": "ingeniero_procesos",
            "nombre": "Ingeniero de Procesos",
            "cliente": "CENERH",
            "descripcion": "Búsqueda de Ingeniero de Procesos para CENERH",
            "tests_a_aplicar": ["numerico", "atencion", "competencias", "big_five", "ie"],
        },
        {
            "id": "gerente_operativo",
            "nombre": "Gerente Operativo",
            "cliente": "CENERH",
            "descripcion": "Búsqueda de Gerente Operativo para CENERH",
            "tests_a_aplicar": ["verbal", "liderazgo", "competencias", "motivacion", "valores"],
        },
    ]

    for data in vacantes_data:
        existing = session.query(Vacante).filter_by(id=data["id"]).first()
        if existing:
            print(f"  ✓ Vacante {data['id']} ya existe")
            continue

        vacante = Vacante(
            id=data["id"],
            nombre=data["nombre"],
            cliente=data["cliente"],
            descripcion=data["descripcion"],
            tests_a_aplicar=data["tests_a_aplicar"],
            pesos_scoring={
                "competencias": 0.35,
                "psicometricos": 0.35,
                "cognitivos": 0.30,
            }
        )
        session.add(vacante)
        session.commit()  # Commit vacante primero para cumplir FK antes de crear peso

        peso = PesoVacante(
            id=f"peso_{data['id']}",
            vacante_id=data["id"],
            peso_competencias=0.35,
            peso_psicometricos=0.35,
            peso_cognitivos=0.30,
        )
        session.add(peso)
        session.commit()
        print(f"✅ Vacante {data['id']} cargada")

    print()


def main():
    """Ejecutar seed completo"""
    session = SessionLocal()

    try:
        print("=" * 70)
        print("🚀 SEED: Cargando banco completo de tests en SQLite local")
        print("=" * 70 + "\n")

        cargar_tests(session)
        cargar_preguntas_generales(session)
        cargar_preguntas_roles_estrategicos(session)
        cargar_competencias(session)
        cargar_assessment_centers(session)
        cargar_vacante_ejemplo(session)

        total_tests = session.query(TestPsicometrico).count()
        total_preguntas = session.query(PreguntaTest).count()

        print("=" * 70)
        print("✅ SEED COMPLETADO")
        print("=" * 70)
        print(f"\nBD: cenerh_recruit.db")
        print(f"Tests: {total_tests} cargados")
        print(f"Preguntas: {total_preguntas} cargadas (contenido real, no muestra)")
        print("Vacantes: 3 de ejemplo")
        print("\n✨ Listo para empezar")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()
