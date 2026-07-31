/**
 * CENERH RECRUIT OS - Assessment Center
 * Escenarios de respuesta abierta, evaluados por IA
 */

import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { assessmentAPI } from '../services/api';
import { FONT_SANS, FONT_SERIF } from '../theme';

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
      <div className="min-h-screen bg-[#0D0D0D] flex items-center justify-center" style={FONT_SANS}>
        <div className="text-white text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-[#C9A14A] mb-4"></div>
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
    <div className="min-h-screen bg-[#0D0D0D] py-8" style={FONT_SANS}>
      <div className="max-w-3xl mx-auto px-4">
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-2xl font-semibold text-white" style={FONT_SERIF}>Assessment Center</h1>
              <p className="text-[#B8BFC7] text-sm">Hola, {candidatoNombre}</p>
            </div>
            <div className="text-right">
              <div className="text-3xl font-bold text-[#C9A14A]">{indiceActual + 1} / {assessments.length}</div>
              <p className="text-[#B8BFC7] text-sm">Escenario</p>
            </div>
          </div>
          <div className="bg-[#1f1f1f] h-1 overflow-hidden">
            <div
              className="bg-[#C9A14A] h-full transition-all duration-300"
              style={{ width: `${((indiceActual + 1) / assessments.length) * 100}%` }}
            ></div>
          </div>
        </div>

        {error && (
          <div className="border border-[#D62828] text-[#D62828] px-4 py-3 mb-6">{error}</div>
        )}

        <div className="border border-[#2a2a2a] p-6">
          <span className="inline-block border border-[#0050A0] text-[#0050A0] text-xs font-semibold px-3 py-1 mb-3">
            {assessmentActual.categoria}
          </span>
          <h2 className="text-lg font-semibold text-white mb-4">{assessmentActual.nombre}</h2>
          <p className="text-[#B8BFC7] mb-6 leading-relaxed">{pregunta.escenario}</p>

          <textarea
            value={respuestas[pregunta.id] || ''}
            onChange={(e) => handleRespuesta(pregunta.id, e.target.value)}
            rows="8"
            className="w-full px-4 py-3 bg-[#0D0D0D] border border-[#2a2a2a] text-white rounded focus:ring-1 focus:ring-[#C9A14A] focus:border-[#C9A14A] outline-none resize-none placeholder:text-[#555]"
            placeholder="Escribe tu respuesta aquí..."
          />
          <p className="text-xs text-[#666] mt-2">
            Tu respuesta será evaluada por un análisis automatizado.{' '}
            <Link to="/como-usamos-la-ia" target="_blank" className="text-[#C9A14A] hover:text-white underline">Cómo usamos la IA</Link>
          </p>
        </div>

        <div className="mt-8 flex justify-end">
          <button
            onClick={handleSiguiente}
            disabled={guardando}
            className="bg-[#D62828] hover:bg-[#b91f1f] text-white font-bold tracking-wide py-3 px-8 transition disabled:opacity-50"
          >
            {guardando ? 'GUARDANDO...' : indiceActual === assessments.length - 1 ? 'FINALIZAR' : 'SIGUIENTE'}
          </button>
        </div>
      </div>
    </div>
  );
}
