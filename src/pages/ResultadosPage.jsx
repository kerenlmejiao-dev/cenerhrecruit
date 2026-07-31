/**
 * CENERH RECRUIT OS - Página de Resultados
 *
 * El candidato NUNCA ve su score, clasificación ni desglose por test/categoría
 * -- esa información es solo para el reclutador (ver CandidatoAssessments.jsx).
 * Aquí solo se muestra en qué etapa va su proceso de reclutamiento.
 */

import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
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

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-blue-900 py-8">
      <div className="max-w-4xl mx-auto px-4">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="text-4xl font-bold text-white mb-2">¡Evaluación Completa!</div>
          <p className="text-blue-100">Hola, {candidatoNombre}</p>
        </div>

        <StatusReclutamiento status={datos.status_reclutamiento} />

        {/* Acciones */}
        <div className="mb-8">
          <button
            onClick={() => navigate('/perfil?retorno=resultados')}
            className="bg-white hover:bg-gray-50 text-blue-600 font-bold py-3 px-6 rounded-lg shadow-lg hover:shadow-xl transition flex items-center justify-center gap-2"
          >
            <span>✏️</span>
            Corregir o actualizar mis datos
          </button>
        </div>

        {/* Info */}
        <div className="bg-blue-50 border-l-4 border-blue-600 p-6 rounded">
          <p className="text-blue-900 font-semibold mb-2">¿Qué sucede ahora?</p>
          <p className="text-blue-800 text-sm">
            Tu proceso de evaluación ha finalizado. Toda la información ha sido entregada a tu
            reclutador, quien la revisará y se comunicará contigo con los siguientes pasos.
          </p>
        </div>
      </div>
    </div>
  );
}
