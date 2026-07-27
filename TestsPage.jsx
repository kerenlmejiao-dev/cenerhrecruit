/**
 * CENERH RECRUIT OS - Página de Tests
 * Donde candidatos responden preguntas psicométricas
 */

import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { testsAPI } from '../services/api';

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

  useEffect(() => {
    if (!candidatoId) {
      navigate('/');
      return;
    }

    cargarTests();
  }, []);

  const cargarTests = async () => {
    try {
      const data = await testsAPI.obtenerDisponibles();
      setTests(data.tests);
      
      if (data.tests.length > 0) {
        await cargarPreguntas(data.tests[0].id);
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
      const data = await testsAPI.obtenerPreguntas(testId, candidatoId);
      setPreguntas(data.preguntas || []);
      setRespuestas({});
      setProgreso(0);
    } catch (err) {
      setError('Error al cargar preguntas');
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
      navigate('/resultados');
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
      <div className="min-h-screen bg-gradient-to-br from-blue-900 to-blue-800 flex items-center justify-center">
        <div className="text-white text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-white mb-4"></div>
          <p>Cargando evaluación...</p>
        </div>
      </div>
    );
  }

  if (!tests[testActual]) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-900 to-blue-800 flex items-center justify-center">
        <div className="bg-white rounded-lg shadow-lg p-8 text-center max-w-md">
          <p className="text-gray-900">Error al cargar tests</p>
        </div>
      </div>
    );
  }

  const testActualObj = tests[testActual];
  const totalTests = tests.length;
  const porcentajeProgreso = ((testActual + 1) / totalTests) * 100;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-blue-900 py-8">
      <div className="max-w-4xl mx-auto px-4">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-3xl font-bold text-white">{testActualObj.nombre}</h1>
              <p className="text-blue-100 text-sm">Hola, {candidatoNombre}</p>
            </div>
            <div className="text-right">
              <div className="text-4xl font-bold text-yellow-300">
                {testActual + 1} / {totalTests}
              </div>
              <p className="text-blue-100 text-sm">Test</p>
            </div>
          </div>

          {/* Barra de progreso */}
          <div className="bg-blue-950 rounded-full h-2 overflow-hidden">
            <div
              className="bg-gradient-to-r from-yellow-400 to-yellow-300 h-full transition-all duration-300"
              style={{ width: `${porcentajeProgreso}%` }}
            ></div>
          </div>
        </div>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
            {error}
          </div>
        )}

        {/* Preguntas */}
        <div className="space-y-6">
          {preguntas.map((pregunta, idx) => (
            <div
              key={pregunta.id}
              className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition"
            >
              {/* Número de pregunta */}
              <div className="flex items-start mb-4">
                <div className="w-8 h-8 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold mr-4 flex-shrink-0">
                  {idx + 1}
                </div>
                <h3 className="text-lg font-semibold text-gray-900 flex-grow">
                  {pregunta.pregunta}
                </h3>
              </div>

              {/* Opciones */}
              {pregunta.opciones && pregunta.opciones.length > 0 ? (
                <div className="space-y-3 ml-12">
                  {pregunta.opciones.map((opcion, idx) => (
                    <label
                      key={idx}
                      className="flex items-center p-3 border-2 border-gray-200 rounded-lg cursor-pointer hover:border-blue-500 hover:bg-blue-50 transition"
                    >
                      <input
                        type="radio"
                        name={pregunta.id}
                        value={String.fromCharCode(65 + idx)} // A, B, C, D...
                        checked={respuestas[pregunta.id] === String.fromCharCode(65 + idx)}
                        onChange={(e) => handleRespuesta(pregunta.id, e.target.value)}
                        className="w-5 h-5 text-blue-600"
                      />
                      <span className="ml-3 text-gray-700">{opcion}</span>
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
                        className="w-5 h-5 text-blue-600"
                      />
                      <span className="text-xs text-gray-600 mt-2">
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
            className="bg-gradient-to-r from-yellow-400 to-yellow-500 hover:from-yellow-500 hover:to-yellow-600 text-gray-900 font-bold py-3 px-8 rounded-lg shadow-lg hover:shadow-xl transition disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {guardando ? 'Guardando...' : testActual === totalTests - 1 ? 'Finalizar' : 'Siguiente'}
          </button>
        </div>

        {/* Info */}
        <div className="mt-8 text-center text-blue-100 text-sm">
          <p>Tus respuestas se guardan automáticamente</p>
        </div>
      </div>
    </div>
  );
}
