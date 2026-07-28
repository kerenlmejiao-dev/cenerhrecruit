/**
 * CENERH RECRUIT OS - Página de Resultados
 * Donde candidatos ven sus scores y descargan PDF
 */

import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { candidatosAPI } from '../services/api';

export default function ResultadosPage() {
  const navigate = useNavigate();
  const [datos, setDatos] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [descargando, setDescargando] = useState(false);
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

  const descargarPDF = async () => {
    try {
      setDescargando(true);
      const resultado = await candidatosAPI.generarPDF(candidatoId);

      // Crear descarga (simular)
      alert(`PDF generado: ${resultado.tamaño_kb} KB\n\nEn producción, el PDF se descargará automáticamente.`);
    } catch (err) {
      alert('Error al generar PDF');
    } finally {
      setDescargando(false);
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

        {/* Acciones */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
          <button
            onClick={descargarPDF}
            disabled={descargando}
            className="bg-white hover:bg-gray-50 text-blue-600 font-bold py-3 px-6 rounded-lg shadow-lg hover:shadow-xl transition flex items-center justify-center gap-2 disabled:opacity-50"
          >
            <span>📄</span>
            {descargando ? 'Generando PDF...' : 'Descargar PDF'}
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
