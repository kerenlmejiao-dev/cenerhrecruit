/**
 * CENERH RECRUIT OS - Cómo usamos la Inteligencia Artificial
 * Página pública, sin login. Dirigida tanto a candidatos como a reclutadores.
 */

import { Link } from 'react-router-dom';
import { FONT_SANS, FONT_SERIF } from '../theme';

function Seccion({ titulo, children }) {
  return (
    <div className="border border-[#2a2a2a] p-6 md:p-8 mb-6">
      <h2 className="text-xl font-semibold text-white mb-4" style={FONT_SERIF}>{titulo}</h2>
      {children}
    </div>
  );
}

export default function ComoUsamosLaIAPage() {
  return (
    <div className="min-h-screen bg-[#0D0D0D] py-10" style={FONT_SANS}>
      <div className="max-w-3xl mx-auto px-4">
        <div className="text-center mb-10">
          <div className="text-3xl font-semibold text-white mb-2" style={FONT_SERIF}>Cómo usamos la Inteligencia Artificial</div>
          <p className="text-[#B8BFC7]">Esta página aplica tanto para candidatos como para reclutadores</p>
        </div>

        <Seccion titulo="¿Dónde usamos IA hoy?">
          <p className="text-[#B8BFC7] text-sm mb-4">Usamos un modelo de lenguaje (Claude, de Anthropic) en dos momentos concretos del proceso, nunca para decidir automáticamente quién es contratado:</p>
          <div className="space-y-4">
            <div className="border border-[#0050A0]/40 p-4">
              <h3 className="font-bold text-white text-sm mb-1">1. Assessment Centers</h3>
              <p className="text-[#B8BFC7] text-sm">Cuando una vacante lo incluye, el candidato responde en texto libre a un escenario de trabajo (ej. "cómo manejarías una crisis con un cliente"). La IA lee esa respuesta y la puntúa contra una rúbrica de criterios (ej. transparencia, plan de acción), dando un score y un comentario.</p>
            </div>
            <div className="border border-[#C9A14A]/40 p-4">
              <h3 className="font-bold text-white text-sm mb-1">2. Compatibilidad con la vacante</h3>
              <p className="text-[#B8BFC7] text-sm">La IA compara los datos del perfil del candidato (ciudad de residencia, formación, experiencia laboral, último cargo) contra los requisitos que el reclutador definió para la posición, y genera un score de encaje con fortalezas y posibles brechas.</p>
            </div>
          </div>
        </Seccion>

        <Seccion titulo="¿Qué datos analiza?">
          <p className="text-[#B8BFC7] text-sm mb-2">Solo los datos que el propio candidato completó en su perfil:</p>
          <ul className="text-[#B8BFC7] text-sm list-disc list-inside space-y-1">
            <li>Su respuesta escrita al escenario del Assessment Center</li>
            <li>Ciudad o provincia de residencia</li>
            <li>Nivel académico, carrera y universidad</li>
            <li>Años de experiencia, último cargo y funciones desempeñadas</li>
          </ul>
          <p className="text-[#B8BFC7] text-sm mt-3">No usamos datos sensibles como cédula, salario, estado civil, hijos ni contacto de emergencia para ningún análisis de IA — esos campos existen solo para la ficha del reclutador, la IA nunca los procesa.</p>
        </Seccion>

        <Seccion titulo="¿Dónde viven tus datos?">
          <p className="text-[#B8BFC7] text-sm">Tu información se procesa y se guarda en la infraestructura de CENERH Consulting para el mercado dominicano — no la enviamos a bases de datos de terceros ni la usamos para entrenar modelos de IA. El único servicio externo que interviene es el modelo de lenguaje que puntúa tu respuesta en el momento, y no conserva tus datos después de responder.</p>
        </Seccion>

        <Seccion titulo="Nuestras garantías">
          <ul className="space-y-3">
            <li className="flex gap-2 text-sm text-[#B8BFC7]">
              <span className="text-[#C9A14A] font-bold">✓</span>
              <span><strong className="text-white">La decisión final siempre es humana.</strong> La IA nunca aprueba, rechaza ni contrata a nadie — solo genera información de apoyo para que el reclutador decida.</span>
            </li>
            <li className="flex gap-2 text-sm text-[#B8BFC7]">
              <span className="text-[#C9A14A] font-bold">✓</span>
              <span><strong className="text-white">Revisión humana obligatoria antes de usarse.</strong> Cada análisis de Assessment Center queda marcado como "pendiente de revisión" hasta que un reclutador lo lea y lo confirme.</span>
            </li>
            <li className="flex gap-2 text-sm text-[#B8BFC7]">
              <span className="text-[#C9A14A] font-bold">✓</span>
              <span><strong className="text-white">Tu respuesta se trata como dato, nunca como instrucción.</strong> El sistema está diseñado para ignorar cualquier intento de manipular al modelo desde el texto de una respuesta.</span>
            </li>
            <li className="flex gap-2 text-sm text-[#B8BFC7]">
              <span className="text-[#C9A14A] font-bold">✓</span>
              <span><strong className="text-white">No es el único criterio.</strong> El score de IA se combina con los tests psicométricos tradicionales — nunca decide solo.</span>
            </li>
          </ul>
        </Seccion>

        <Seccion titulo="Si eres candidato">
          <p className="text-[#B8BFC7] text-sm">Tus respuestas y resultados se entregan directamente a tu reclutador -- no se muestran en pantalla ni por correo, para que el proceso de evaluación sea igual de objetivo para todos los candidatos. Tu página de seguimiento solo indica en qué etapa del proceso de reclutamiento te encuentras.</p>
        </Seccion>

        <Seccion titulo="Si eres reclutador">
          <p className="text-[#B8BFC7] text-sm">El análisis de IA es un punto de partida, no un veredicto. Antes de avanzar o descartar a un candidato, lee siempre su respuesta completa y marca el análisis como revisado. El score de compatibilidad es orientativo — puede pasar por alto contexto que solo tú conoces del cliente o la posición.</p>
        </Seccion>

        <div className="text-center mt-8">
          <Link to="/" className="text-[#666] hover:text-white text-sm underline">Volver al inicio</Link>
        </div>
      </div>
    </div>
  );
}
