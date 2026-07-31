/**
 * CENERH RECRUIT OS - Página de Resultados
 * Donde candidatos ven sus scores y descargan PDF
 */

import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { candidatosAPI } from '../services/api';

const ETAPAS_PROCESO = ['Aplicación recibida', 'En evaluación', 'Preseleccionado', 'Entrevista', 'Decisión final'];

function StatusReclutamiento({ status }) {
  if (status === 'Rechazado') {
    return (
      <div className="bg-gray-100 border border-gray-300 rounded-lg p-6 mb-8 text-center">
        <p className="text-gray-800 font-semibold">Tu proceso para esta posición ha finalizado</p>
        <p className="text-gray-600 text-sm mt-1">Gracias por tu interés. Te invitamos a aplicar a futuras vacantes que encajen con tu perfil.</p>
      </div>
    );
  }

  if (status === 'Contratado') {
    return (
      <div className="bg-green-50 border border-green-300 rounded-lg p-6 mb-8 text-center">
        <p className="text-green-800 font-bold text-lg">¡Felicidades, fuiste seleccionado! 🎉</p>
        <p className="text-green-700 text-sm mt-1">Pronto se pondrán en contacto contigo con los siguientes pasos.</p>
      </div>
    );
  }

  const indiceActual = ETAPAS_PROCESO.indexOf(status);

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
      <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-4">¿Cómo vas en el proceso?</h2>
      <div className="flex items-center">
        {ETAPAS_PROCESO.map((etapa, i) => {
          const completada = indiceActual >= 0 && i < indiceActual;
          const actual = i === indiceActual;
          return (
            <div key={etapa} className="flex items-center flex-1 last:flex-none">
              <div className="flex flex-col items-center gap-1 text-center w-24">
                <div className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold ${
                  completada ? 'bg-blue-600 text-white' :
                  actual ? 'bg-blue-600 text-white ring-4 ring-blue-200' :
                  'bg-gray-200 text-gray-500'
                }`}>
                  {completada ? '✓' : i + 1}
                </div>
                <span className={`text-xs ${actual ? 'font-bold text-blue-700' : 'text-gray-500'}`}>{etapa}</span>
              </div>
              {i < ETAPAS_PROCESO.length - 1 && (
                <div className={`flex-1 h-0.5 ${completada ? 'bg-blue-600' : 'bg-gray-200'}`}></div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default function ResultadosPage() {
  const navigate = useNavigate();
  const [datos, setDatos] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [enviando, setEnviando] = useState(false);

  const candidatoId = localStorage.getItem('candidatoId');
  const candidatoNombre = localStorage.getItem('candidatoNombre');

  useEffect(() => {
    if (!candidatoId) {
      navigate('/');
      return;
    }

    cargarResultados();
  }, []);

  const cargarResultados = async () => {
    try {
      const data = await candidatosAPI.obtenerResultados(candidatoId);
      setDatos(data);
    } catch (err) {
      setError('Error al cargar resultados');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const enviarEmail = async () => {
    try {
      setEnviando(true);
      const resultado = await candidatosAPI.enviarEmail(candidatoId);
      alert(`Email enviado a ${resultado.email}`);
    } catch (err) {
      alert('Error al enviar email');
    } finally {
      setEnviando(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-900 to-blue-800 flex items-center justify-center">
        <div className="text-white text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-white mb-4"></div>
          <p>Cargando resultados...</p>
        </div>
      </div>
    );
  }

  if (error || !datos) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-900 to-blue-800 flex items-center justify-center">
        <div className="bg-white rounded-lg shadow-lg p-8 text-center max-w-md">
          <p className="text-red-600 mb-4">{error || 'No hay datos disponibles'}</p>
          <button
            onClick={() => navigate('/')}
            className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700"
          >
            Volver
          </button>
        </div>
      </div>
    );
  }

  const scoreClasificacion = (score) => {
    if (score >= 81) return { bg: 'bg-green-100', border: 'border-green-300', text: 'text-green-700', label: 'PRIORITARIO ⭐⭐⭐' };
    if (score >= 61) return { bg: 'bg-blue-100', border: 'border-blue-300', text: 'text-blue-700', label: 'VIABLE ⭐⭐' };
    if (score >= 41) return { bg: 'bg-yellow-100', border: 'border-yellow-300', text: 'text-yellow-700', label: 'CONSIDERAR ⭐' };
    return { bg: 'bg-red-100', border: 'border-red-300', text: 'text-red-700', label: 'NO RECOMENDADO' };
  };

  const clasificacion = scoreClasificacion(datos.score_final);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-blue-900 py-8">
      <div className="max-w-4xl mx-auto px-4">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="text-4xl font-bold text-white mb-2">¡Evaluación Completa!</div>
          <p className="text-blue-100">Hola, {candidatoNombre}</p>
        </div>

        <StatusReclutamiento status={datos.status_reclutamiento} />

        {/* Score Final */}
        <div className={`${clasificacion.bg} ${clasificacion.border} border-2 rounded-lg shadow-xl p-8 mb-8`}>
          <div className="text-center">
            <p className={`text-sm font-semibold ${clasificacion.text} mb-2`}>SCORE FINAL</p>
            <div className="text-6xl font-bold text-gray-900 mb-2">{datos.score_final}</div>
            <p className={`text-xl font-bold ${clasificacion.text}`}>{clasificacion.label}</p>
          </div>
        </div>

        {/* Scores por Test */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
          {datos.scores_por_test && datos.scores_por_test.map((score) => {
            const class_info = scoreClasificacion(score.score);
            return (
              <div
                key={score.test_id}
                className={`${class_info.bg} ${class_info.border} border rounded-lg p-6`}
              >
                <div className="flex justify-between items-start mb-3">
                  <div>
                    <h3 className="font-bold text-gray-900">{score.test_nombre}</h3>
                    <p className={`text-sm ${class_info.text}`}>{score.clasificacion}</p>
                  </div>
                  <div className="text-3xl font-bold text-gray-900">{score.score}</div>
                </div>
                <div className="w-full bg-gray-300 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full bg-gradient-to-r from-blue-500 to-green-500`}
                    style={{ width: `${(score.score / 100) * 100}%` }}
                  ></div>
                </div>
              </div>
            );
          })}
        </div>

        {/* Promedios por Categoría */}
        {datos.promedios && (
          <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Desempeño por Categoría</h2>
            <div className="space-y-4">
              {Object.entries(datos.promedios).map(([categoria, promedio]) => {
                const nombreCategoria = {
                  competencias: 'Competencias Laborales',
                  psicometricos: 'Evaluación Psicométrica',
                  cognitivos: 'Habilidades Cognitivas',
                }[categoria] || categoria;

                return (
                  <div key={categoria}>
                    <div className="flex justify-between mb-2">
                      <span className="font-semibold text-gray-700">{nombreCategoria}</span>
                      <span className="font-bold text-blue-600">{promedio}/100</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-3">
                      <div
                        className="h-3 rounded-full bg-gradient-to-r from-blue-600 to-purple-600"
                        style={{ width: `${(promedio / 100) * 100}%` }}
                      ></div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Assessment Centers */}
        {datos.assessments && datos.assessments.length > 0 && (
          <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Assessment Centers</h2>
            <div className="space-y-4">
              {datos.assessments.map((a) => (
                <div key={a.assessment_id} className="border border-purple-200 bg-purple-50 rounded-lg p-4">
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="font-bold text-gray-900">{a.nombre}</h3>
                    <div className="text-2xl font-bold text-purple-700">{a.score}</div>
                  </div>
                  {a.feedback && <p className="text-sm text-gray-700">{a.feedback}</p>}
                </div>
              ))}
            </div>
            <Link to="/como-usamos-la-ia" target="_blank" className="text-xs text-purple-700 hover:text-purple-900 underline mt-3 inline-block">
              Cómo la IA analizó tu respuesta
            </Link>
          </div>
        )}

        {/* Acciones */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
          <button
            onClick={() => navigate('/perfil?retorno=resultados')}
            className="bg-white hover:bg-gray-50 text-blue-600 font-bold py-3 px-6 rounded-lg shadow-lg hover:shadow-xl transition flex items-center justify-center gap-2"
          >
            <span>✏️</span>
            Corregir o actualizar mis datos
          </button>

          <button
            onClick={enviarEmail}
            disabled={enviando}
            className="bg-gradient-to-r from-yellow-400 to-yellow-500 hover:from-yellow-500 hover:to-yellow-600 text-gray-900 font-bold py-3 px-6 rounded-lg shadow-lg hover:shadow-xl transition flex items-center justify-center gap-2 disabled:opacity-50"
          >
            <span>📧</span>
            {enviando ? 'Enviando...' : 'Enviar por Email'}
          </button>
        </div>

        {/* Info */}
        <div className="bg-blue-50 border-l-4 border-blue-600 p-6 rounded">
          <p className="text-blue-900 font-semibold mb-2">¿Qué sucede ahora?</p>
          <p className="text-blue-800 text-sm">
            Tu evaluación ha sido completada. CENERH Consulting analizará tus resultados y se comunicará contigo en los próximos 3 días hábiles con retroalimentación personalizada.
          </p>
        </div>
      </div>
    </div>
  );
}
