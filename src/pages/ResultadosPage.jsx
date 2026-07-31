/**
 * CENERH RECRUIT OS - Página de Resultados
 *
 * El candidato NUNCA ve su score, clasificación ni desglose por test/categoría
 * -- esa información es solo para el reclutador (ver CandidatoAssessments.jsx).
 * Aquí solo se muestra en qué etapa va su proceso de reclutamiento.
 */

import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { candidatosAPI, authAPI } from '../services/api';
import { FONT_SANS, FONT_SERIF } from '../theme';
import StatusReclutamiento from '../components/StatusReclutamiento';

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
      <div className="min-h-screen bg-[#0D0D0D] flex items-center justify-center" style={FONT_SANS}>
        <div className="text-white text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-[#C9A14A] mb-4"></div>
          <p>Cargando resultados...</p>
        </div>
      </div>
    );
  }

  if (error || !datos) {
    return (
      <div className="min-h-screen bg-[#0D0D0D] flex items-center justify-center" style={FONT_SANS}>
        <div className="border border-[#2a2a2a] p-8 text-center max-w-md">
          <p className="text-[#D62828] mb-4">{error || 'No hay datos disponibles'}</p>
          <button
            onClick={() => navigate('/')}
            className="bg-[#D62828] hover:bg-[#b91f1f] text-white px-6 py-2 font-bold"
          >
            Volver
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0D0D0D] py-8" style={FONT_SANS}>
      <div className="max-w-4xl mx-auto px-4">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="text-4xl font-semibold text-white mb-2" style={FONT_SERIF}>¡Evaluación Completa!</div>
          <p className="text-[#B8BFC7]">Hola, {candidatoNombre}</p>
        </div>

        <div className="mb-8">
          <StatusReclutamiento status={datos.status_reclutamiento} />
        </div>

        {/* Acciones */}
        <div className="mb-8 flex flex-wrap gap-3">
          <button
            onClick={() => navigate('/perfil?retorno=resultados')}
            className="border border-[#2a2a2a] hover:border-[#C9A14A] text-white font-semibold py-3 px-6 transition flex items-center justify-center gap-2"
          >
            <span>✏️</span>
            Corregir o actualizar mis datos
          </button>
          {authAPI.estaAutenticado() && (
            <Link
              to="/mis-aplicaciones"
              className="border border-[#2a2a2a] hover:border-[#C9A14A] text-white font-semibold py-3 px-6 transition flex items-center justify-center gap-2"
            >
              <span>📋</span>
              Ver todas mis aplicaciones
            </Link>
          )}
        </div>

        {/* Info */}
        <div className="border-l-4 border-[#C9A14A] p-6 bg-[#141414]">
          <p className="text-white font-semibold mb-2">¿Qué sucede ahora?</p>
          <p className="text-[#B8BFC7] text-sm">
            Tu proceso de evaluación ha finalizado. Toda la información ha sido entregada a tu
            reclutador, quien la revisará y se comunicará contigo con los siguientes pasos.
          </p>
        </div>
      </div>
    </div>
  );
}
