/**
 * CENERH RECRUIT OS - Página de Resultados
 *
 * El candidato NUNCA ve su score, clasificación ni desglose por test/categoría
 * -- esa información es solo para el reclutador (ver CandidatoAssessments.jsx).
 * Aquí solo se muestra en qué etapa va su proceso de reclutamiento.
 */

import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { candidatosAPI, authAPI, pagosCandidatoAPI } from '../services/api';
import { FONT_SANS, FONT_SERIF } from '../theme';
import StatusReclutamiento from '../components/StatusReclutamiento';
import PagoCandidatoCTA from '../components/PagoCandidatoCTA';

export default function ResultadosPage() {
  const navigate = useNavigate();
  const [datos, setDatos] = useState(null);
  const [compras, setCompras] = useState(null);
  const [reporte, setReporte] = useState(null);
  const [cargandoReporte, setCargandoReporte] = useState(false);
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
      if (authAPI.estaAutenticado()) {
        const comprasData = await pagosCandidatoAPI.compras(candidatoId);
        setCompras(comprasData);
        if (comprasData.resultados) {
          cargarReporte();
        }
      }
    } catch (err) {
      setError('Error al cargar resultados');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const cargarReporte = async () => {
    setCargandoReporte(true);
    try {
      const data = await pagosCandidatoAPI.reporteResultados(candidatoId);
      setReporte(data.reporte);
    } catch (err) {
      console.error(err);
    } finally {
      setCargandoReporte(false);
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
          {authAPI.estaAutenticado() ? (
            <StatusReclutamiento
              status={datos.status_reclutamiento}
              desbloqueado={datos.estatus_desbloqueado}
              candidatoId={candidatoId}
            />
          ) : (
            <div className="border border-[#2a2a2a] p-6 text-center">
              <p className="text-[#B8BFC7] text-sm">
                <Link to="/login-candidato" className="text-[#C9A14A] hover:text-white underline">Inicia sesión</Link>
                {' '}para ver el estatus de tu proceso.
              </p>
            </div>
          )}
        </div>

        {/* Resultados (RD$500) */}
        {authAPI.estaAutenticado() && (
          <div className="mb-8">
            {!compras ? null : compras.resultados ? (
              <div className="border border-[#2a2a2a] p-6">
                <h2 className="text-sm font-semibold text-[#666] uppercase tracking-wide mb-4">Tus resultados</h2>
                {cargandoReporte && <p className="text-[#B8BFC7] text-sm">Generando tu reporte...</p>}
                {!cargandoReporte && reporte && (
                  <div className="space-y-4">
                    <div>
                      <p className="text-[#C9A14A] font-semibold text-sm mb-2">Fortalezas</p>
                      <ul className="list-disc list-inside text-[#B8BFC7] text-sm space-y-1">
                        {reporte.fortalezas?.map((f, i) => <li key={i}>{f}</li>)}
                      </ul>
                    </div>
                    <div>
                      <p className="text-[#C9A14A] font-semibold text-sm mb-2">Áreas de oportunidad</p>
                      <ul className="list-disc list-inside text-[#B8BFC7] text-sm space-y-1">
                        {reporte.areas_de_oportunidad?.map((a, i) => <li key={i}>{a}</li>)}
                      </ul>
                    </div>
                    {reporte.mensaje && (
                      <p className="text-white text-sm border-l-4 border-[#C9A14A] pl-4 py-1">{reporte.mensaje}</p>
                    )}
                  </div>
                )}
                {!cargandoReporte && !reporte && (
                  <p className="text-[#B8BFC7] text-sm">No pudimos generar tu reporte todavía. Intenta más tarde.</p>
                )}
              </div>
            ) : (
              <PagoCandidatoCTA
                candidatoId={candidatoId}
                tipo="resultados"
                precio={500}
                titulo="Recibe tus resultados"
                descripcion="Por RD$500 recibes un reporte con tus fortalezas y áreas de oportunidad de este proceso."
              />
            )}
          </div>
        )}

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
