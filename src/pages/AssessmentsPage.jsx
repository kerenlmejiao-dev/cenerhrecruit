/**
 * CENERH RECRUIT OS - Assessment Center
 * Escenarios de respuesta abierta, evaluados por IA
 */

import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { assessmentAPI } from '../services/api';

export default function AssessmentsPage() {
  const navigate = useNavigate();
  const [assessments, setAssessments] = useState([]);
  const [respuestas, setRespuestas] = useState({});
  const [indiceActual, setIndiceActual] = useState(0);
  const [loading, setLoading] = useState(true);
  const [guardando, setGuardando] = useState(false);
  const [error, setError] = useState('');

  const candidatoId = localStorage.getItem('candidatoId');
  const candidatoNombre = localStorage.getItem('candidatoNombre');

  useEffect(() => {
    if (!candidatoId) {
      navigate('/');
      return;
    }
    cargarAssessments();
  }, []);

  // Al cambiar de escenario (sin cambiar de ruta) volver siempre al inicio.
  useEffect(() => {
    window.scrollTo(0, 0);
  }, [indiceActual]);

  const cargarAssessments = async () => {
    try {
      const data = await assessmentAPI.listar(candidatoId);
      if (!data.assessments || data.assessments.length === 0) {
        navigate('/resultados');
        return;
      }
      setAssessments(data.assessments);
    } catch (err) {
      setError('Error al cargar los assessment centers');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleRespuesta = (preguntaId, texto) => {
    setRespuestas(prev => ({ ...prev, [preguntaId]: texto }));
  };

  const handleSiguiente = async () => {
    const assessmentActual = assessments[indiceActual];
    const pregunta = assessmentActual.preguntas[0];
    const texto = respuestas[pregunta.id] || '';

    if (!texto.trim()) {
      setError('Por favor escribe tu respuesta antes de continuar');
      return;
    }

    setError('');
    setGuardando(true);
    try {
      await assessmentAPI.guardarRespuesta(candidatoId, pregunta.id, texto);

      if (indiceActual < assessments.length - 1) {
        setIndiceActual(indiceActual + 1);
      } else {
        navigate('/resultados');
      }
    } catch (err) {
      setError('Error al guardar tu respuesta. Intenta nuevamente.');
      console.error(err);
    } finally {
      setGuardando(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-900 to-blue-800 flex items-center justify-center">
        <div className="text-white text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-white mb-4"></div>
          <p>Cargando assessment center...</p>
        </div>
      </div>
    );
  }

  if (assessments.length === 0) {
    return null;
  }

  const assessmentActual = assessments[indiceActual];
  const pregunta = assessmentActual.preguntas[0];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-blue-900 py-8">
      <div className="max-w-3xl mx-auto px-4">
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-2xl font-bold text-white">Assessment Center</h1>
              <p className="text-blue-100 text-sm">Hola, {candidatoNombre}</p>
            </div>
            <div className="text-right">
              <div className="text-3xl font-bold text-yellow-300">{indiceActual + 1} / {assessments.length}</div>
              <p className="text-blue-100 text-sm">Escenario</p>
            </div>
          </div>
          <div className="bg-blue-950 rounded-full h-2 overflow-hidden">
            <div
              className="bg-gradient-to-r from-yellow-400 to-yellow-300 h-full transition-all duration-300"
              style={{ width: `${((indiceActual + 1) / assessments.length) * 100}%` }}
            ></div>
          </div>
        </div>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">{error}</div>
        )}

        <div className="bg-white rounded-lg shadow-lg p-6">
          <span className="inline-block bg-purple-100 text-purple-700 text-xs font-semibold px-3 py-1 rounded-full mb-3">
            {assessmentActual.categoria}
          </span>
          <h2 className="text-lg font-semibold text-gray-900 mb-4">{assessmentActual.nombre}</h2>
          <p className="text-gray-700 mb-6 leading-relaxed">{pregunta.escenario}</p>

          <textarea
            value={respuestas[pregunta.id] || ''}
            onChange={(e) => handleRespuesta(pregunta.id, e.target.value)}
            rows="8"
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none resize-none"
            placeholder="Escribe tu respuesta aquí..."
          />
          <p className="text-xs text-gray-500 mt-2">
            Tu respuesta será evaluada por un análisis automatizado.{' '}
            <Link to="/como-usamos-la-ia" target="_blank" className="text-blue-600 hover:text-blue-800 underline">Cómo usamos la IA</Link>
          </p>
        </div>

        <div className="mt-8 flex justify-end">
          <button
            onClick={handleSiguiente}
            disabled={guardando}
            className="bg-gradient-to-r from-yellow-400 to-yellow-500 hover:from-yellow-500 hover:to-yellow-600 text-gray-900 font-bold py-3 px-8 rounded-lg shadow-lg hover:shadow-xl transition disabled:opacity-50"
          >
            {guardando ? 'Guardando...' : indiceActual === assessments.length - 1 ? 'Finalizar' : 'Siguiente'}
          </button>
        </div>
      </div>
    </div>
  );
}
