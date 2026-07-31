/**
 * CENERH RECRUIT OS - Página de Tests
 * Donde candidatos responden preguntas psicométricas
 */

import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { testsAPI, vacantesAPI } from '../services/api';
import { FONT_SANS, FONT_SERIF } from '../theme';

export default function TestsPage() {
  const navigate = useNavigate();
  const [tests, setTests] = useState([]);
  const [testActual, setTestActual] = useState(0);
  const [preguntas, setPreguntas] = useState([]);
  const [respuestas, setRespuestas] = useState({});
  const [loading, setLoading] = useState(true);
  const [guardando, setGuardando] = useState(false);
  const [error, setError] = useState('');
  const [progreso, setProgreso] = useState(0);

  const candidatoId = localStorage.getItem('candidatoId');
  const candidatoNombre = localStorage.getItem('candidatoNombre');
  const vacanteId = localStorage.getItem('vacanteId');

  useEffect(() => {
    if (!candidatoId) {
      navigate('/');
      return;
    }

    cargarTests();
  }, []);

  // Al cambiar de test (sin cambiar de ruta) volver siempre al inicio de la
  // página, para que la primera pregunta del test nuevo sea lo primero visible.
  useEffect(() => {
    window.scrollTo(0, 0);
  }, [testActual]);

  const cargarTests = async () => {
    try {
      const datos = await testsAPI.obtenerDisponibles();
      let testsFiltrados = datos.tests;

      if (vacanteId) {
        try {
          const config = await vacantesAPI.obtenerConfig(vacanteId);
          const testsAAplicar = config.tests_a_aplicar || [];

          if (testsAAplicar.length > 0) {
            testsFiltrados = testsAAplicar
              .map(testId => datos.tests.find(t => t.id === testId))
              .filter(Boolean);
          }
        } catch (errConfig) {
          console.error('Error cargando configuracion de vacante:', errConfig);
        }
      }

      setTests(testsFiltrados);

      if (testsFiltrados.length > 0) {
        await cargarPreguntas(testsFiltrados[0].id);
      }
    } catch (err) {
      setError('Error al cargar tests');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const cargarPreguntas = async (testId) => {
    try {
      setLoading(true);
      setError('');
      const data = await testsAPI.obtenerPreguntas(testId, candidatoId);
      setPreguntas(data.preguntas || []);
      setRespuestas({});
      setProgreso(0);
    } catch (err) {
      setError('Error al cargar preguntas');
      setPreguntas([]);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleRespuesta = (preguntaId, valor) => {
    setRespuestas(prev => ({
      ...prev,
      [preguntaId]: valor
    }));
  };

  const handleSiguiente = async () => {
    if (testActual < tests.length - 1) {
      // Guardar respuestas del test actual
      await guardarRespuestasTest(tests[testActual].id);

      // Pasar al siguiente test
      const siguiente = testActual + 1;
      setTestActual(siguiente);
      await cargarPreguntas(tests[siguiente].id);
    } else {
      // Último test completado
      await guardarRespuestasTest(tests[testActual].id);
      navigate('/assessments');
    }
  };

  const guardarRespuestasTest = async (testId) => {
    try {
      setGuardando(true);
      await testsAPI.guardarRespuestas(testId, candidatoId, respuestas);
    } catch (err) {
      console.error('Error guardando respuestas:', err);
    } finally {
      setGuardando(false);
    }
  };

  if (loading && tests.length === 0) {
    return (
      <div className="min-h-screen bg-[#0D0D0D] flex items-center justify-center" style={FONT_SANS}>
        <div className="text-white text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-[#C9A14A] mb-4"></div>
          <p>Cargando evaluación...</p>
        </div>
      </div>
    );
  }

  if (!tests[testActual]) {
    return (
      <div className="min-h-screen bg-[#0D0D0D] flex items-center justify-center" style={FONT_SANS}>
        <div className="border border-[#2a2a2a] p-8 text-center max-w-md">
          <p className="text-white">Error al cargar tests</p>
        </div>
      </div>
    );
  }

  const testActualObj = tests[testActual];
  const totalTests = tests.length;
  const porcentajeProgreso = ((testActual + 1) / totalTests) * 100;

  return (
    <div className="min-h-screen bg-[#0D0D0D] py-8" style={FONT_SANS}>
      <div className="max-w-4xl mx-auto px-4">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-3xl font-semibold text-white" style={FONT_SERIF}>{testActualObj.nombre}</h1>
              <p className="text-[#B8BFC7] text-sm">Hola, {candidatoNombre}</p>
            </div>
            <div className="text-right">
              <div className="text-4xl font-bold text-[#C9A14A]">
                {testActual + 1} / {totalTests}
              </div>
              <p className="text-[#B8BFC7] text-sm">Test</p>
            </div>
          </div>

          {/* Barra de progreso */}
          <div className="bg-[#1f1f1f] h-1 overflow-hidden">
            <div
              className="bg-[#C9A14A] h-full transition-all duration-300"
              style={{ width: `${porcentajeProgreso}%` }}
            ></div>
          </div>
        </div>

        {error && (
          <div className="border border-[#D62828] text-[#D62828] px-4 py-3 mb-6">
            {error}
          </div>
        )}

        {/* Preguntas */}
        <div className="space-y-6">
          {preguntas.map((pregunta, idx) => (
            <div
              key={pregunta.id}
              className="border border-[#2a2a2a] p-6 hover:border-[#3a3a3a] transition"
            >
              {/* Número de pregunta */}
              <div className="flex items-start mb-4">
                <div className="w-8 h-8 rounded-full bg-[#0050A0] text-white flex items-center justify-center font-bold mr-4 flex-shrink-0">
                  {idx + 1}
                </div>
                <h3 className="text-lg font-semibold text-white flex-grow">
                  {pregunta.pregunta}
                </h3>
              </div>

              {/* Opciones */}
              {pregunta.opciones && Object.keys(pregunta.opciones).length > 0 ? (
                <div className="space-y-3 ml-12">
                  {Object.entries(pregunta.opciones).map(([letra, texto]) => (
                    <label
                      key={letra}
                      className="flex items-center p-3 border border-[#2a2a2a] cursor-pointer hover:border-[#C9A14A] transition"
                    >
                      <input
                        type="radio"
                        name={pregunta.id}
                        value={letra}
                        checked={respuestas[pregunta.id] === letra}
                        onChange={(e) => handleRespuesta(pregunta.id, e.target.value)}
                        className="w-5 h-5 accent-[#D62828]"
                      />
                      <span className="ml-3 text-[#B8BFC7]"><strong className="text-white">{letra}.</strong> {texto}</span>
                    </label>
                  ))}
                </div>
              ) : (
                /* Escala Likert (1-5) */
                <div className="flex justify-between ml-12">
                  {[1, 2, 3, 4, 5].map((valor) => (
                    <label key={valor} className="flex flex-col items-center cursor-pointer">
                      <input
                        type="radio"
                        name={pregunta.id}
                        value={valor}
                        checked={respuestas[pregunta.id] === valor}
                        onChange={(e) => handleRespuesta(pregunta.id, e.target.value)}
                        className="w-5 h-5 accent-[#D62828]"
                      />
                      <span className="text-xs text-[#B8BFC7] mt-2">
                        {valor === 1 && 'Muy en desacuerdo'}
                        {valor === 2 && 'Desacuerdo'}
                        {valor === 3 && 'Neutral'}
                        {valor === 4 && 'Acuerdo'}
                        {valor === 5 && 'Muy de acuerdo'}
                      </span>
                    </label>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Botón Siguiente */}
        <div className="mt-8 flex justify-end">
          <button
            onClick={handleSiguiente}
            disabled={guardando}
            className="bg-[#D62828] hover:bg-[#b91f1f] text-white font-bold tracking-wide py-3 px-8 transition disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {guardando ? 'GUARDANDO...' : testActual === totalTests - 1 ? 'FINALIZAR' : 'SIGUIENTE'}
          </button>
        </div>

        {/* Info */}
        <div className="mt-8 text-center text-[#666] text-sm">
          <p>Tus respuestas se guardan automáticamente</p>
        </div>
      </div>
    </div>
  );
}
