"""
Script para inicializar BD en producción
Ejecutar una sola vez después de deploy
"""
import os
from sqlalchemy import create_engine, inspect
from models import Base, TestPsicometrico, Vacante
from seed import TESTS_CONFIG, PREGUNTAS_CONFIG
from database import get_db_session

def init_database():
    """Inicializar BD en producción"""
    
    # Obtener URL de BD
    database_url = os.getenv("DATABASE_URL", "sqlite:///cenerh_recruit.db")
    
    # SQLite usa sqlite:///, PostgreSQL usa postgresql:///
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    print(f"\n{'='*70}")
    print(f"🚀 INICIALIZANDO BD EN PRODUCCIÓN")
    print(f"{'='*70}\n")
    
    print(f"📊 BD: {database_url[:50]}...\n")
    
    # Crear engine
    engine = create_engine(database_url, echo=False)
    
    # Crear todas las tablas
    print("📋 Creando tablas...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas\n")
    
    # Verificar que tablas existen
    inspector = inspect(engine)
    tablas = inspector.get_table_names()
    print(f"📊 Tablas en BD: {len(tablas)}")
    for tabla in tablas:
        print(f"   ✓ {tabla}")
    print()
    
    # Verificar si ya hay datos
    from sqlalchemy.orm import Session
    session = Session(engine)
    
    num_tests = session.query(TestPsicometrico).count()
    
    if num_tests > 0:
        print(f"⚠️  BD ya tiene datos ({num_tests} tests)")
        print("   No cargando datos de nuevo\n")
    else:
        print("📥 Cargando datos iniciales...\n")
        
        # Cargar tests
        print("📊 Cargando tests...")
        for test_config in TESTS_CONFIG:
            test = TestPsicometrico(**test_config)
            session.add(test)
        session.commit()
        print("✅ Tests cargados\n")
        
        # Cargar preguntas (muestra)
        print("❓ Cargando preguntas de muestra...")
        pregunta_count = 0
        for test_id, preguntas in PREGUNTAS_CONFIG.items():
            from models import PreguntaTest
            for idx, pregunta in enumerate(preguntas[:2], 1):  # Solo 2 por test en muestra
                preg_obj = PreguntaTest(
                    id=f"{test_id}_{idx}",
                    test_id=test_id,
                    pregunta=pregunta.get("pregunta", ""),
                    opciones=pregunta.get("opciones", []),
                    respuesta_correcta=pregunta.get("respuesta_correcta", ""),
                    dificultad=pregunta.get("dificultad", "media"),
                )
                session.add(preg_obj)
                pregunta_count += 1
        
        session.commit()
        print(f"✅ {pregunta_count} preguntas cargadas (muestra)\n")
        
        # Crear vacante de ejemplo
        print("🎯 Creando vacante de ejemplo...")
        vacante = Vacante(
            id="contador_paraiso",
            nombre="Contador General",
            cliente="Paraíso Punta Cana",
            descripcion="Evaluación para puesto de Contador General",
            tests_a_aplicar=["verbal", "numerico", "competencias", "ie", "motivacion"],
        )
        session.add(vacante)
        session.commit()
        print("✅ Vacante de ejemplo creada\n")
    
    session.close()
    
    print(f"{'='*70}")
    print("✅ INICIALIZACIÓN COMPLETADA")
    print(f"{'='*70}\n")
    
    print("Tu BD está lista para producción.\n")
    print("Próximo paso: python api.py\n")


if __name__ == "__main__":
    init_database()
