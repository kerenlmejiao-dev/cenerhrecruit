/**
 * CENERH RECRUIT OS - Cómo usamos la Inteligencia Artificial
 * Página pública, sin login. Dirigida tanto a candidatos como a reclutadores.
 */

import { Link } from 'react-router-dom';

function Seccion({ titulo, children }) {
  return (
    <div className="bg-white rounded-lg shadow-lg p-6 md:p-8 mb-6">
      <h2 className="text-xl font-bold text-gray-900 mb-4">{titulo}</h2>
      {children}
    </div>
  );
}

export default function ComoUsamosLaIAPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-blue-900 py-10">
      <div className="max-w-3xl mx-auto px-4">
        <div className="text-center mb-10">
          <div className="text-3xl font-bold text-white mb-2">Cómo usamos la Inteligencia Artificial</div>
          <p className="text-blue-100">Esta página aplica tanto para candidatos como para reclutadores</p>
        </div>

        <Seccion titulo="¿Dónde usamos IA hoy?">
          <p className="text-gray-700 text-sm mb-4">Usamos un modelo de lenguaje (Claude, de Anthropic) en dos momentos concretos del proceso, nunca para decidir automáticamente quién es contratado:</p>
          <div className="space-y-4">
            <div className="border border-purple-200 bg-purple-50 rounded-lg p-4">
              <h3 className="font-bold text-gray-900 text-sm mb-1">1. Assessment Centers</h3>
              <p className="text-gray-700 text-sm">Cuando una vacante lo incluye, el candidato responde en texto libre a un escenario de trabajo (ej. "cómo manejarías una crisis con un cliente"). La IA lee esa respuesta y la puntúa contra una rúbrica de criterios (ej. transparencia, plan de acción), dando un score y un comentario.</p>
            </div>
            <div className="border border-blue-200 bg-blue-50 rounded-lg p-4">
              <h3 className="font-bold text-gray-900 text-sm mb-1">2. Compatibilidad con la vacante</h3>
              <p className="text-gray-700 text-sm">La IA compara los datos del perfil del candidato (ciudad de residencia, formación, experiencia laboral, último cargo) contra los requisitos que el reclutador definió para la posición, y genera un score de encaje con fortalezas y posibles brechas.</p>
            </div>
          </div>
        </Seccion>

        <Seccion titulo="¿Qué datos analiza?">
          <p className="text-gray-700 text-sm mb-2">Solo los datos que el propio candidato completó en su perfil:</p>
          <ul className="text-gray-700 text-sm list-disc list-inside space-y-1">
            <li>Su respuesta escrita al escenario del Assessment Center</li>
            <li>Ciudad o provincia de residencia</li>
            <li>Nivel académico, carrera y universidad</li>
            <li>Años de experiencia, último cargo y funciones desempeñadas</li>
          </ul>
          <p className="text-gray-700 text-sm mt-3">No usamos datos sensibles como cédula, salario, estado civil, hijos ni contacto de emergencia para ningún análisis de IA — esos campos existen solo para la ficha del reclutador, la IA nunca los procesa.</p>
        </Seccion>

        <Seccion titulo="¿Dónde viven tus datos?">
          <p className="text-gray-700 text-sm">Tu información se procesa y se guarda en la infraestructura de CENERH Consulting para el mercado dominicano — no la enviamos a bases de datos de terceros ni la usamos para entrenar modelos de IA. El único servicio externo que interviene es el modelo de lenguaje que puntúa tu respuesta en el momento, y no conserva tus datos después de responder.</p>
        </Seccion>

        <Seccion titulo="Nuestras garantías">
          <ul className="space-y-3">
            <li className="flex gap-2 text-sm text-gray-700">
              <span className="text-green-600 font-bold">✓</span>
              <span><strong>La decisión final siempre es humana.</strong> La IA nunca aprueba, rechaza ni contrata a nadie — solo genera información de apoyo para que el reclutador decida.</span>
            </li>
            <li className="flex gap-2 text-sm text-gray-700">
              <span className="text-green-600 font-bold">✓</span>
              <span><strong>Revisión humana obligatoria antes de usarse.</strong> Cada análisis de Assessment Center queda marcado como "pendiente de revisión" hasta que un reclutador lo lea y lo confirme.</span>
            </li>
            <li className="flex gap-2 text-sm text-gray-700">
              <span className="text-green-600 font-bold">✓</span>
              <span><strong>Tu respuesta se trata como dato, nunca como instrucción.</strong> El sistema está diseñado para ignorar cualquier intento de manipular al modelo desde el texto de una respuesta.</span>
            </li>
            <li className="flex gap-2 text-sm text-gray-700">
              <span className="text-green-600 font-bold">✓</span>
              <span><strong>No es el único criterio.</strong> El score de IA se combina con los tests psicométricos tradicionales — nunca decide solo.</span>
            </li>
          </ul>
        </Seccion>

        <Seccion titulo="Si eres candidato">
          <p className="text-gray-700 text-sm">Puedes ver el feedback que recibiste en cualquier Assessment Center desde tu página de resultados. Si consideras que un análisis no te representa, puedes escribirnos y pedir que un reclutador lo revise manualmente antes de tomarse en cuenta.</p>
        </Seccion>

        <Seccion titulo="Si eres reclutador">
          <p className="text-gray-700 text-sm">El análisis de IA es un punto de partida, no un veredicto. Antes de avanzar o descartar a un candidato, lee siempre su respuesta completa y marca el análisis como revisado. El score de compatibilidad es orientativo — puede pasar por alto contexto que solo tú conoces del cliente o la posición.</p>
        </Seccion>

        <div className="text-center mt-8">
          <Link to="/" className="text-blue-100 hover:text-white text-sm underline">Volver al inicio</Link>
        </div>
      </div>
    </div>
  );
}
