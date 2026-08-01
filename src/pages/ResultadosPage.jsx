/**
 * CENERH RECRUIT OS - Página de Resultados
 *
 * El candidato NUNCA ve su score, clasificación ni desglose por test/categoría
 * -- esa información es solo para el reclutador (ver CandidatoAssessments.jsx).
 *
 * Esta pantalla solo confirma que el proceso de evaluación terminó (y de paso
 * dispara el cálculo final del score en el backend) -- luego devuelve al
 * candidato a "Mis aplicaciones", que es donde vive el seguimiento de estatus
 * y el pago de resultados de cada aplicación (ver MisAplicacionesPage.jsx).
 */

import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { candidatosAPI, authAPI } from '../services/api';
import { FONT_SANS, FONT_SERIF } from '../theme';

const SEGUNDOS_ANTES_DE_REDIRIGIR = 2500;

export default function ResultadosPage() {
  const navigate = useNavigate();
  const [listo, setListo] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const candidatoId = localStorage.getItem('candidatoId');
  const candidatoNombre = localStorage.getItem('candidatoNombre');

  useEffect(() => {
    if (!candidatoId) {
      navigate('/');
      return;
    }

    (async () => {
      try {
        await candidatosAPI.obtenerResultados(candidatoId);
        setListo(true);
      } catch (err) {
        setError('Error al finalizar tu evaluación');
        console.error(err);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  useEffect(() => {
    if (!listo || !authAPI.estaAutenticado()) return;
    const timer = setTimeout(() => navigate('/mis-aplicaciones'), SEGUNDOS_ANTES_DE_REDIRIGIR);
    return () => clearTimeout(timer);
  }, [listo]);

  if (loading) {
    return (
      <div className="min-h-screen bg-[#0D0D0D] flex items-center justify-center" style={FONT_SANS}>
        <div className="text-white text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-[#C9A14A] mb-4"></div>
          <p>Finalizando tu evaluación...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-[#0D0D0D] flex items-center justify-center" style={FONT_SANS}>
        <div className="border border-[#2a2a2a] p-8 text-center max-w-md">
          <p className="text-[#D62828] mb-4">{error}</p>
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
    <div className="min-h-screen bg-[#0D0D0D] flex items-center justify-center p-4" style={FONT_SANS}>
      <div className="border border-[#2a2a2a] p-10 text-center max-w-md">
        <div className="text-3xl font-semibold text-white mb-2" style={FONT_SERIF}>¡Evaluación Completa!</div>
        <p className="text-[#B8BFC7] mb-6">Hola, {candidatoNombre}. Tu proceso de evaluación ha finalizado.</p>

        {authAPI.estaAutenticado() ? (
          <>
            <p className="text-[#666] text-sm mb-6">Te llevamos a tus aplicaciones en un momento...</p>
            <Link
              to="/mis-aplicaciones"
              className="inline-block bg-[#D62828] hover:bg-[#b91f1f] text-white font-bold tracking-wide py-3 px-8 transition"
            >
              IR A MIS APLICACIONES AHORA
            </Link>
          </>
        ) : (
          <p className="text-[#B8BFC7] text-sm">
            <Link to="/login-candidato" className="text-[#C9A14A] hover:text-white underline">Inicia sesión</Link>
            {' '}para ver el estatus de tu proceso y tus resultados.
          </p>
        )}
      </div>
    </div>
  );
}
