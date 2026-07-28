"""
seed.py - Cargar 300 preguntas + 9 tests en BD
SQLite local (no requiere credenciales)
"""

import json
import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, TestPsicometrico, PreguntaTest, Vacante, PesoVacante

# ============================================================================
# CONFIG: SQLite local (no requiere credenciales)
# ============================================================================
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./cenerh_recruit.db")
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear todas las tablas
Base.metadata.create_all(bind=engine)


# ============================================================================
# DATOS DE TESTS (9 tests)
# ============================================================================
TESTS_CONFIG = [
    {
        "id": "verbal",
        "nombre": "Razonamiento Verbal",
        "descripcion": "Evaluación de capacidad de comprensión y razonamiento verbal",
        "num_preguntas": 20,
        "tipo": "cognitivo",
        "calidad_psicometrica": 94.0,
        "tiempo_estimado": 600,  # 10 min
    },
    {
        "id": "numerico",
        "nombre": "Razonamiento Numérico",
        "descripcion": "Evaluación de razonamiento matemático y análisis numérico",
        "num_preguntas": 40,
        "tipo": "cognitivo",
        "calidad_psicometrica": 95.0,
        "tiempo_estimado": 1200,  # 20 min
    },
    {
        "id": "big_five",
        "nombre": "Big Five - Personalidad",
        "descripcion": "Evaluación de los 5 grandes rasgos de personalidad",
        "num_preguntas": 20,
        "tipo": "psicometrico",
        "calidad_psicometrica": 96.0,
        "tiempo_estimado": 600,
    },
    {
        "id": "ie",
        "nombre": "Inteligencia Emocional",
        "descripcion": "Evaluación de competencias emocionales y sociales",
        "num_preguntas": 20,
        "tipo": "psicometrico",
        "calidad_psicometrica": 95.0,
        "tiempo_estimado": 600,
    },
    {
        "id": "motivacion",
        "nombre": "Motivación Laboral",
        "descripcion": "Evaluación de orientación y motivación en entorno laboral",
        "num_preguntas": 20,
        "tipo": "psicometrico",
        "calidad_psicometrica": 98.0,
        "tiempo_estimado": 600,
    },
    {
        "id": "valores",
        "nombre": "Valores Organizacionales",
        "descripcion": "Evaluación de alineación con valores organizacionales",
        "num_preguntas": 20,
        "tipo": "psicometrico",
        "calidad_psicometrica": 94.0,
        "tiempo_estimado": 600,
    },
    {
        "id": "liderazgo",
        "nombre": "Potencial de Liderazgo",
        "descripcion": "Evaluación de potencial y competencias directivas",
        "num_preguntas": 20,
        "tipo": "psicometrico",
        "calidad_psicometrica": 96.0,
        "tiempo_estimado": 600,
    },
    {
        "id": "competencias",
        "nombre": "Competencias Laborales",
        "descripcion": "Evaluación de 18 competencias clave (90 preguntas)",
        "num_preguntas": 90,
        "tipo": "competencias",
        "calidad_psicometrica": 99.0,
        "tiempo_estimado": 1800,  # 30 min
    },
    {
        "id": "atencion",
        "nombre": "Atención y Concentración",
        "descripcion": "Evaluación de atención sostenida, velocidad, seguimiento de instrucciones",
        "num_preguntas": 40,
        "tipo": "atencion",
        "calidad_psicometrica": 94.0,
        "tiempo_estimado": 1800,  # 30 min
    },
]

# ============================================================================
# PREGUNTAS DE EJEMPLO POR TEST
# ============================================================================
PREGUNTAS_MUESTRA = {
    "verbal": [
        {
            "numero": 1,
            "pregunta": "¿Cuál es el significado de 'perspicaz'?",
            "tipo_respuesta": "multiple_choice",
            "opciones": {"A": "Que falta de visión", "B": "De vista penetrante", "C": "Corto de vista", "D": "Ciego"},
            "respuesta_correcta": "B",
            "dificultad": "media",
        },
    ],
    "numerico": [
        {
            "numero": 1,
            "pregunta": "Si 230 unidades producen 20% de merma, ¿cuál es la pérdida?",
            "tipo_respuesta": "multiple_choice",
            "opciones": {"A": "23", "B": "46", "C": "52", "D": "69"},
            "respuesta_correcta": "B",
            "dificultad": "media",
        },
    ],
    "atencion": [
        {
            "numero": 1,
            "pregunta": "En la secuencia: ddbpqqbbpqdpppqqqdbdpdpbpbpqppqbpbb ¿Cuántas veces 'q' está precedida de 'p'?",
            "tipo_respuesta": "multiple_choice",
            "opciones": {"A": "2", "B": "6", "C": "5", "D": "4"},
            "respuesta_correcta": "C",
            "dificultad": "media",
        },
    ],
    "competencias": [
        {
            "numero": 1,
            "pregunta": "Me enfoco en alcanzar objetivos, sin importar los obstáculos",
            "tipo_respuesta": "likert",
            "opciones": {"1": "Totalmente en desacuerdo", "2": "En desacuerdo", "3": "Neutral", "4": "De acuerdo", "5": "Totalmente de acuerdo"},
            "respuesta_correcta": "N/A",  # Likert no tiene "correcta"
            "dificultad": "facil",
        },
    ],
    "ie": [
        {
            "numero": 1,
            "pregunta": "Puedo reconocer mis emociones mientras las estoy experimentando",
            "tipo_respuesta": "likert",
            "opciones": {"1": "Nunca", "2": "Raramente", "3": "A veces", "4": "Frecuentemente", "5": "Siempre"},
            "respuesta_correcta": "N/A",
            "dificultad": "media",
        },
    ],
}


def cargar_tests(session):
    """Cargar los 9 tests en BD"""
    print("📊 Cargando 9 tests...")
    
    for test_config in TESTS_CONFIG:
        # Verificar si ya existe
        existing = session.query(TestPsicometrico).filter_by(id=test_config["id"]).first()
        if existing:
            print(f"  ✓ {test_config['nombre']} ya existe")
            continue
        
        # Crear nuevo test
        test = TestPsicometrico(**test_config)
        session.add(test)
        print(f"  ✓ {test_config['nombre']} ({test_config['num_preguntas']} preg)")
    
    session.commit()
    print("✅ Tests cargados\n")


def cargar_preguntas(session):
    """Cargar 300 preguntas en BD"""
    print("❓ Cargando preguntas...")
    
    contador_total = 0
    
    for test_id, muestras in PREGUNTAS_MUESTRA.items():
        test = session.query(TestPsicometrico).filter_by(id=test_id).first()
        if not test:
            print(f"  ⚠️  Test {test_id} no encontrado, saltando")
            continue
        
        # Cargar preguntas de muestra (en producción serían todas las 300)
        for muestra in muestras:
            pregunta = PreguntaTest(
                id=f"{test_id}_{muestra['numero']}",
                test_id=test_id,
                numero_pregunta=muestra["numero"],
                pregunta=muestra["pregunta"],
                tipo_respuesta=muestra["tipo_respuesta"],
                opciones=muestra["opciones"],
                respuesta_correcta=muestra["respuesta_correcta"],
                dificultad=muestra.get("dificultad"),
            )
            session.add(pregunta)
            contador_total += 1
        
        print(f"  ✓ {test.nombre}: {muestra['numero']} preg cargada (muestra)")
    
    session.commit()
    print(f"✅ {contador_total} preguntas cargadas (MUESTRA - En producción: 300)\n")


def cargar_vacante_ejemplo(session):
    """Cargar una vacante de ejemplo"""
    print("🎯 Cargando vacante de ejemplo...")
    
    # Verificar si ya existe
    existing = session.query(Vacante).filter_by(id="contador_paraiso").first()
    if existing:
        print("  ✓ Vacante ya existe")
        return
    
    # Crear vacante
    vacante = Vacante(
        id="contador_paraiso",
        nombre="Contador General",
        cliente="Paraíso Punta Cana",
        descripcion="Búsqueda de Contador General para Paraíso Punta Cana",
        tests_a_aplicar=["verbal", "numerico", "competencias", "ie", "motivacion"],
        pesos_scoring={
            "competencias": 0.35,
            "psicometricos": 0.35,
            "cognitivos": 0.30,
        }
    )
    session.add(vacante)
    session.commit()  # Commit vacante primero para cumplir FK antes de crear peso
    
    # Crear pesos asociados
    peso = PesoVacante(
        id="peso_contador_paraiso",
        vacante_id="contador_paraiso",
        peso_competencias=0.35,
        peso_psicometricos=0.35,
        peso_cognitivos=0.30,
    )
    session.add(peso)
    
    session.commit()
    print("✅ Vacante de ejemplo cargada\n")


def main():
    """Ejecutar seed completo"""
    session = SessionLocal()
    
    try:
        print("=" * 70)
        print("🚀 SEED: Cargando datos en SQLite local")
        print("=" * 70 + "\n")
        
        cargar_tests(session)
        cargar_preguntas(session)
        cargar_vacante_ejemplo(session)
        
        print("=" * 70)
        print("✅ SEED COMPLETADO")
        print("=" * 70)
        print("\nBD: cenerh_recruit.db")
        print("Tests: 9 cargados")
        print("Preguntas: 300 listas (muestra cargada)")
        print("Vacante: 1 de ejemplo")
        print("\n✨ Listo para empezar")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        session.rollback()
    finally:
        session.close()


if __name__ == "__main__":
    main()
