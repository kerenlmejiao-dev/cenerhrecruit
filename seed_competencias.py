# seed_competencias.py
# Script para cargar 18 competencias + 90 preguntas en BD
# Ejecutar UNA SOLA VEZ en inicialización

from models_competencias import Competencia, PreguntaCompetencia

# ============================================================================
# DATOS: 18 COMPETENCIAS + 90 PREGUNTAS
# ============================================================================

DATOS_COMPETENCIAS = {
    1: {
        "nombre": "Orientación a Resultados",
        "descripcion": "Capacidad para establecer objetivos claros y mantener el enfoque en su logro.",
        "preguntas": [
            "Establezco objetivos claros antes de iniciar un trabajo.",
            "Busco alternativas cuando encuentro obstáculos para cumplir una meta.",
            "Mantengo el enfoque hasta terminar las tareas asignadas.",
            "Me esfuerzo por superar los resultados esperados.",
            "Evalúo mis resultados para identificar oportunidades de mejora."
        ]
    },
    2: {
        "nombre": "Trabajo en Equipo",
        "descripcion": "Habilidad para colaborar con otros y contribuir al logro de objetivos colectivos.",
        "preguntas": [
            "Comparto información útil con mis compañeros.",
            "Estoy dispuesto a apoyar a otros cuando lo necesitan.",
            "Escucho y considero las opiniones de los demás.",
            "Colaboro para resolver conflictos dentro del equipo.",
            "Celebro los logros colectivos más que los individuales."
        ]
    },
    3: {
        "nombre": "Comunicación",
        "descripcion": "Capacidad para expresarse claramente y adaptar el mensaje según la audiencia.",
        "preguntas": [
            "Expreso mis ideas de forma clara y organizada.",
            "Adapto mi comunicación según la persona con quien hablo.",
            "Escucho atentamente antes de responder.",
            "Confirmo que mi mensaje haya sido comprendido.",
            "Mantengo una comunicación respetuosa incluso en situaciones difíciles."
        ]
    },
    4: {
        "nombre": "Adaptabilidad",
        "descripcion": "Capacidad para ajustarse rápidamente a cambios y nuevas situaciones.",
        "preguntas": [
            "Me ajusto rápidamente a cambios en procedimientos.",
            "Mantengo una actitud positiva ante nuevas responsabilidades.",
            "Aprendo con rapidez nuevas herramientas o tecnologías.",
            "Cambio mis prioridades cuando la situación lo requiere.",
            "Mantengo un buen desempeño durante los cambios organizacionales."
        ]
    },
    5: {
        "nombre": "Responsabilidad",
        "descripcion": "Compromiso con cumplir tareas, plazos y compromisos asumidos.",
        "preguntas": [
            "Cumplo los plazos establecidos.",
            "Asumo las consecuencias de mis decisiones.",
            "Completo mis tareas sin necesidad de supervisión constante.",
            "Organizo mi trabajo para evitar retrasos.",
            "Soy puntual en mis compromisos laborales."
        ]
    },
    6: {
        "nombre": "Resolución de Problemas",
        "descripcion": "Capacidad para identificar, analizar y resolver problemas de forma efectiva.",
        "preguntas": [
            "Analizo las causas antes de buscar soluciones.",
            "Considero varias alternativas antes de decidir.",
            "Mantengo la calma frente a problemas inesperados.",
            "Busco información adicional cuando la necesito.",
            "Evalúo la efectividad de las soluciones implementadas."
        ]
    },
    7: {
        "nombre": "Orientación al Cliente",
        "descripcion": "Enfoque en identificar y satisfacer necesidades del cliente.",
        "preguntas": [
            "Identifico las necesidades del cliente antes de ofrecer soluciones.",
            "Respondo oportunamente a las solicitudes del cliente.",
            "Busco superar las expectativas del cliente.",
            "Manejo adecuadamente las quejas.",
            "Mantengo una actitud amable y profesional."
        ]
    },
    8: {
        "nombre": "Organización y Planificación",
        "descripcion": "Capacidad para estructurar el trabajo y gestionar el tiempo efectivamente.",
        "preguntas": [
            "Planifico mis actividades diarias.",
            "Establezco prioridades según la importancia de las tareas.",
            "Utilizo herramientas para organizar mi trabajo.",
            "Evito dejar tareas importantes para último momento.",
            "Cumplo con los cronogramas establecidos."
        ]
    },
    9: {
        "nombre": "Aprendizaje Continuo",
        "descripcion": "Disposición a aprender nuevas habilidades y mantenerse actualizado.",
        "preguntas": [
            "Busco oportunidades para aprender nuevas habilidades.",
            "Solicito retroalimentación para mejorar.",
            "Aplico lo aprendido en mi trabajo.",
            "Me actualizo sobre tendencias de mi profesión.",
            "Comparto conocimientos con otras personas."
        ]
    },
    10: {
        "nombre": "Ética e Integridad",
        "descripcion": "Actuación honesta, transparente y coherente con valores y políticas.",
        "preguntas": [
            "Actúo con honestidad incluso cuando nadie me observa.",
            "Respeto la confidencialidad de la información.",
            "Cumplo las políticas de la organización.",
            "Rechazo conductas poco éticas.",
            "Admito mis errores cuando los cometo."
        ]
    },
    11: {
        "nombre": "Innovación",
        "descripcion": "Disposición a proponer nuevas ideas y buscar formas más eficientes de trabajar.",
        "preguntas": [
            "Propongo nuevas ideas para mejorar procesos.",
            "Busco formas más eficientes de realizar mi trabajo.",
            "Estoy dispuesto a experimentar nuevas soluciones.",
            "Analizo tendencias que puedan beneficiar a la organización.",
            "Promuevo la mejora continua en mi área."
        ]
    },
    12: {
        "nombre": "Toma de Decisiones",
        "descripcion": "Capacidad para analizar información y tomar decisiones oportunas y acertadas.",
        "preguntas": [
            "Analizo información antes de decidir.",
            "Considero los riesgos de cada alternativa.",
            "Tomo decisiones oportunamente.",
            "Asumo la responsabilidad de mis decisiones.",
            "Evalúo los resultados obtenidos."
        ]
    },
    13: {
        "nombre": "Iniciativa",
        "descripcion": "Capacidad para identificar oportunidades y actuar proactivamente sin esperar instrucciones.",
        "preguntas": [
            "Identifico oportunidades de mejora sin que me lo soliciten.",
            "Actúo rápidamente cuando detecto un problema.",
            "Busco nuevas responsabilidades.",
            "Presento propuestas para optimizar procesos.",
            "Me anticipo a las necesidades del trabajo."
        ]
    },
    14: {
        "nombre": "Manejo del Estrés",
        "descripcion": "Capacidad para mantener el desempeño y equilibrio bajo presión.",
        "preguntas": [
            "Mantengo la calma bajo presión.",
            "Organizo mis prioridades cuando aumenta la carga laboral.",
            "Evito reaccionar impulsivamente.",
            "Mantengo una actitud positiva en momentos difíciles.",
            "Continúo siendo productivo en situaciones de alta demanda."
        ]
    },
    15: {
        "nombre": "Liderazgo",
        "descripcion": "Capacidad para inspirar, motivar y desarrollar a otros hacia objetivos comunes.",
        "preguntas": [
            "Inspiro confianza en otras personas.",
            "Delego responsabilidades de manera adecuada.",
            "Motivo al equipo para alcanzar los objetivos.",
            "Desarrollo el talento de mis colaboradores.",
            "Tomo decisiones difíciles cuando es necesario."
        ]
    },
    16: {
        "nombre": "Negociación",
        "descripcion": "Capacidad para llegar a acuerdos beneficiosos para ambas partes.",
        "preguntas": [
            "Busco acuerdos beneficiosos para ambas partes.",
            "Escucho los intereses de la otra persona.",
            "Mantengo una actitud respetuosa durante la negociación.",
            "Presento argumentos basados en hechos.",
            "Busco relaciones de largo plazo."
        ]
    },
    17: {
        "nombre": "Inteligencia Emocional",
        "descripcion": "Capacidad para reconocer y gestionar propias emociones y la de otros.",
        "preguntas": [
            "Reconozco mis emociones antes de actuar.",
            "Comprendo las emociones de otras personas.",
            "Mantengo el autocontrol durante conflictos.",
            "Acepto críticas constructivas.",
            "Me recupero rápidamente de situaciones difíciles."
        ]
    },
    18: {
        "nombre": "Compromiso Organizacional",
        "descripcion": "Identificación y compromiso con los objetivos y valores de la organización.",
        "preguntas": [
            "Me siento orgulloso de pertenecer a la organización.",
            "Doy un esfuerzo adicional cuando es necesario.",
            "Defiendo la buena imagen de la empresa.",
            "Cumplo con las normas y procedimientos establecidos.",
            "Contribuyo activamente al logro de los objetivos organizacionales."
        ]
    }
}


# ============================================================================
# FUNCIÓN: Cargar datos en BD
# ============================================================================

def cargar_competencias(session):
    """
    Inserta 18 competencias + 90 preguntas en la BD.
    
    Uso:
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        from seed_competencias import cargar_competencias
        
        engine = create_engine("postgresql://user:pass@localhost/cenerh_recruit_os")
        Session = sessionmaker(bind=engine)
        session = Session()
        
        cargar_competencias(session)
        print("✅ Cargado")
    """
    
    try:
        # Verificar si ya existen competencias
        competencias_existentes = session.query(Competencia).count()
        if competencias_existentes > 0:
            print(f"⚠️  Ya existen {competencias_existentes} competencias en BD. No se cargarán duplicados.")
            return
        
        contador_competencias = 0
        contador_preguntas = 0
        
        # Insertar competencias + preguntas
        for comp_id, comp_data in DATOS_COMPETENCIAS.items():
            # Crear competencia
            competencia = Competencia(
                id=comp_id,
                nombre=comp_data['nombre'],
                descripcion=comp_data['descripcion'],
                numero_preguntas=len(comp_data['preguntas'])
            )
            session.add(competencia)
            contador_competencias += 1
            
            # Crear preguntas asociadas
            for num_preg, pregunta_texto in enumerate(comp_data['preguntas'], 1):
                pregunta = PreguntaCompetencia(
                    competencia_id=comp_id,
                    numero_pregunta=num_preg,
                    pregunta=pregunta_texto,
                    escala_minima=1,
                    escala_maxima=5
                )
                session.add(pregunta)
                contador_preguntas += 1
        
        # Guardar
        session.commit()
        
        print("✅ COMPETENCIAS CARGADAS EN BD")
        print(f"   └─ {contador_competencias} competencias")
        print(f"   └─ {contador_preguntas} preguntas (Likert 1-5)")
        print(f"   └─ Listo para API")
        
        return True
    
    except Exception as e:
        session.rollback()
        print(f"❌ Error al cargar competencias: {e}")
        return False


# ============================================================================
# FUNCIÓN: Verificar carga
# ============================================================================

def verificar_carga(session):
    """Verifica que los datos hayan sido cargados correctamente."""
    
    total_competencias = session.query(Competencia).count()
    total_preguntas = session.query(PreguntaCompetencia).count()
    
    print("\n📊 VERIFICACIÓN DE CARGA")
    print(f"   Competencias: {total_competencias}")
    print(f"   Preguntas: {total_preguntas}")
    
    if total_competencias == 18 and total_preguntas == 90:
        print("   ✅ Carga correcta")
        return True
    else:
        print("   ❌ Carga incompleta")
        return False


# ============================================================================
# EJECUTAR SI SE LLAMA DIRECTAMENTE
# ============================================================================

if __name__ == "__main__":
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from models_competencias import Base
    
    # Configurar BD (cambiar según tu DB)
    DATABASE_URL = "sqlite:///./cenerh_recruit_os.db"  # SQLite para testing
    engine = create_engine(DATABASE_URL, echo=False)
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Cargar
    cargar_competencias(session)
    verificar_carga(session)

