/**
 * Portal Reclutador - Assessment Centers de un candidato: respuesta abierta,
 * score/feedback de la IA (Claude) y marcado de revisión humana.
 *
 * El score de IA no debe usarse ciego para contratar, así que esta pantalla
 * existe para que el reclutador lea la respuesta real antes de decidir.
 * Requiere suscripción activa (el backend responde 402 si no la hay).
 */

import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { reclutadorAPI } from '../../services/api';

export default function CandidatoAssessments() {
  const { candidatoId } = useParams();
  const navigate = useNavigate();
  const [assessments, setAssessments] = useState(null);
  const [compatibilidad, setCompatibilidad] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [requiereSuscripcion, setRequiereSuscripcion] = useState(false);
  const [marcando, setMarcando] = useState(null);

  useEffect(() => {
    cargar();
  }, [candidatoId]);

  const cargar = async () => {
    setLoading(true);
    setError('');
    setRequiereSuscripcion(false);
    try {
      const data = await reclutadorAPI.assessmentsCandidato(candidatoId);
      setAssessments(data.assessments);
      setCompatibilidad(data.compatibilidad);
    } catch (err) {
      if (err.response?.status === 402) {
        setRequiereSuscripcion(true);
      } else if (err.response?.status === 403) {
        setError('No autorizado para ver este candidato.');
      } else {
        setError('Error al cargar los assessment centers.');
      }
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const marcarRevisado = async (assessmentId) => {
    setMarcando(assessmentId);
    try {
      await reclutadorAPI.marcarAssessmentRevisado(candidatoId, assessmentId);
      setAssessments(prev =>
        prev.map(a => a.assessment_id === assessmentId ? { ...a, revisado_por_humano: true } : a)
      );
    } catch (err) {
      setError('No se pudo marcar como revisado. Intenta nuevamente.');
      console.error(err);
    } finally {
      setMarcando(null);
    }
  };

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center text-gray-600">Cargando...</div>;
  }

  if (requiereSuscripcion) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="bg-white rounded-lg shadow p-8 max-w-md text-center">
          <h1 className="text-xl font-bold text-gray-900 mb-2">Suscripción requerida</h1>
          <p className="text-gray-600 mb-6">
            Necesitas una suscripción activa para ver el análisis de los Assessment Centers de tus candidatos.
          </p>
          <Link
            to="/reclutador/suscripcion"
            className="inline-block bg-gradient-to-r from-blue-600 to-blue-800 text-white font-semibold px-6 py-2.5 rounded-lg hover:from-blue-700 hover:to-blue-900 transition"
          >
            Ver planes de suscripción
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white shadow">
        <div className="max-w-4xl mx-auto px-4 py-6">
          <button onClick={() => navigate(-1)} className="text-sm text-blue-600 hover:text-blue-800">&larr; Volver</button>
          <h1 className="text-3xl font-bold text-gray-900 mt-2">Análisis de IA</h1>
          <p className="text-gray-600 text-sm mt-1">Compatibilidad con la vacante y Assessment Centers — apoyo para decidir, no usar ciego</p>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 py-8 space-y-6">
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">{error}</div>
        )}

        {compatibilidad ? (
          <div className="bg-white rounded-lg shadow p-6 border-l-4 border-blue-500">
            <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-2">Compatibilidad con la vacante</h2>
            <div className="flex items-baseline gap-2 mb-3">
              <span className="text-3xl font-bold text-blue-600">{Math.round(compatibilidad.score)}</span>
              <span className="text-gray-500 text-sm">/100</span>
            </div>
            {compatibilidad.resumen && <p className="text-gray-700 text-sm mb-3">{compatibilidad.resumen}</p>}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {compatibilidad.fortalezas && compatibilidad.fortalezas.length > 0 && (
                <div>
                  <h3 className="text-xs font-semibold text-green-700 uppercase mb-1">Fortalezas</h3>
                  <ul className="text-sm text-gray-600 list-disc list-inside space-y-0.5">
                    {compatibilidad.fortalezas.map((f, i) => <li key={i}>{f}</li>)}
                  </ul>
                </div>
              )}
              {compatibilidad.brechas && compatibilidad.brechas.length > 0 && (
                <div>
                  <h3 className="text-xs font-semibold text-amber-700 uppercase mb-1">Brechas / riesgos</h3>
                  <ul className="text-sm text-gray-600 list-disc list-inside space-y-0.5">
                    {compatibilidad.brechas.map((b, i) => <li key={i}>{b}</li>)}
                  </ul>
                </div>
              )}
            </div>
          </div>
        ) : (
          <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 text-sm text-gray-500 italic">
            Aún no hay un análisis de compatibilidad para este candidato.
          </div>
        )}

        <h2 className="text-lg font-bold text-gray-900">Assessment Centers</h2>

        {assessments && assessments.length === 0 && (
          <div className="bg-white rounded-lg shadow p-6 text-center text-gray-500">
            Este candidato no tiene assessment centers respondidos todavía.
          </div>
        )}

        {assessments && assessments.map(a => (
          <div key={a.assessment_id} className="bg-white rounded-lg shadow p-6">
            <div className="flex items-start justify-between gap-4 mb-4">
              <div>
                <span className="bg-purple-50 text-purple-700 px-3 py-1 rounded-full text-xs font-semibold">{a.categoria}</span>
                <h2 className="text-lg font-semibold text-gray-900 mt-2">{a.nombre}</h2>
              </div>
              {a.revisado_por_humano ? (
                <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-xs font-semibold whitespace-nowrap">✓ Revisado</span>
              ) : (
                <span className="bg-yellow-100 text-yellow-700 px-3 py-1 rounded-full text-xs font-semibold whitespace-nowrap">Pendiente de revisión</span>
              )}
            </div>

            <div className="mb-4">
              <h3 className="text-sm font-semibold text-gray-700 mb-1">Escenario planteado</h3>
              <p className="text-gray-600 text-sm bg-gray-50 rounded p-3">{a.escenario}</p>
            </div>

            <div className="mb-4">
              <h3 className="text-sm font-semibold text-gray-700 mb-1">Respuesta del candidato</h3>
              <p className="text-gray-800 text-sm bg-blue-50 rounded p-3 whitespace-pre-wrap">{a.respuesta_texto}</p>
            </div>

            {a.score_ia !== null ? (
              <div className="mb-4">
                <h3 className="text-sm font-semibold text-gray-700 mb-1">
                  Análisis de la IA &mdash; Score: <span className="text-blue-600">{Math.round(a.score_ia)}/100</span>
                </h3>
                {a.feedback_ia && <p className="text-gray-600 text-sm mb-2">{a.feedback_ia}</p>}
                {a.criterios_detalle && a.criterios_detalle.length > 0 && (
                  <ul className="text-sm text-gray-600 list-disc list-inside space-y-0.5">
                    {a.criterios_detalle.map((c, i) => (
                      <li key={i}>{c.nombre}: {c.score}/100{c.comentario ? ` — ${c.comentario}` : ''}</li>
                    ))}
                  </ul>
                )}
              </div>
            ) : (
              <div className="mb-4 text-sm text-gray-500 italic">
                Aún no hay un score de IA para esta respuesta.
              </div>
            )}

            {!a.revisado_por_humano && a.score_ia !== null && (
              <button
                onClick={() => marcarRevisado(a.assessment_id)}
                disabled={marcando === a.assessment_id}
                className="bg-gray-800 text-white text-sm font-medium px-4 py-2 rounded-lg hover:bg-gray-900 transition disabled:opacity-50"
              >
                {marcando === a.assessment_id ? 'Marcando...' : 'Marcar como revisado'}
              </button>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
