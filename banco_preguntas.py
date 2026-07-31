"""
banco_preguntas.py - Contenido real del banco de tests (Fase 1)

Preguntas para los tests que antes solo tenían 1 pregunta de muestra
(verbal, numérico, big_five, ie, motivación, valores, liderazgo),
el test de Atención completo (40 preguntas, verificadas matemáticamente),
los 5 tests de "Roles Estratégicos", y los 5 escenarios de Assessment
Center evaluados por IA.

Contenido redactado como placeholder real (no genérico) para completar
el MVP; la dueña de la plataforma puede revisar/ajustar cada pregunta
con su criterio de psicóloga industrial.
"""

# ============================================================================
# VERBAL (20 preguntas, opción múltiple)
# ============================================================================
VERBAL = [
    {"pregunta": "¿Cuál es el significado de 'perspicaz'?", "opciones": {"A": "De vista penetrante", "B": "Que falta de visión", "C": "Corto de vista", "D": "Ciego"}, "correcta": "A"},
    {"pregunta": "¿Cuál es el sinónimo de 'efímero'?", "opciones": {"A": "Duradero", "B": "Pasajero", "C": "Sólido", "D": "Extenso"}, "correcta": "B"},
    {"pregunta": "¿Cuál es el antónimo de 'escaso'?", "opciones": {"A": "Limitado", "B": "Reducido", "C": "Abundante", "D": "Mínimo"}, "correcta": "C"},
    {"pregunta": "Médico es a hospital como maestro es a ___", "opciones": {"A": "Alumno", "B": "Libro", "C": "Pizarra", "D": "Escuela"}, "correcta": "D"},
    {"pregunta": "¿Cuál es el significado de 'meticuloso'?", "opciones": {"A": "Minucioso", "B": "Descuidado", "C": "Apresurado", "D": "Confuso"}, "correcta": "A"},
    {"pregunta": "¿Cuál es el antónimo de 'locuaz'?", "opciones": {"A": "Hablador", "B": "Callado", "C": "Simpático", "D": "Extrovertido"}, "correcta": "B"},
    {"pregunta": "Llave es a puerta como contraseña es a ___", "opciones": {"A": "Sistema", "B": "Computadora", "C": "Acceso", "D": "Usuario"}, "correcta": "C"},
    {"pregunta": "¿Cuál es el sinónimo de 'pragmático'?", "opciones": {"A": "Idealista", "B": "Teórico", "C": "Confuso", "D": "Práctico"}, "correcta": "D"},
    {"pregunta": "¿Cuál es el significado de 'ambiguo'?", "opciones": {"A": "Impreciso", "B": "Claro", "C": "Directo", "D": "Evidente"}, "correcta": "A"},
    {"pregunta": "Autor es a libro como compositor es a ___", "opciones": {"A": "Partitura", "B": "Canción", "C": "Instrumento", "D": "Orquesta"}, "correcta": "B"},
    {"pregunta": "¿Cuál es el antónimo de 'cauteloso'?", "opciones": {"A": "Prudente", "B": "Cuidadoso", "C": "Imprudente", "D": "Reservado"}, "correcta": "C"},
    {"pregunta": "¿Cuál es el sinónimo de 'resiliente'?", "opciones": {"A": "Frágil", "B": "Vulnerable", "C": "Débil", "D": "Resistente"}, "correcta": "D"},
    {"pregunta": "¿Cuál es el significado de 'empatía'?", "opciones": {"A": "Comprensión de sentimientos ajenos", "B": "Indiferencia", "C": "Rechazo", "D": "Desconfianza"}, "correcta": "A"},
    {"pregunta": "Termómetro es a temperatura como balanza es a ___", "opciones": {"A": "Tiempo", "B": "Peso", "C": "Distancia", "D": "Volumen"}, "correcta": "B"},
    {"pregunta": "¿Cuál es el antónimo de 'conciso'?", "opciones": {"A": "Breve", "B": "Claro", "C": "Extenso", "D": "Directo"}, "correcta": "C"},
    {"pregunta": "¿Cuál es el sinónimo de 'diligente'?", "opciones": {"A": "Perezoso", "B": "Distraído", "C": "Lento", "D": "Aplicado"}, "correcta": "D"},
    {"pregunta": "¿Cuál es el significado de 'subjetivo'?", "opciones": {"A": "Basado en opiniones personales", "B": "Basado en hechos", "C": "Neutral", "D": "Comprobable"}, "correcta": "A"},
    {"pregunta": "Piloto es a avión como capitán es a ___", "opciones": {"A": "Tripulación", "B": "Barco", "C": "Puerto", "D": "Mar"}, "correcta": "B"},
    {"pregunta": "¿Cuál es el antónimo de 'flexible'?", "opciones": {"A": "Adaptable", "B": "Versátil", "C": "Rígido", "D": "Moldeable"}, "correcta": "C"},
    {"pregunta": "¿Cuál es el sinónimo de 'innovador'?", "opciones": {"A": "Tradicional", "B": "Conservador", "C": "Rutinario", "D": "Creativo"}, "correcta": "D"},
]

# ============================================================================
# NUMÉRICO (40 preguntas, opción múltiple) - verificadas aritméticamente
# ============================================================================
NUMERICO = [
    {"pregunta": "Si 230 unidades producen 20% de merma, ¿cuál es la pérdida?", "opciones": {"A": "46", "B": "23", "C": "52", "D": "69"}, "correcta": "A"},
    {"pregunta": "¿Cuál es el 15% de 800?", "opciones": {"A": "100", "B": "120", "C": "140", "D": "80"}, "correcta": "B"},
    {"pregunta": "Un producto cuesta $250 con 10% de descuento. ¿Precio final?", "opciones": {"A": "200", "B": "240", "C": "225", "D": "210"}, "correcta": "C"},
    {"pregunta": "Serie: 3, 6, 9, 12, __. ¿Siguiente número?", "opciones": {"A": "14", "B": "16", "C": "18", "D": "15"}, "correcta": "D"},
    {"pregunta": "Serie: 2, 4, 8, 16, __. ¿Siguiente número?", "opciones": {"A": "32", "B": "24", "C": "30", "D": "36"}, "correcta": "A"},
    {"pregunta": "Si x + 5 = 12, ¿cuánto vale x?", "opciones": {"A": "5", "B": "7", "C": "6", "D": "8"}, "correcta": "B"},
    {"pregunta": "Si 3x = 21, ¿cuánto vale x?", "opciones": {"A": "6", "B": "8", "C": "7", "D": "9"}, "correcta": "C"},
    {"pregunta": "Un empleado gana $30,000 mensuales y recibe un aumento del 8%. ¿Nuevo salario?", "opciones": {"A": "31,000", "B": "32,000", "C": "33,000", "D": "32,400"}, "correcta": "D"},
    {"pregunta": "Un artículo cuesta $500 y se vende con 25% de ganancia. ¿Precio de venta?", "opciones": {"A": "625", "B": "600", "C": "650", "D": "700"}, "correcta": "A"},
    {"pregunta": "¿Cuál es el 40% de 250?", "opciones": {"A": "80", "B": "100", "C": "90", "D": "110"}, "correcta": "B"},
    {"pregunta": "Un tanque se llena en 6 horas con una llave. ¿Qué fracción se llena en 2 horas?", "opciones": {"A": "1/2", "B": "1/4", "C": "1/3", "D": "2/3"}, "correcta": "C"},
    {"pregunta": "5 trabajadores hacen un trabajo en 10 días. ¿Cuántos días tardarían 10 trabajadores (misma tasa)?", "opciones": {"A": "20", "B": "10", "C": "15", "D": "5"}, "correcta": "D"},
    {"pregunta": "Serie: 1, 4, 9, 16, __. ¿Siguiente número?", "opciones": {"A": "25", "B": "20", "C": "23", "D": "30"}, "correcta": "A"},
    {"pregunta": "¿A qué porcentaje equivale 3/4?", "opciones": {"A": "65%", "B": "75%", "C": "70%", "D": "80%"}, "correcta": "B"},
    {"pregunta": "Un préstamo de $200,000 tiene 12% de interés anual. ¿Interés en 1 año?", "opciones": {"A": "20,000", "B": "22,000", "C": "24,000", "D": "26,000"}, "correcta": "C"},
    {"pregunta": "¿Cuál es el promedio de 8, 10 y 12?", "opciones": {"A": "9", "B": "11", "C": "12", "D": "10"}, "correcta": "D"},
    {"pregunta": "Un carro recorre 60km en 1.5 horas. ¿Velocidad promedio?", "opciones": {"A": "40 km/h", "B": "35 km/h", "C": "45 km/h", "D": "50 km/h"}, "correcta": "A"},
    {"pregunta": "¿Cuánto es 7 x 8 - 15?", "opciones": {"A": "36", "B": "41", "C": "46", "D": "51"}, "correcta": "B"},
    {"pregunta": "El 25% de un número es 50. ¿Cuál es el número?", "opciones": {"A": "150", "B": "175", "C": "200", "D": "225"}, "correcta": "C"},
    {"pregunta": "Serie: 5, 10, 20, 40, __. ¿Siguiente número?", "opciones": {"A": "60", "B": "70", "C": "90", "D": "80"}, "correcta": "D"},
    {"pregunta": "Un empleado trabaja 8 horas diarias, 5 días a la semana. ¿Horas en 4 semanas?", "opciones": {"A": "160", "B": "140", "C": "150", "D": "170"}, "correcta": "A"},
    {"pregunta": "2 productos cuestan $180 en total; uno cuesta el doble del otro. ¿Cuánto cuesta el más barato?", "opciones": {"A": "50", "B": "60", "C": "70", "D": "80"}, "correcta": "B"},
    {"pregunta": "¿Cuál es la raíz cuadrada de 144?", "opciones": {"A": "10", "B": "11", "C": "12", "D": "14"}, "correcta": "C"},
    {"pregunta": "Una empresa reduce su personal de 50 a 40 empleados. ¿Qué porcentaje de reducción?", "opciones": {"A": "10%", "B": "15%", "C": "25%", "D": "20%"}, "correcta": "D"},
    {"pregunta": "Serie: 2, 3, 5, 8, 13, __. ¿Siguiente número?", "opciones": {"A": "21", "B": "18", "C": "20", "D": "24"}, "correcta": "A"},
    {"pregunta": "Compras 3 artículos a $45 cada uno con 10% de descuento total. ¿Cuánto pagas?", "opciones": {"A": "110", "B": "121.5", "C": "130", "D": "135"}, "correcta": "B"},
    {"pregunta": "Un depósito bancario de $50,000 genera 6% de interés anual. ¿Interés generado?", "opciones": {"A": "2,500", "B": "3,500", "C": "3,000", "D": "4,000"}, "correcta": "C"},
    {"pregunta": "¿Cuánto es 120 ÷ 4 + 15?", "opciones": {"A": "35", "B": "40", "C": "50", "D": "45"}, "correcta": "D"},
    {"pregunta": "La razón entre A y B es 3:5 y A=15. ¿Cuánto es B?", "opciones": {"A": "25", "B": "20", "C": "22", "D": "28"}, "correcta": "A"},
    {"pregunta": "Serie: 81, 27, 9, 3, __. ¿Siguiente número?", "opciones": {"A": "0", "B": "1", "C": "2", "D": "3"}, "correcta": "B"},
    {"pregunta": "Un vendedor gana 5% de comisión sobre $80,000 en ventas. ¿Cuánto gana?", "opciones": {"A": "3,500", "B": "4,500", "C": "4,000", "D": "5,000"}, "correcta": "C"},
    {"pregunta": "¿Cuál es el doble de la mitad de 60?", "opciones": {"A": "30", "B": "45", "C": "90", "D": "60"}, "correcta": "D"},
    {"pregunta": "Un producto aumenta de $80 a $100. ¿Porcentaje de aumento?", "opciones": {"A": "25%", "B": "20%", "C": "30%", "D": "35%"}, "correcta": "A"},
    {"pregunta": "Un equipo de 6 personas completa una tarea en 12 horas. ¿Cuántas horas tardarían 3 personas?", "opciones": {"A": "18", "B": "24", "C": "20", "D": "22"}, "correcta": "B"},
    {"pregunta": "Serie: 1, 1, 2, 3, 5, 8, __. ¿Siguiente número?", "opciones": {"A": "11", "B": "12", "C": "13", "D": "14"}, "correcta": "C"},
    {"pregunta": "El precio de un producto con IVA (18%) es $118. ¿Precio sin IVA?", "opciones": {"A": "90", "B": "95", "C": "105", "D": "100"}, "correcta": "D"},
    {"pregunta": "¿Cuánto es 9² - 4²?", "opciones": {"A": "65", "B": "55", "C": "60", "D": "70"}, "correcta": "A"},
    {"pregunta": "Una fábrica produce 500 unidades en 8 horas. ¿Cuántas produce en 1 hora?", "opciones": {"A": "55", "B": "62.5", "C": "60", "D": "65"}, "correcta": "B"},
    {"pregunta": "Inviertes $100,000 y obtienes 15% de retorno. ¿Cuál es tu ganancia?", "opciones": {"A": "10,000", "B": "12,000", "C": "15,000", "D": "18,000"}, "correcta": "C"},
    {"pregunta": "Serie: 4, 9, 16, 25, __. ¿Siguiente número?", "opciones": {"A": "30", "B": "32", "C": "34", "D": "36"}, "correcta": "D"},
]

LIKERT_OPCIONES = {"1": "Totalmente en desacuerdo", "2": "En desacuerdo", "3": "Neutral", "4": "De acuerdo", "5": "Totalmente de acuerdo"}
LIKERT_OPCIONES_FRECUENCIA = {"1": "Nunca", "2": "Raramente", "3": "A veces", "4": "Frecuentemente", "5": "Siempre"}

# ============================================================================
# BIG FIVE (20 preguntas, Likert) - 4 items x 5 factores
# ============================================================================
BIG_FIVE = [
    "Me gusta explorar ideas y conceptos nuevos.",
    "Disfruto de actividades creativas y artísticas.",
    "Me adapto con facilidad a situaciones novedosas.",
    "Prefiero probar métodos diferentes en vez de seguir siempre la misma rutina.",
    "Me considero una persona organizada y responsable con mis tareas.",
    "Planifico mis tareas con anticipación.",
    "Soy detallista en la ejecución de mi trabajo.",
    "Persisto en una tarea hasta completarla, incluso si es tediosa.",
    "Me siento cómodo iniciando conversaciones con personas desconocidas.",
    "Disfruto trabajar en equipo y en ambientes sociales.",
    "Prefiero actividades grupales sobre el trabajo en solitario.",
    "Me energizo al interactuar con otras personas.",
    "Considero los sentimientos de los demás antes de actuar.",
    "Coopero fácilmente con mis compañeros de trabajo.",
    "Confío en las intenciones de las personas con las que trabajo.",
    "Evito conflictos innecesarios y busco el consenso.",
    "Mantengo la calma incluso bajo presión.",
    "No me afectan fácilmente las críticas.",
    "Puedo controlar mis emociones en situaciones estresantes.",
    "Me recupero rápidamente después de un contratiempo.",
]

# ============================================================================
# INTELIGENCIA EMOCIONAL (20 preguntas, Likert)
# ============================================================================
IE = [
    "Puedo reconocer mis emociones mientras las estoy experimentando",
    "Identifico rápidamente cuando una situación me genera estrés.",
    "Puedo nombrar con precisión lo que siento en un momento dado.",
    "Entiendo cómo mis emociones afectan mi desempeño laboral.",
    "Reconozco las emociones de los demás a través de su lenguaje corporal.",
    "Puedo mantener la calma en situaciones de conflicto.",
    "Controlo mis impulsos incluso cuando estoy frustrado.",
    "No dejo que mis emociones negativas afecten mis decisiones importantes.",
    "Me adapto emocionalmente cuando los planes cambian de repente.",
    "Puedo motivarme a mí mismo incluso ante el fracaso.",
    "Muestro empatía genuina hacia los problemas de mis compañeros.",
    "Escucho activamente antes de responder emocionalmente.",
    "Puedo dar retroalimentación difícil sin generar conflicto.",
    "Reconozco cuando otra persona necesita apoyo emocional.",
    "Manejo bien las críticas constructivas.",
    "Puedo negociar manteniendo una relación positiva con la otra parte.",
    "Inspiro confianza en las personas con las que trabajo.",
    "Sé cuándo es el momento adecuado para expresar mi opinión.",
    "Mantengo relaciones laborales saludables a largo plazo.",
    "Reconozco mis propias limitaciones emocionales y busco ayuda si la necesito.",
]

# ============================================================================
# MOTIVACIÓN LABORAL (20 preguntas, Likert)
# ============================================================================
MOTIVACION = [
    "Me siento motivado cuando tengo metas claras y desafiantes en mi trabajo",
    "El reconocimiento por mi trabajo es importante para mantenerme motivado.",
    "Disfruto asumir nuevas responsabilidades en mi puesto.",
    "Me esfuerzo más cuando veo una oportunidad de crecimiento profesional.",
    "La estabilidad laboral es un factor clave en mi motivación.",
    "Me motiva trabajar en proyectos que tengan impacto visible.",
    "El salario es un factor determinante en mi desempeño.",
    "Prefiero trabajos con autonomía para tomar mis propias decisiones.",
    "Me motiva aprender nuevas habilidades constantemente.",
    "El ambiente de trabajo influye directamente en mi productividad.",
    "Me siento motivado cuando mi trabajo tiene un propósito claro.",
    "Busco activamente oportunidades para destacar en mi equipo.",
    "La posibilidad de ascenso es importante para mi compromiso laboral.",
    "Me motiva competir conmigo mismo por mejorar resultados.",
    "Valoro el feedback constante de mis superiores.",
    "Me comprometo más cuando participo en la toma de decisiones.",
    "El trabajo en equipo aumenta mi motivación diaria.",
    "Prefiero metas a largo plazo sobre recompensas inmediatas.",
    "Me motiva contribuir al éxito general de la organización.",
    "Mantengo mi motivación incluso en tareas rutinarias.",
]

# ============================================================================
# VALORES ORGANIZACIONALES (20 preguntas, Likert)
# ============================================================================
VALORES = [
    "La honestidad y la transparencia son fundamentales en cualquier equipo de trabajo",
    "El respeto mutuo es esencial para un buen ambiente laboral.",
    "La responsabilidad social empresarial debe ser prioridad de toda organización.",
    "La ética debe prevalecer incluso sobre los resultados financieros.",
    "Valoro la igualdad de oportunidades dentro de una empresa.",
    "La colaboración es más importante que la competencia interna.",
    "Las decisiones empresariales deben considerar el impacto ambiental.",
    "La diversidad en el equipo enriquece los resultados del trabajo.",
    "El cumplimiento de normas y políticas es innegociable.",
    "La confianza entre colegas es la base de un buen equipo.",
    "Prefiero trabajar en empresas con una misión clara y significativa.",
    "La calidad del trabajo debe primar sobre la velocidad de entrega.",
    "Los líderes deben predicar con el ejemplo.",
    "El equilibrio entre vida personal y laboral es un valor importante.",
    "La innovación debe fomentarse aunque implique riesgos.",
    "La lealtad hacia la empresa se gana, no se exige.",
    "Es importante que la empresa invierta en el desarrollo de su personal.",
    "La comunicación abierta previene la mayoría de los conflictos laborales.",
    "Las decisiones deben tomarse considerando a todos los involucrados.",
    "Valoro trabajar donde se reconozca el esfuerzo individual y colectivo.",
]

# ============================================================================
# POTENCIAL DE LIDERAZGO (20 preguntas, Likert)
# ============================================================================
LIDERAZGO = [
    "Me resulta natural guiar a otros y tomar decisiones en situaciones de presión",
    "Puedo delegar tareas de manera efectiva sin perder el control del resultado.",
    "Inspiro confianza en las personas que dependen de mí.",
    "Tomo decisiones difíciles incluso cuando no son populares.",
    "Sé comunicar una visión clara a mi equipo.",
    "Asumo la responsabilidad de los errores de mi equipo, no solo los míos.",
    "Escucho las opiniones de mi equipo antes de decidir.",
    "Motivo a otros a dar su mejor esfuerzo incluso en momentos difíciles.",
    "Identifico el potencial de las personas y las ayudo a desarrollarlo.",
    "Mantengo la calma y el enfoque en situaciones de crisis.",
    "Puedo mediar conflictos entre miembros de mi equipo.",
    "Doy retroalimentación honesta y constructiva regularmente.",
    "Adapto mi estilo de liderazgo según la situación y las personas.",
    "Fomento la autonomía y la iniciativa en mi equipo.",
    "Reconozco públicamente los logros de mi equipo.",
    "Tomo la iniciativa cuando nadie más lo hace.",
    "Puedo influir en otros sin necesidad de autoridad formal.",
    "Establezco metas claras y realistas para mi equipo.",
    "Aprendo de mis errores como líder y ajusto mi enfoque.",
    "Me proyecto a largo plazo, no solo en resultados inmediatos.",
]

# ============================================================================
# ROLES ESTRATÉGICOS (5 tests x 10 preguntas, Likert)
# ============================================================================
ROLES_ESTRATEGICOS = {
    "rol_supervision": {
        "nombre": "Capacidad de Supervisión",
        "descripcion": "Mide delegación, control de calidad y gestión de equipos operativos",
        "preguntas": [
            "Delego tareas considerando las fortalezas de cada miembro del equipo.",
            "Superviso el trabajo de otros sin caer en el micromanagement.",
            "Establezco controles de calidad claros para el trabajo de mi equipo.",
            "Doy seguimiento constante al progreso de las tareas asignadas.",
            "Actúo con rapidez cuando detecto un problema en el desempeño de alguien.",
            "Rindo cuentas por los resultados de las personas que superviso.",
            "Resuelvo conflictos entre subordinados de manera justa.",
            "Motivo a mi equipo incluso cuando los resultados no son los esperados.",
            "Tomo decisiones rápidas y firmes cuando la situación lo requiere.",
            "Reviso mis propias decisiones cuando nueva información lo amerita.",
        ],
    },
    "rol_liderazgo_ejecutivo": {
        "nombre": "Liderazgo Ejecutivo - Influencia y Gestión de Crisis",
        "descripcion": "Mide visión, comunicación e influencia en roles de liderazgo senior",
        "preguntas": [
            "Inspiro a otros a comprometerse con una visión de largo plazo.",
            "Comunico con claridad hacia dónde va la organización o el equipo.",
            "Genero credibilidad y confianza incluso en momentos de incertidumbre.",
            "Tomo el control cuando una crisis afecta a mi equipo u organización.",
            "Mantengo la calma y transmito seguridad durante una crisis.",
            "Comunico decisiones difíciles de forma clara y respetuosa.",
            "Anticipo problemas antes de que se conviertan en crisis.",
            "Construyo consenso entre personas con intereses distintos.",
            "Actúo con integridad incluso cuando nadie está observando.",
            "Aprendo de las crisis pasadas para prevenir futuras.",
        ],
    },
    "rol_ventas": {
        "nombre": "Mentalidad Comercial y Cierre de Ventas",
        "descripcion": "Mide impulso comercial, manejo de objeciones y orientación a resultados",
        "preguntas": [
            "Me siento cómodo iniciando contacto con clientes potenciales desconocidos.",
            "Persisto en el seguimiento de una venta incluso después de un rechazo inicial.",
            "Identifico las necesidades reales del cliente antes de ofrecer una solución.",
            "Manejo objeciones de precio sin ceder innecesariamente en el valor ofrecido.",
            "Cierro ventas preguntando directamente por el compromiso del cliente.",
            "Construyo relaciones de largo plazo más que buscar ventas únicas.",
            "Me motiva superar mis propias metas de ventas anteriores.",
            "Investigo a fondo al cliente y su industria antes de una reunión importante.",
            "Mantengo el seguimiento post-venta para asegurar la satisfacción del cliente.",
            "Convierto el rechazo en una oportunidad de aprendizaje, no de desmotivación.",
        ],
    },
    "rol_mercadeo": {
        "nombre": "Pensamiento Estratégico de Mercadeo",
        "descripcion": "Mide análisis de mercado, creatividad y ejecución de campañas",
        "preguntas": [
            "Analizo tendencias de mercado antes de proponer una estrategia.",
            "Identifico oportunidades de diferenciación frente a la competencia.",
            "Genero ideas creativas para posicionar una marca o producto.",
            "Mido los resultados de una campaña para ajustar la estrategia.",
            "Traduzco datos de mercado en decisiones prácticas y accionables.",
            "Pienso en el cliente final al diseñar cualquier estrategia de comunicación.",
            "Colaboro con otras áreas para ejecutar una campaña de forma integral.",
            "Anticipo cambios en las preferencias del consumidor.",
            "Equilibro creatividad con objetivos comerciales concretos.",
            "Ajusto rápidamente una estrategia cuando los resultados no son los esperados.",
        ],
    },
    "rol_desarrollo_negocios": {
        "nombre": "Visión de Desarrollo de Negocios",
        "descripcion": "Mide identificación de oportunidades, networking y visión de crecimiento",
        "preguntas": [
            "Identifico oportunidades de crecimiento antes que la competencia.",
            "Construyo relaciones estratégicas (networking) de forma proactiva.",
            "Pienso en la escalabilidad de una idea antes de implementarla.",
            "Evalúo riesgos calculados antes de tomar una decisión de negocio.",
            "Diseño planes de crecimiento realistas basados en datos del mercado.",
            "Negocio acuerdos que beneficien a ambas partes a largo plazo.",
            "Identifico nuevos mercados o segmentos no explorados.",
            "Tomo la iniciativa para proponer nuevas líneas de negocio.",
            "Persisto en el desarrollo de una oportunidad de negocio pese a obstáculos iniciales.",
            "Evalúo el retorno de inversión antes de comprometer recursos.",
        ],
    },
}

# ============================================================================
# ASSESSMENT CENTERS (5, uno por rol estratégico) - evaluados por IA
# ============================================================================
ASSESSMENT_CENTERS = {
    "Supervisión": {
        "nombre": "Simulación: Conflicto de Desempeño en el Equipo",
        "descripcion": "Evalúa cómo el candidato aborda un problema de desempeño de un supervisado",
        "escenario": (
            "Uno de tus supervisados ha llegado tarde 3 veces esta semana y su desempeño "
            "ha bajado notablemente. Tienes una reunión con él en 10 minutos. Describe cómo "
            "abordarías esta conversación y qué acciones tomarías después."
        ),
        "rubrica": {
            "criterios": [
                {"nombre": "Empatía", "descripcion": "Considera el contexto/causas antes de juzgar", "peso": 0.25},
                {"nombre": "Firmeza", "descripcion": "Establece expectativas claras y consecuencias", "peso": 0.25},
                {"nombre": "Plan de acción", "descripcion": "Propone pasos concretos de seguimiento", "peso": 0.25},
                {"nombre": "Comunicación", "descripcion": "Tono profesional, claro y respetuoso", "peso": 0.25},
            ]
        },
    },
    "Liderazgo": {
        "nombre": "Caso: Empresa en Crisis de Entrega",
        "descripcion": "Evalúa gestión de crisis, transparencia y capacidad de recuperación",
        "escenario": (
            "Tu equipo enfrenta una crisis: un proyecto clave se retrasará 2 semanas y el "
            "cliente ya fue notificado erróneamente de que estaría a tiempo. Describe cómo "
            "comunicarías esta situación a tu equipo y al cliente, y qué harías en las "
            "próximas 48 horas."
        ),
        "rubrica": {
            "criterios": [
                {"nombre": "Gestión de crisis", "descripcion": "Prioriza acciones bajo presión", "peso": 0.30},
                {"nombre": "Transparencia", "descripcion": "Comunica la situación real sin minimizarla ni exagerarla", "peso": 0.25},
                {"nombre": "Responsabilidad", "descripcion": "Asume su rol en la solución, no solo culpa a otros", "peso": 0.25},
                {"nombre": "Plan de recuperación", "descripcion": "Propone pasos concretos para mitigar el daño", "peso": 0.20},
            ]
        },
    },
    "Ventas": {
        "nombre": "Role-play: Objeción de Precio",
        "descripcion": "Evalúa manejo de objeciones, escucha activa y cierre",
        "escenario": (
            "Un cliente potencial te dice que el producto de tu competidor es 20% más "
            "barato y que probablemente elegirá esa opción. Describe cómo responderías en "
            "ese momento para intentar cerrar la venta."
        ),
        "rubrica": {
            "criterios": [
                {"nombre": "Manejo de objeciones", "descripcion": "No compite solo por precio, resalta valor diferencial", "peso": 0.30},
                {"nombre": "Escucha activa", "descripcion": "Indaga las verdaderas prioridades del cliente", "peso": 0.25},
                {"nombre": "Cierre", "descripcion": "Propone un siguiente paso concreto", "peso": 0.25},
                {"nombre": "Profesionalismo", "descripcion": "Mantiene una actitud respetuosa hacia el competidor y el cliente", "peso": 0.20},
            ]
        },
    },
    "Mercadeo": {
        "nombre": "Caso: Campaña con Presupuesto Reducido",
        "descripcion": "Evalúa creatividad, priorización y pensamiento estratégico",
        "escenario": (
            "Te asignan lanzar una campaña de marketing para un producto nuevo con un "
            "presupuesto reducido a la mitad de lo esperado. Describe tu estrategia para "
            "maximizar el impacto con este presupuesto limitado."
        ),
        "rubrica": {
            "criterios": [
                {"nombre": "Creatividad", "descripcion": "Propone soluciones no convencionales", "peso": 0.25},
                {"nombre": "Priorización", "descripcion": "Enfoca el presupuesto en los canales de mayor impacto", "peso": 0.25},
                {"nombre": "Orientación a resultados", "descripcion": "Define cómo mediría el éxito de la campaña", "peso": 0.25},
                {"nombre": "Pensamiento estratégico", "descripcion": "Conecta la campaña con los objetivos de negocio", "peso": 0.25},
            ]
        },
    },
    "Desarrollo de Negocios": {
        "nombre": "Caso: Defender una Oportunidad de Expansión",
        "descripcion": "Evalúa visión estratégica, manejo de datos y persuasión",
        "escenario": (
            "Identificaste una oportunidad de expandir el negocio a un nuevo segmento de "
            "mercado, pero la dirección es escéptica por falta de datos. Describe cómo "
            "presentarías y defenderías esta oportunidad."
        ),
        "rubrica": {
            "criterios": [
                {"nombre": "Visión estratégica", "descripcion": "Articula el potencial de crecimiento con claridad", "peso": 0.25},
                {"nombre": "Manejo de datos", "descripcion": "Propone cómo validar la oportunidad con evidencia", "peso": 0.25},
                {"nombre": "Persuasión", "descripcion": "Construye un argumento convincente para audiencias escépticas", "peso": 0.25},
                {"nombre": "Gestión de riesgo", "descripcion": "Reconoce riesgos y cómo mitigarlos", "peso": 0.25},
            ]
        },
    },
}


def _likert_preguntas(textos, opciones=None):
    opciones = opciones or LIKERT_OPCIONES
    return [
        {
            "numero": i + 1,
            "pregunta": texto,
            "tipo_respuesta": "likert",
            "opciones": opciones,
            "respuesta_correcta": "N/A",
            "dificultad": "media",
        }
        for i, texto in enumerate(textos)
    ]


def _mc_preguntas(items):
    return [
        {
            "numero": i + 1,
            "pregunta": item["pregunta"],
            "tipo_respuesta": "multiple_choice",
            "opciones": item["opciones"],
            "respuesta_correcta": item["correcta"],
            "dificultad": "media",
        }
        for i, item in enumerate(items)
    ]


# ============================================================================
# ATENCIÓN Y CONCENTRACIÓN (40 preguntas, opción múltiple)
#
# Contenido base: Test_Atencion_40_Preguntas_OFICIAL.txt
# La "clave de respuestas" original en ANALISIS_TEST_ATENCION_40_PREGUNTAS.md
# tenía 12 errores verificables (aritmética/lógica que no correspondía a las
# opciones reales de cada pregunta) — las respuestas aquí fueron recalculadas
# y verificadas una por una contra el enunciado real de cada pregunta.
# ============================================================================
ATENCION = [
    # Subtest A: Cancelación visual (Q1-10) - contar 'pq' en la secuencia
    {"pregunta": "En la siguiente secuencia, ¿cuántas veces la letra 'q' está inmediatamente precedida por una 'p'? Secuencia: ddbpqqbbpqdpppqqqdbdpdpbpbpqppqbpbb", "opciones": {"A": "2", "B": "6", "C": "5", "D": "4"}, "correcta": "C"},
    {"pregunta": "En la siguiente secuencia, ¿cuántas veces la letra 'q' está inmediatamente precedida por una 'p'? Secuencia: qbdbppbdbbbddqdpdbdpqbdpdqpqqpbdbdq", "opciones": {"A": "4", "B": "1", "C": "3", "D": "2"}, "correcta": "D"},
    {"pregunta": "En la siguiente secuencia, ¿cuántas veces la letra 'q' está inmediatamente precedida por una 'p'? Secuencia: qqdbbqpbppbpppqdbdbdpbppdqpddpbdbqp", "opciones": {"A": "4", "B": "1", "C": "3", "D": "2"}, "correcta": "B"},
    {"pregunta": "En la siguiente secuencia, ¿cuántas veces la letra 'q' está inmediatamente precedida por una 'p'? Secuencia: ppdpppqbbqpqpbdbbqpddqbdbddqqqddbqb", "opciones": {"A": "5", "B": "2", "C": "4", "D": "3"}, "correcta": "B"},
    {"pregunta": "En la siguiente secuencia, ¿cuántas veces la letra 'q' está inmediatamente precedida por una 'p'? Secuencia: qppqdpdqbdqbpqqbbdqdbdpbpbdbqbppdbd", "opciones": {"A": "4", "B": "1", "C": "3", "D": "2"}, "correcta": "D"},
    {"pregunta": "En la siguiente secuencia, ¿cuántas veces la letra 'q' está inmediatamente precedida por una 'p'? Secuencia: ppbddpbpbdbpdqbppqbdbpqdqppbqpqpdbq", "opciones": {"A": "3", "B": "5", "C": "6", "D": "4"}, "correcta": "A"},
    {"pregunta": "En la siguiente secuencia, ¿cuántas veces la letra 'q' está inmediatamente precedida por una 'p'? Secuencia: bpbdpppdqdqqbbpdqdbpdqqddpqpddbpbpq", "opciones": {"A": "2", "B": "5", "C": "3", "D": "4"}, "correcta": "A"},
    {"pregunta": "En la siguiente secuencia, ¿cuántas veces la letra 'q' está inmediatamente precedida por una 'p'? Secuencia: dqdqpbdpqpqppqpqdppdbbpqbdpbdqpdqdq", "opciones": {"A": "5", "B": "3", "C": "6", "D": "4"}, "correcta": "A"},
    {"pregunta": "En la siguiente secuencia, ¿cuántas veces la letra 'q' está inmediatamente precedida por una 'p'? Secuencia: bqpqbqqpqbdqpqbqqpqppbqpqpbpddqqbdd", "opciones": {"A": "5", "B": "6", "C": "8", "D": "9"}, "correcta": "A"},
    {"pregunta": "En la siguiente secuencia, ¿cuántas veces la letra 'q' está inmediatamente precedida por una 'p'? Secuencia: dbdbqqdqppqqqbqbqpbddqdpqdpppdddbqq", "opciones": {"A": "3", "B": "0", "C": "2", "D": "1"}, "correcta": "C"},
    # Subtest B: Percepción de diferencias (Q11-20)
    {"pregunta": "Compare las siguientes dos series alfanuméricas. Si son exactamente IGUALES marque (A), si tienen alguna diferencia marque (B). Serie 1: A78B99C21X | Serie 2: A78B99C21X", "opciones": {"A": "Iguales", "B": "Diferentes"}, "correcta": "A"},
    {"pregunta": "Compare las siguientes dos series alfanuméricas. Si son exactamente IGUALES marque (A), si tienen alguna diferencia marque (B). Serie 1: M45K908L12 | Serie 2: M45K908I12", "opciones": {"A": "Iguales", "B": "Diferentes"}, "correcta": "B"},
    {"pregunta": "Compare las siguientes dos series alfanuméricas. Si son exactamente IGUALES marque (A), si tienen alguna diferencia marque (B). Serie 1: 8899001122 | Serie 2: 8899001122", "opciones": {"A": "Iguales", "B": "Diferentes"}, "correcta": "A"},
    {"pregunta": "Compare las siguientes dos series alfanuméricas. Si son exactamente IGUALES marque (A), si tienen alguna diferencia marque (B). Serie 1: ZXCVBNM123 | Serie 2: ZXCVBMN123", "opciones": {"A": "Iguales", "B": "Diferentes"}, "correcta": "B"},
    {"pregunta": "Compare las siguientes dos series alfanuméricas. Si son exactamente IGUALES marque (A), si tienen alguna diferencia marque (B). Serie 1: QWERT12345 | Serie 2: QWERT12345", "opciones": {"A": "Iguales", "B": "Diferentes"}, "correcta": "A"},
    {"pregunta": "Compare las siguientes dos series alfanuméricas. Si son exactamente IGUALES marque (A), si tienen alguna diferencia marque (B). Serie 1: 1A2B3C4D5E | Serie 2: 1A2B3C4D5F", "opciones": {"A": "Iguales", "B": "Diferentes"}, "correcta": "B"},
    {"pregunta": "Compare las siguientes dos series alfanuméricas. Si son exactamente IGUALES marque (A), si tienen alguna diferencia marque (B). Serie 1: 9988776655 | Serie 2: 9988776655", "opciones": {"A": "Iguales", "B": "Diferentes"}, "correcta": "A"},
    {"pregunta": "Compare las siguientes dos series alfanuméricas. Si son exactamente IGUALES marque (A), si tienen alguna diferencia marque (B). Serie 1: POIUYTREWQ | Serie 2: POIUYTREWQ", "opciones": {"A": "Iguales", "B": "Diferentes"}, "correcta": "A"},
    {"pregunta": "Compare las siguientes dos series alfanuméricas. Si son exactamente IGUALES marque (A), si tienen alguna diferencia marque (B). Serie 1: LMNOP98765 | Serie 2: LMN0P98765", "opciones": {"A": "Iguales", "B": "Diferentes"}, "correcta": "B"},
    {"pregunta": "Compare las siguientes dos series alfanuméricas. Si son exactamente IGUALES marque (A), si tienen alguna diferencia marque (B). Serie 1: 5544332211 | Serie 2: 5544332211", "opciones": {"A": "Iguales", "B": "Diferentes"}, "correcta": "A"},
    # Subtest C: Seguimiento de instrucciones complejas (Q21-30)
    {"pregunta": "Si el número 85 es impar y mayor que 80, marque la opción C. De lo contrario, marque la opción A.", "opciones": {"A": "A", "B": "B", "C": "C", "D": "D"}, "correcta": "C"},
    {"pregunta": "Sume 4 + 7. Si el resultado es menor que 10, marque A. Si es exactamente 11, marque B. Si es mayor, marque C.", "opciones": {"A": "A", "B": "B", "C": "C", "D": "D"}, "correcta": "B"},
    {"pregunta": "Si la palabra 'CANDIDATO' tiene 4 vocales, marque D. Si tiene 5, marque B.", "opciones": {"A": "A", "B": "B", "C": "C", "D": "D"}, "correcta": "D"},
    {"pregunta": "Mire la serie: 2, 4, 6. Si el siguiente número lógico es 8, marque A, a menos que 8 sea impar, en cuyo caso marque C.", "opciones": {"A": "A", "B": "B", "C": "C", "D": "D"}, "correcta": "A"},
    {"pregunta": "Si Punta Cana está en República Dominicana, marque C. Si está en Puerto Rico, marque A.", "opciones": {"A": "A", "B": "B", "C": "C", "D": "D"}, "correcta": "C"},
    {"pregunta": "Multiplique 3 x 4. Si el resultado es par, divídalo entre 2 y marque la opción que contenga esa letra (A=1, B=2, C=3, D=4, E=5, F=6).", "opciones": {"A": "C", "B": "F", "C": "E", "D": "B"}, "correcta": "B"},
    {"pregunta": "Si la letra 'M' está antes que la 'P' en el abecedario y después de la 'J', marque la opción B.", "opciones": {"A": "A", "B": "B", "C": "C", "D": "D"}, "correcta": "B"},
    {"pregunta": "Lea al revés la palabra 'LUZ'. Si termina en 'Z', marque A. Si termina en 'L', marque D.", "opciones": {"A": "A", "B": "B", "C": "C", "D": "D"}, "correcta": "D"},
    {"pregunta": "Si un triángulo tiene 4 lados, marque B. Si un cuadrado tiene 4 ángulos rectos, marque C.", "opciones": {"A": "A", "B": "B", "C": "C", "D": "D"}, "correcta": "C"},
    {"pregunta": "Reste 15 de 30. Si el resultado es divisible entre 5, marque A. Si no lo es, marque D.", "opciones": {"A": "A", "B": "B", "C": "C", "D": "D"}, "correcta": "A"},
    # Subtest D: Búsqueda y clasificación (Q31-40)
    {"pregunta": "Dado el código de inventario 'X-4-Y-7-Z-2', indique la suma de todos los números presentes.", "opciones": {"A": "11", "B": "14", "C": "12", "D": "13"}, "correcta": "D"},
    {"pregunta": "En la palabra 'RECLUTAMIENTO', ¿qué letra ocupa la séptima posición de izquierda a derecha?", "opciones": {"A": "T", "B": "M", "C": "I", "D": "A"}, "correcta": "D"},
    {"pregunta": "Observe la serie: @, #, $, %, @, &, #, $. ¿Cuántas veces se repite el símbolo '@'?", "opciones": {"A": "3", "B": "1", "C": "2", "D": "4"}, "correcta": "C"},
    {"pregunta": "Si a la palabra 'CONSULTORA' le quitamos todas las vocales, ¿cuántas letras quedan?", "opciones": {"A": "7", "B": "8", "C": "5", "D": "6"}, "correcta": "D"},
    {"pregunta": "¿Cuál es la tercera consonante de la palabra 'PSICÓLOGA'?", "opciones": {"A": "S", "B": "P", "C": "L", "D": "C"}, "correcta": "D"},
    {"pregunta": "En el número de expediente '2026-05-99', ¿cuál es el resultado de sumar los primeros cuatro dígitos?", "opciones": {"A": "9", "B": "8", "C": "10", "D": "11"}, "correcta": "C"},
    {"pregunta": "Busque la palabra oculta al unir las primeras letras de: Gato, Elefante, Sapo, Tigre, Iguana, Oso, Nube. ¿Qué palabra se forma?", "opciones": {"A": "GIRASOL", "B": "GRUPOS", "C": "GESTION", "D": "GENESIS"}, "correcta": "C"},
    {"pregunta": "Cuente las vocales cerradas (i, u) en la frase: 'Diseño organizacional y manuales'.", "opciones": {"A": "3", "B": "5", "C": "2", "D": "4"}, "correcta": "D"},
    {"pregunta": "Si agrupamos los números 1, 4, 7, 2, 5, 8 en pares e impares, ¿cuántos números pares hay?", "opciones": {"A": "2", "B": "4", "C": "5", "D": "3"}, "correcta": "D"},
    {"pregunta": "En la cadena 'CENERH2026', si multiplicamos el primer número por el último, el resultado es:", "opciones": {"A": "10", "B": "12", "C": "8", "D": "14"}, "correcta": "B"},
]


# ============================================================================
# BANCOS POR INDUSTRIA (Fase 3) - 15 preguntas c/u, opción múltiple
# Conocimiento técnico/situacional básico del sector, verificado y con
# distribución balanceada de respuestas (A/B/C/D) vía script independiente.
# ============================================================================
INDUSTRIA_SALUD = [
    {"pregunta": "¿Qué significa la sigla EPP en el contexto de bioseguridad?", "opciones": {"A": "Equipo de Protección Personal", "B": "Estándar de Procedimientos de Planta", "C": "Evaluación de Pacientes Prioritarios", "D": "Escala de Presión Postural"}, "correcta": "A"},
    {"pregunta": "Antes de atender a un paciente, el protocolo básico de higiene indica:", "opciones": {"A": "Uso de perfume", "B": "Lavado de manos", "C": "Cambio de uniforme cada semana", "D": "Ninguna acción especial"}, "correcta": "B"},
    {"pregunta": "¿Qué es el 'triage' en un servicio de urgencias?", "opciones": {"A": "El proceso de facturación del paciente", "B": "El registro de historial médico", "C": "La clasificación de pacientes según gravedad", "D": "La limpieza del área de emergencias"}, "correcta": "C"},
    {"pregunta": "La confidencialidad del historial clínico de un paciente está protegida principalmente por:", "opciones": {"A": "La decisión del paciente únicamente", "B": "No existe protección legal", "C": "Solo aplica en hospitales públicos", "D": "El secreto profesional y la normativa de protección de datos de salud"}, "correcta": "D"},
    {"pregunta": "¿Cuál de las siguientes es una buena práctica en el manejo de desechos biológicos?", "opciones": {"A": "Separarlos en contenedores rotulados según tipo de riesgo", "B": "Mezclarlos con la basura común", "C": "Guardarlos indefinidamente", "D": "Quemarlos en cualquier lugar"}, "correcta": "A"},
    {"pregunta": "Cuando un paciente presenta una reacción alérgica inesperada durante un procedimiento, la prioridad inmediata es:", "opciones": {"A": "Continuar el procedimiento como estaba planeado", "B": "Estabilizar al paciente y suspender el procedimiento", "C": "Esperar a que pase sola", "D": "Consultar únicamente por escrito al médico tratante"}, "correcta": "B"},
    {"pregunta": "¿Qué significa 'consentimiento informado' en un contexto clínico?", "opciones": {"A": "El paciente firma sin necesidad de explicación previa", "B": "Es un trámite solo administrativo", "C": "El paciente autoriza un procedimiento tras comprender los riesgos y beneficios explicados", "D": "Solo aplica en cirugías mayores"}, "correcta": "C"},
    {"pregunta": "La esterilización de instrumental médico tiene como objetivo principal:", "opciones": {"A": "Mejorar su apariencia", "B": "Aumentar su vida útil económica", "C": "Facilitar su almacenamiento", "D": "Eliminar microorganismos y prevenir infecciones"}, "correcta": "D"},
    {"pregunta": "Ante un error de medicación detectado a tiempo, el protocolo correcto es:", "opciones": {"A": "Reportarlo según el protocolo de seguridad del paciente y corregirlo", "B": "Ignorarlo si el paciente no lo notó", "C": "Ocultarlo para evitar sanciones", "D": "Solo informar al final del turno"}, "correcta": "A"},
    {"pregunta": "¿Cuál de estas competencias es más crítica para un rol de atención directa al paciente?", "opciones": {"A": "Manejo de hojas de cálculo avanzadas", "B": "Empatía y comunicación clara bajo presión", "C": "Conocimiento de marketing digital", "D": "Habilidades de programación"}, "correcta": "B"},
    {"pregunta": "La 'cadena de frío' es relevante principalmente para:", "opciones": {"A": "El aire acondicionado del hospital", "B": "La refrigeración de alimentos del comedor", "C": "El almacenamiento de vacunas y ciertos medicamentos", "D": "Ningún proceso clínico"}, "correcta": "C"},
    {"pregunta": "Un profesional de la salud detecta que un compañero cometió una negligencia grave. La conducta ética esperada es:", "opciones": {"A": "Callar para no generar conflictos", "B": "Resolverlo por su cuenta sin informar", "C": "Solo comentarlo informalmente", "D": "Reportarlo por los canales correspondientes"}, "correcta": "D"},
    {"pregunta": "¿Qué implica el término 'humanización del cuidado' en salud?", "opciones": {"A": "Priorizar el trato digno, la empatía y las necesidades del paciente como persona", "B": "Automatizar todos los procesos clínicos", "C": "Reducir el tiempo de consulta al mínimo", "D": "Enfocarse solo en indicadores clínicos"}, "correcta": "A"},
    {"pregunta": "Frente a una queja de un paciente sobre el tiempo de espera, la respuesta más profesional es:", "opciones": {"A": "Ignorar la queja", "B": "Escuchar, explicar la situación con empatía y buscar una solución posible", "C": "Discutir con el paciente", "D": "Delegar sin seguimiento"}, "correcta": "B"},
    {"pregunta": "El trabajo en equipo interdisciplinario (médicos, enfermería, administración) es importante porque:", "opciones": {"A": "Es un requisito solo burocrático", "B": "No afecta los resultados clínicos", "C": "Mejora la calidad y seguridad de la atención al paciente", "D": "Solo aplica en hospitales grandes"}, "correcta": "C"},
]

INDUSTRIA_TECNOLOGIA = [
    {"pregunta": "¿Para qué se usa principalmente un sistema de control de versiones como Git?", "opciones": {"A": "Para rastrear cambios en el código y facilitar la colaboración", "B": "Para diseñar interfaces gráficas", "C": "Para comprimir archivos", "D": "Para administrar copias impresas de documentos"}, "correcta": "A"},
    {"pregunta": "¿Qué significa la sigla API?", "opciones": {"A": "Automated Process Integration", "B": "Application Programming Interface", "C": "Advanced Protocol Index", "D": "Application Process Installer"}, "correcta": "B"},
    {"pregunta": "En el ciclo de vida de desarrollo de software (SDLC), la fase de pruebas (testing) tiene como objetivo:", "opciones": {"A": "Escribir la documentación final", "B": "Diseñar el logo del producto", "C": "Detectar errores antes de pasar a producción", "D": "Definir el presupuesto del proyecto"}, "correcta": "C"},
    {"pregunta": "¿Cuál de las siguientes es una buena práctica de seguridad al manejar contraseñas?", "opciones": {"A": "Compartirlas por correo sin cifrar", "B": "Usar la misma contraseña en todos los sistemas", "C": "Escribirlas en notas físicas visibles", "D": "Usar contraseñas únicas y un gestor de contraseñas"}, "correcta": "D"},
    {"pregunta": "¿Qué es un 'bug' en desarrollo de software?", "opciones": {"A": "Un error o falla en el funcionamiento del sistema", "B": "Una nueva funcionalidad planeada", "C": "Un tipo de base de datos", "D": "Un lenguaje de programación"}, "correcta": "A"},
    {"pregunta": "Un cliente reporta que la aplicación se cae de forma intermitente. El primer paso lógico para diagnosticar el problema es:", "opciones": {"A": "Reiniciar el servidor sin investigar más", "B": "Revisar los logs/registros del sistema para identificar el error", "C": "Ignorar el reporte", "D": "Reescribir toda la aplicación desde cero"}, "correcta": "B"},
    {"pregunta": "¿Qué ventaja principal ofrece trabajar con metodologías ágiles (como Scrum)?", "opciones": {"A": "Eliminar toda comunicación con el cliente", "B": "Planificar todo el proyecto sin posibilidad de cambios", "C": "Entregar valor de forma incremental con retroalimentación frecuente", "D": "Evitar el trabajo en equipo"}, "correcta": "C"},
    {"pregunta": "¿Qué es la 'deuda técnica'?", "opciones": {"A": "Un préstamo bancario de la empresa de tecnología", "B": "El presupuesto asignado a hardware", "C": "Un tipo de licencia de software", "D": "El costo futuro de mantenimiento generado por decisiones de código rápidas pero no óptimas"}, "correcta": "D"},
    {"pregunta": "En ciberseguridad, el 'phishing' se refiere a:", "opciones": {"A": "Un intento de engañar a alguien para obtener información sensible mediante mensajes falsos", "B": "Un método de respaldo de datos", "C": "Un lenguaje de programación", "D": "Un protocolo de red seguro"}, "correcta": "A"},
    {"pregunta": "¿Qué práctica ayuda a reducir riesgos al desplegar cambios en producción?", "opciones": {"A": "Desplegar directamente sin pruebas", "B": "Usar entornos de prueba/staging antes de producción", "C": "Desplegar solo los viernes en la tarde", "D": "No hacer respaldos previos"}, "correcta": "B"},
    {"pregunta": "¿Cuál es el propósito principal de una copia de seguridad (backup)?", "opciones": {"A": "Aumentar la velocidad del sistema", "B": "Reducir el tamaño de los archivos", "C": "Poder recuperar información en caso de pérdida o fallo", "D": "Mejorar el diseño visual"}, "correcta": "C"},
    {"pregunta": "Cuando un equipo de desarrollo no logra cumplir una fecha de entrega, la actitud más profesional es:", "opciones": {"A": "Ocultar el atraso hasta el último momento", "B": "Culpar a otros miembros públicamente", "C": "Entregar algo incompleto sin avisar", "D": "Comunicar el atraso con anticipación, explicar las causas y proponer un plan ajustado"}, "correcta": "D"},
    {"pregunta": "¿Qué es la escalabilidad de un sistema?", "opciones": {"A": "Su capacidad de manejar mayor carga o crecimiento sin degradar el rendimiento", "B": "Su tamaño físico en el servidor", "C": "El número de desarrolladores que lo construyeron", "D": "El color de su interfaz"}, "correcta": "A"},
    {"pregunta": "Ante un conflicto de opiniones técnicas dentro del equipo sobre qué solución implementar, lo más recomendable es:", "opciones": {"A": "Imponer la opinión propia sin discusión", "B": "Evaluar objetivamente los pros y contras de cada opción y decidir basado en datos", "C": "Ignorar el desacuerdo y no decidir", "D": "Escalarlo de inmediato sin intentar resolverlo en equipo"}, "correcta": "B"},
    {"pregunta": "¿Por qué es importante documentar el código y las decisiones técnicas?", "opciones": {"A": "Es un requisito sin utilidad práctica", "B": "Solo sirve para auditorías legales", "C": "Facilita el mantenimiento y la incorporación de nuevos miembros al equipo", "D": "Ralentiza el desarrollo sin ningún beneficio"}, "correcta": "C"},
]

INDUSTRIA_CONSTRUCCION = [
    {"pregunta": "¿Qué elemento de protección personal es indispensable en toda obra de construcción?", "opciones": {"A": "Casco de seguridad", "B": "Corbata", "C": "Reloj de lujo", "D": "Bufanda"}, "correcta": "A"},
    {"pregunta": "¿Qué documento indica las dimensiones y especificaciones técnicas de una obra?", "opciones": {"A": "El contrato de arrendamiento", "B": "Los planos de construcción", "C": "El manual de marketing", "D": "La factura de compra"}, "correcta": "B"},
    {"pregunta": "Antes de excavar en una zona, es importante verificar:", "opciones": {"A": "El clima del mes siguiente", "B": "El color de la pintura a usar", "C": "La ubicación de tuberías y cableado subterráneo", "D": "La marca de las herramientas"}, "correcta": "C"},
    {"pregunta": "¿Qué se debe hacer al detectar una grieta estructural inesperada en una columna durante la obra?", "opciones": {"A": "Cubrirla con pintura y continuar", "B": "Ignorarla si no es visible desde la calle", "C": "Esperar a que el cliente la note", "D": "Detener el trabajo en esa zona y reportarlo al ingeniero responsable"}, "correcta": "D"},
    {"pregunta": "El andamiaje en una obra debe:", "opciones": {"A": "Estar certificado, anclado correctamente y ser inspeccionado antes de su uso", "B": "Usarse sin importar su estado", "C": "Ser el más económico disponible sin revisión", "D": "Solo revisarse al final de la obra"}, "correcta": "A"},
    {"pregunta": "¿Qué significa la sigla EPP en construcción?", "opciones": {"A": "Estimado de Presupuesto Preliminar", "B": "Equipo de Protección Personal", "C": "Estructura de Planta Principal", "D": "Evaluación de Proyecto Pendiente"}, "correcta": "B"},
    {"pregunta": "Un supervisor de obra nota que un trabajador no está usando el arnés de seguridad en altura. La acción correcta es:", "opciones": {"A": "Dejarlo continuar si tiene experiencia", "B": "Reportarlo solo al final del día", "C": "Detener la actividad de inmediato y exigir el uso del equipo de seguridad", "D": "Ignorarlo si el trabajo va rápido"}, "correcta": "C"},
    {"pregunta": "¿Cuál es un objetivo principal de un cronograma de obra (Gantt)?", "opciones": {"A": "Calcular el salario de los empleados", "B": "Diseñar la fachada del edificio", "C": "Decidir el color de la pintura final", "D": "Planificar y controlar los tiempos de cada etapa del proyecto"}, "correcta": "D"},
    {"pregunta": "El concreto necesita un período de 'curado' para:", "opciones": {"A": "Alcanzar su resistencia estructural adecuada", "B": "Cambiar de color", "C": "Secarse más rápido sin importar la resistencia", "D": "Reducir su costo"}, "correcta": "A"},
    {"pregunta": "Ante un sobrecosto detectado a mitad de proyecto, la acción más profesional es:", "opciones": {"A": "Ocultarlo hasta el final del proyecto", "B": "Informar a los interesados, analizar la causa y ajustar el presupuesto o alcance", "C": "Detener el proyecto sin explicación", "D": "Cobrar el sobrecosto sin informar al cliente"}, "correcta": "B"},
    {"pregunta": "¿Qué es una 'orden de cambio' en un proyecto de construcción?", "opciones": {"A": "Un tipo de material de construcción", "B": "Un permiso ambiental", "C": "Una modificación formal y documentada al alcance, tiempo o costo original del proyecto", "D": "Un documento de recursos humanos"}, "correcta": "C"},
    {"pregunta": "La correcta gestión de residuos de construcción incluye:", "opciones": {"A": "Quemarlos en el terreno", "B": "Arrojarlos en cualquier área cercana", "C": "Ignorarlos hasta el final de la obra", "D": "Clasificar y disponer los materiales según normativa ambiental"}, "correcta": "D"},
    {"pregunta": "¿Por qué es importante coordinar entre cuadrillas (electricidad, plomería, estructura)?", "opciones": {"A": "Para evitar retrabajos, conflictos de instalación y retrasos en la obra", "B": "No es necesario si cada cuadrilla trabaja por separado", "C": "Solo importa en obras pequeñas", "D": "Retrasa innecesariamente el proyecto"}, "correcta": "A"},
    {"pregunta": "Un cliente solicita un cambio de último momento que compromete la seguridad estructural. La respuesta profesional es:", "opciones": {"A": "Aceptar el cambio sin cuestionarlo", "B": "Explicar los riesgos técnicos y negociar una alternativa segura y viable", "C": "Ignorar la solicitud sin explicación", "D": "Renunciar al proyecto sin dialogar"}, "correcta": "B"},
    {"pregunta": "El uso de materiales certificados en obra es importante principalmente porque:", "opciones": {"A": "Es más barato siempre", "B": "Es solo un requisito estético", "C": "Garantiza la seguridad y durabilidad de la construcción", "D": "No afecta la calidad final"}, "correcta": "C"},
]

INDUSTRIA_ENERGIA = [
    {"pregunta": "¿Qué elemento de protección es esencial al trabajar con instalaciones eléctricas de alto voltaje?", "opciones": {"A": "Guantes dieléctricos y equipo aislante certificado", "B": "Guantes de tela común", "C": "Ninguno si se tiene experiencia", "D": "Solo lentes de sol"}, "correcta": "A"},
    {"pregunta": "Antes de intervenir un circuito eléctrico, el procedimiento de seguridad estándar indica:", "opciones": {"A": "Trabajar con el circuito energizado para ahorrar tiempo", "B": "Desenergizar, bloquear y etiquetar el circuito (LOTO)", "C": "Avisar solo verbalmente sin bloqueo físico", "D": "Confiar en que otros ya lo revisaron"}, "correcta": "B"},
    {"pregunta": "¿Qué mide un vatímetro?", "opciones": {"A": "La temperatura ambiente", "B": "La velocidad del viento", "C": "La potencia eléctrica consumida", "D": "El nivel de ruido"}, "correcta": "C"},
    {"pregunta": "Las energías renovables como la solar y eólica se caracterizan principalmente por:", "opciones": {"A": "Requerir combustibles fósiles para funcionar", "B": "Generar más emisiones que el petróleo", "C": "No poder integrarse a la red eléctrica", "D": "Provenir de fuentes naturales que se regeneran continuamente"}, "correcta": "D"},
    {"pregunta": "Un técnico detecta un olor a quemado en un transformador durante una inspección de rutina. La acción correcta es:", "opciones": {"A": "Reportarlo de inmediato y seguir el protocolo de emergencia/desenergización", "B": "Ignorarlo si sigue funcionando", "C": "Esperar al siguiente mantenimiento programado", "D": "Intentar repararlo sin apoyo ni protocolo"}, "correcta": "A"},
    {"pregunta": "El mantenimiento preventivo en plantas de energía tiene como objetivo principal:", "opciones": {"A": "Aumentar los costos operativos sin beneficio", "B": "Reducir fallas inesperadas y prolongar la vida útil de los equipos", "C": "Reemplazar equipos que aún funcionan bien sin razón", "D": "Reducir la seguridad del personal"}, "correcta": "B"},
    {"pregunta": "¿Qué es un apagón en cascada (blackout en cadena)?", "opciones": {"A": "Un tipo de mantenimiento programado", "B": "Un aumento controlado de voltaje", "C": "Una falla que se propaga de un punto de la red a otras partes conectadas", "D": "Una mejora en la eficiencia energética"}, "correcta": "C"},
    {"pregunta": "Ante una alerta de sobrecarga en una subestación, la prioridad del operador es:", "opciones": {"A": "Ignorar la alerta si el sistema sigue encendido", "B": "Aumentar la carga para probar el límite real", "C": "Esperar a que se resuelva sola", "D": "Seguir el protocolo de reducción de carga o desconexión segura según procedimiento"}, "correcta": "D"},
    {"pregunta": "¿Qué significa el término 'eficiencia energética'?", "opciones": {"A": "Obtener el mismo resultado o servicio utilizando menos energía", "B": "Consumir la mayor cantidad de energía posible", "C": "Usar solo energía fósil", "D": "Eliminar todo uso de electricidad"}, "correcta": "A"},
    {"pregunta": "La normativa ambiental en proyectos energéticos busca principalmente:", "opciones": {"A": "Aumentar las emisiones sin control", "B": "Minimizar el impacto ambiental de la generación y distribución de energía", "C": "Evitar cualquier tipo de regulación", "D": "Beneficiar solo a la empresa sin considerar el entorno"}, "correcta": "B"},
    {"pregunta": "¿Qué acción es prioritaria si un trabajador sufre un choque eléctrico?", "opciones": {"A": "Tocar a la persona de inmediato sin cortar la energía", "B": "Esperar sin actuar", "C": "Cortar la fuente de energía antes de tocar a la persona afectada y pedir ayuda médica", "D": "Solo tomar fotos del incidente"}, "correcta": "C"},
    {"pregunta": "Un proyecto de energía enfrenta un retraso por permisos ambientales pendientes. La respuesta profesional es:", "opciones": {"A": "Iniciar la obra sin los permisos", "B": "Ocultar el retraso a los interesados", "C": "Cancelar el proyecto sin evaluar alternativas", "D": "Informar a los interesados, dar seguimiento al trámite y ajustar el cronograma"}, "correcta": "D"},
    {"pregunta": "¿Qué es la 'demanda pico' en un sistema eléctrico?", "opciones": {"A": "El momento de mayor consumo de energía en un período determinado", "B": "El momento de menor consumo de energía", "C": "Un tipo de energía renovable", "D": "Un error de medición del sistema"}, "correcta": "A"},
    {"pregunta": "La inspección regular de líneas de transmisión es importante para:", "opciones": {"A": "Aumentar el costo sin ningún beneficio", "B": "Detectar desgaste o daños antes de que causen fallas mayores", "C": "Cumplir un trámite sin utilidad real", "D": "Reducir la vida útil de los equipos"}, "correcta": "B"},
    {"pregunta": "¿Por qué es importante la comunicación clara entre turnos en una planta de energía?", "opciones": {"A": "No es relevante si el sistema es automático", "B": "Solo importa para el pago de horas extra", "C": "Para garantizar la continuidad segura de las operaciones y evitar errores por falta de información", "D": "Retrasa innecesariamente la operación"}, "correcta": "C"},
]

INDUSTRIA_HOTELERIA = [
    {"pregunta": "Un huésped llega antes del horario de check-in oficial y su habitación no está lista. La respuesta más profesional es:", "opciones": {"A": "Explicar la situación con cortesía, ofrecer resguardar el equipaje y dar una alternativa mientras se prepara la habitación", "B": "Decirle que espere sin más explicación", "C": "Ignorar la solicitud", "D": "Cancelar la reserva sin consultarlo"}, "correcta": "A"},
    {"pregunta": "¿Qué es el 'overbooking' en la gestión hotelera?", "opciones": {"A": "Un tipo de tarifa promocional", "B": "Aceptar más reservas que habitaciones disponibles, previendo cancelaciones", "C": "Un sistema de limpieza de habitaciones", "D": "Un protocolo de seguridad contra incendios"}, "correcta": "B"},
    {"pregunta": "Ante la queja de un huésped por ruido excesivo en la habitación contigua, la acción correcta es:", "opciones": {"A": "Ignorar la queja", "B": "Decirle que es normal y no se puede hacer nada", "C": "Escuchar la queja, disculparse y gestionar una solución (cambio de habitación o resolver el ruido)", "D": "Discutir con el huésped"}, "correcta": "C"},
    {"pregunta": "La limpieza y desinfección de habitaciones sigue protocolos estrictos principalmente para:", "opciones": {"A": "Reducir costos operativos únicamente", "B": "Cumplir solo una formalidad sin impacto real", "C": "Decorar mejor la habitación", "D": "Garantizar la salud, seguridad e higiene de los huéspedes"}, "correcta": "D"},
    {"pregunta": "¿Qué información es esencial verificar al hacer el check-in de un huésped?", "opciones": {"A": "Identidad, reserva y método de pago o garantía", "B": "Solo el nombre sin más verificación", "C": "El destino de sus vacaciones anteriores", "D": "Su opinión sobre otros hoteles"}, "correcta": "A"},
    {"pregunta": "Un cliente exigente solicita un upgrade de habitación sin disponibilidad. La respuesta más profesional es:", "opciones": {"A": "Prometer el upgrade sin poder cumplirlo", "B": "Explicar la situación con amabilidad y ofrecer alternativas dentro de lo posible", "C": "Ignorar la solicitud", "D": "Responder de forma brusca"}, "correcta": "B"},
    {"pregunta": "¿Por qué es importante la coordinación entre recepción, ama de llaves y mantenimiento?", "opciones": {"A": "No es relevante si cada área trabaja por separado", "B": "Solo importa en hoteles pequeños", "C": "Para asegurar que las habitaciones estén listas, limpias y en buen estado a tiempo", "D": "Retrasa la operación innecesariamente"}, "correcta": "C"},
    {"pregunta": "¿Qué es un 'protocolo de evacuación' en un hotel?", "opciones": {"A": "Un tipo de servicio de habitación", "B": "Un programa de fidelización de clientes", "C": "Un horario de limpieza", "D": "El procedimiento establecido para evacuar de forma segura a huéspedes y personal en una emergencia"}, "correcta": "D"},
    {"pregunta": "Un huésped extranjero no habla el idioma local y necesita ayuda. La actitud correcta del personal es:", "opciones": {"A": "Mantener la calma, usar herramientas de traducción o gestos, y buscar apoyo si es necesario", "B": "Ignorarlo hasta que consiga ayuda por su cuenta", "C": "Hablarle más fuerte en el idioma local", "D": "Evitar atenderlo"}, "correcta": "A"},
    {"pregunta": "La retroalimentación (encuestas de satisfacción) de los huéspedes es importante porque:", "opciones": {"A": "No tiene ningún valor práctico", "B": "Permite identificar áreas de mejora en el servicio", "C": "Solo sirve para fines de marketing sin acción real", "D": "Es un trámite sin importancia"}, "correcta": "B"},
    {"pregunta": "¿Qué se debe priorizar al manejar un objeto perdido reportado por un huésped?", "opciones": {"A": "Ignorar el reporte", "B": "Decir que no es responsabilidad del hotel sin investigar", "C": "Registrar el reporte, buscar el objeto y dar seguimiento con el huésped", "D": "Esperar a que el huésped se olvide del tema"}, "correcta": "C"},
    {"pregunta": "Un miembro del equipo comete un error en la cuenta final de un huésped. La acción correcta es:", "opciones": {"A": "Ocultar el error", "B": "Culpar al huésped por el malentendido", "C": "Ignorar la situación", "D": "Revisar el error, corregirlo con transparencia y disculparse con el huésped"}, "correcta": "D"},
    {"pregunta": "¿Qué rol cumple el 'concierge' en un hotel?", "opciones": {"A": "Asistir a los huéspedes con recomendaciones, reservas y gestiones externas", "B": "Limpiar las habitaciones", "C": "Preparar los alimentos del restaurante", "D": "Supervisar el mantenimiento eléctrico"}, "correcta": "A"},
    {"pregunta": "La gestión eficiente de inventario en el área de alimentos y bebidas busca principalmente:", "opciones": {"A": "Aumentar el desperdicio de insumos", "B": "Evitar desperdicio y asegurar disponibilidad de insumos", "C": "Reducir la calidad del servicio", "D": "No tiene relación con la rentabilidad del hotel"}, "correcta": "B"},
    {"pregunta": "¿Por qué la primera impresión en la recepción es especialmente importante en hotelería?", "opciones": {"A": "No tiene impacto en la experiencia general", "B": "Solo importa para huéspedes VIP", "C": "Porque influye directamente en la percepción general de la experiencia del huésped", "D": "Es menos relevante que el precio de la habitación"}, "correcta": "C"},
]

INDUSTRIA_CONFIG = {
    "industria_salud": {
        "nombre": "Conocimientos de Sector: Salud",
        "descripcion": "Evaluación de conocimientos y criterio situacional básico para roles del sector salud",
        "categoria_banco": "Industria: Salud",
        "preguntas": INDUSTRIA_SALUD,
    },
    "industria_tecnologia": {
        "nombre": "Conocimientos de Sector: Tecnología",
        "descripcion": "Evaluación de conocimientos y criterio situacional básico para roles del sector tecnológico",
        "categoria_banco": "Industria: Tecnología",
        "preguntas": INDUSTRIA_TECNOLOGIA,
    },
    "industria_construccion": {
        "nombre": "Conocimientos de Sector: Construcción",
        "descripcion": "Evaluación de conocimientos y criterio situacional básico para roles del sector construcción",
        "categoria_banco": "Industria: Construcción",
        "preguntas": INDUSTRIA_CONSTRUCCION,
    },
    "industria_energia": {
        "nombre": "Conocimientos de Sector: Energía",
        "descripcion": "Evaluación de conocimientos y criterio situacional básico para roles del sector energía",
        "categoria_banco": "Industria: Energía",
        "preguntas": INDUSTRIA_ENERGIA,
    },
    "industria_hoteleria": {
        "nombre": "Conocimientos de Sector: Hotelería",
        "descripcion": "Evaluación de conocimientos y criterio situacional básico para roles del sector hotelero",
        "categoria_banco": "Industria: Hotelería",
        "preguntas": INDUSTRIA_HOTELERIA,
    },
}


def preguntas_por_test():
    """Retorna dict test_id -> lista de preguntas, listo para insertar en PreguntaTest."""
    base = {
        "verbal": _mc_preguntas(VERBAL),
        "numerico": _mc_preguntas(NUMERICO),
        "atencion": _mc_preguntas(ATENCION),
        "big_five": _likert_preguntas(BIG_FIVE),
        "ie": _likert_preguntas(IE, LIKERT_OPCIONES_FRECUENCIA),
        "motivacion": _likert_preguntas(MOTIVACION),
        "valores": _likert_preguntas(VALORES),
        "liderazgo": _likert_preguntas(LIDERAZGO),
    }
    for test_id, config in INDUSTRIA_CONFIG.items():
        base[test_id] = _mc_preguntas(config["preguntas"])
    return base


def roles_estrategicos_config():
    """Retorna config de los 5 tests de Roles Estratégicos: id -> {nombre, descripcion, preguntas}."""
    return ROLES_ESTRATEGICOS


def industria_config():
    """Retorna config de los 5 tests de bancos por industria: id -> {nombre, descripcion, categoria_banco, preguntas}."""
    return INDUSTRIA_CONFIG
