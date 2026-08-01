"""
reporte_candidato_service.py - Reporte de resultados en lenguaje amigable
para el candidato (RD$500, ver PRODUCTOS_CANDIDATO en dlocal_service.py).

El candidato NUNCA ve su score crudo (0-100) ni la clasificación interna de
reclutamiento (PRIORITARIO/VIABLE/CONSIDERAR/NO_RECOMENDADO) -- eso es solo
para el reclutador. Este servicio usa esos números como INSUMO para que
Claude redacte una interpretación cualitativa (fortalezas / áreas de
oportunidad), pero el prompt prohíbe explícitamente repetir los números o
las etiquetas internas en la respuesta.
"""

import json
import os

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
MODELO = os.getenv("ANTHROPIC_REPORTE_MODEL", "claude-haiku-4-5-20251001")

SYSTEM_PROMPT = """Eres un asesor de talento que le explica a un candidato, en lenguaje cercano y \
constructivo, cómo le fue en un proceso de evaluación de reclutamiento -- esto lo lee \
DIRECTAMENTE el candidato, no un reclutador.

Recibirás puntuaciones internas (0-100) por categoría, SOLO como contexto para que entiendas su \
desempeño relativo. Reglas estrictas sobre la respuesta:
- NUNCA menciones ningún número, puntuación, porcentaje o score en tu respuesta.
- NUNCA uses las etiquetas internas de clasificación de reclutamiento (por ejemplo "prioritario", \
"viable", "no recomendado", "alto", "medio", "bajo" referidos a una categoría).
- Habla en términos de fortalezas y áreas de oportunidad, con ejemplos generales del tipo de \
habilidad evaluada (por ejemplo "razonamiento numérico", "manejo de las emociones", "orientación \
a resultados"), sin sonar como un reporte técnico.
- Tono alentador y honesto, nunca desalentador ni alarmista, incluso si el desempeño fue bajo en \
alguna categoría -- enmárcalo siempre como una oportunidad de desarrollo.

Responde ÚNICAMENTE con un objeto JSON válido, sin texto adicional antes o después, con este \
formato exacto:
{
  "fortalezas": [<2 a 4 frases cortas>],
  "areas_de_oportunidad": [<2 a 4 frases cortas, en tono constructivo>],
  "mensaje": <1 párrafo breve (2-3 frases) de cierre, en tono alentador>
}"""


def generar_reporte_candidato(candidato_nombre: str, promedios_por_categoria: dict, feedbacks_assessments: list) -> dict:
    """Genera el reporte amigable a partir de los promedios internos por
    categoría (competencias/psicometricos/cognitivos) y los feedbacks ya
    generados de los assessment centers (si los hay). Retorna None si no hay
    API key o algo falla -- el llamador nunca cobra por un reporte que no se
    pudo generar."""
    if not ANTHROPIC_API_KEY:
        return None

    try:
        import anthropic

        contexto = {
            "promedios_internos_0_a_100": promedios_por_categoria,
            "notas_de_assessments": feedbacks_assessments[:5],
        }

        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        mensaje = client.messages.create(
            model=MODELO,
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=[{
                "role": "user",
                "content": (
                    f"Candidato: {candidato_nombre}\n"
                    "---DATOS INTERNOS (contexto, no repetir números en la respuesta)---\n"
                    f"{json.dumps(contexto, ensure_ascii=False)}\n"
                    "---FIN DATOS---\n\n"
                    "Genera el reporte y responde solo con el JSON."
                ),
            }],
        )
        texto_respuesta = mensaje.content[0].text if mensaje.content else ""
        resultado = json.loads(texto_respuesta)
        if not resultado.get("fortalezas") and not resultado.get("mensaje"):
            return None
        return resultado
    except Exception:
        return None
