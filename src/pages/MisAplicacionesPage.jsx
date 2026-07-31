/**
 * CENERH RECRUIT OS - Mis aplicaciones (candidato autenticado)
 *
 * Lista todas las aplicaciones del candidato (una por vacante, más su perfil
 * de bolsa de talento si lo tiene) con su estado de proceso. Nunca muestra
 * score ni clasificación -- eso es solo para el reclutador.
 */

import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { authAPI, candidatosAPI } from '../services/api';
import { FONT_SANS, FONT_SERIF } from '../theme';
import StatusReclutamiento from '../components/StatusReclutamiento';

export default function MisAplicacionesPage() {
  const [aplicaciones, setAplicaciones] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const usuario = authAPI.usuarioActual();

  useEffect(() => {
    (async () => {
      try {
        const data = await candidatosAPI.misAplicaciones();
        setAplicaciones(data.aplicaciones || []);
      } catch (err) {
        setError('No se pudieron cargar tus aplicaciones.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const handleLogout = () => {
    authAPI.logout();
    window.location.href = '/';
  };

  return (
    <div className="min-h-screen bg-[#0D0D0D]" style={FONT_SANS}>
      <div className="max-w-3xl mx-auto px-4 py-12">
        <div className="flex items-start justify-between mb-10">
          <div>
            <h1 className="text-3xl font-semibold text-white" style={FONT_SERIF}>Mis aplicaciones</h1>
            <p className="text-[#B8BFC7] mt-1">Hola, {usuario?.nombre}</p>
          </div>
          <button onClick={handleLogout} className="text-[#666] hover:text-white text-sm">
            Salir
          </button>
        </div>

        {loading && <p className="text-[#666] text-center">Cargando...</p>}
        {error && (
          <div className="border border-[#D62828] text-[#D62828] px-4 py-3 mb-6 text-center">{error}</div>
        )}

        {!loading && !error && aplicaciones.length === 0 && (
          <div className="border border-[#2a2a2a] p-8 text-center">
            <p className="text-white font-semibold mb-2">Todavía no tienes aplicaciones registradas.</p>
            <Link
              to="/aplicar"
              className="inline-block bg-[#D62828] hover:bg-[#b91f1f] text-white font-bold tracking-wide py-3 px-8 transition mt-2"
            >
              VER VACANTES DISPONIBLES
            </Link>
          </div>
        )}

        <div className="space-y-6">
          {aplicaciones.map(a => (
            <div key={a.candidato_id} className="border border-[#2a2a2a] p-6">
              <div className="mb-4">
                <h2 className="text-lg font-bold text-white">
                  {a.vacante_nombre || 'Bolsa de Talento'}
                </h2>
                {a.vacante_cliente && (
                  <p className="text-[#0050A0] text-sm">{a.vacante_cliente}</p>
                )}
              </div>
              {a.vacante_id ? (
                <StatusReclutamiento status={a.status_reclutamiento} />
              ) : (
                <p className="text-[#B8BFC7] text-sm">
                  Tu perfil está en nuestra bolsa de talento. Te contactaremos cuando surja una posición que encaje contigo.
                </p>
              )}
            </div>
          ))}
        </div>

        <p className="text-center text-[#666] text-xs mt-10">
          <Link to="/aplicar" className="text-[#C9A14A] hover:text-white underline">
            Ver otras vacantes disponibles
          </Link>
        </p>
      </div>
    </div>
  );
}
