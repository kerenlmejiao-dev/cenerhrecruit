/**
 * CENERH RECRUIT OS - Mis aplicaciones (candidato autenticado)
 *
 * Lista todas las aplicaciones del candidato (una por vacante, más su perfil
 * de bolsa de talento si lo tiene) con su estado de proceso. Nunca muestra
 * score ni clasificación -- eso es solo para el reclutador.
 *
 * Este es el "ambiente" al que el candidato vuelve al terminar su proceso de
 * evaluación (ver ResultadosPage.jsx) -- por eso también vive aquí el pago de
 * resultados (RD$500) por aplicación, además del estatus (RD$200).
 */

import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { authAPI, candidatosAPI, pagosCandidatoAPI } from '../services/api';
import { FONT_SANS, FONT_SERIF } from '../theme';
import StatusReclutamiento from '../components/StatusReclutamiento';
import PagoCandidatoCTA from '../components/PagoCandidatoCTA';

export default function MisAplicacionesPage() {
  const navigate = useNavigate();
  const [aplicaciones, setAplicaciones] = useState([]);
  const [comprasPorId, setComprasPorId] = useState({});
  const [reportesPorId, setReportesPorId] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const usuario = authAPI.usuarioActual();

  useEffect(() => {
    (async () => {
      try {
        const data = await candidatosAPI.misAplicaciones();
        const apps = data.aplicaciones || [];
        setAplicaciones(apps);

        const conVacante = apps.filter(a => a.vacante_id);
        const comprasEntries = await Promise.all(
          conVacante.map(async (a) => {
            try {
              const compras = await pagosCandidatoAPI.compras(a.candidato_id);
              return [a.candidato_id, compras];
            } catch (err) {
              console.error('No se pudieron cargar las compras de', a.candidato_id, err);
              return [a.candidato_id, null];
            }
          })
        );
        const comprasMap = Object.fromEntries(comprasEntries);
        setComprasPorId(comprasMap);

        const conResultadosComprados = conVacante.filter(a => comprasMap[a.candidato_id]?.resultados);
        const reporteEntries = await Promise.all(
          conResultadosComprados.map(async (a) => {
            try {
              const data = await pagosCandidatoAPI.reporteResultados(a.candidato_id);
              return [a.candidato_id, data.reporte];
            } catch (err) {
              console.error('No se pudo cargar el reporte de', a.candidato_id, err);
              return [a.candidato_id, null];
            }
          })
        );
        setReportesPorId(Object.fromEntries(reporteEntries));
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

  const handleCorregirDatos = (candidatoId, nombre) => {
    localStorage.setItem('candidatoId', candidatoId);
    localStorage.setItem('candidatoNombre', nombre);
    navigate('/perfil?retorno=resultados');
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
          {aplicaciones.map(a => {
            const compras = comprasPorId[a.candidato_id];
            const reporte = reportesPorId[a.candidato_id];
            return (
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
                  <>
                    <StatusReclutamiento
                      status={a.status_reclutamiento}
                      desbloqueado={a.estatus_desbloqueado}
                      candidatoId={a.candidato_id}
                    />

                    {compras && (
                      <div className="mt-4">
                        {compras.resultados ? (
                          reporte ? (
                            <div className="border border-[#2a2a2a] p-6">
                              <h3 className="text-sm font-semibold text-[#666] uppercase tracking-wide mb-4">Tus resultados</h3>
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
                                    {reporte.areas_de_oportunidad?.map((ar, i) => <li key={i}>{ar}</li>)}
                                  </ul>
                                </div>
                                {reporte.mensaje && (
                                  <p className="text-white text-sm border-l-4 border-[#C9A14A] pl-4 py-1">{reporte.mensaje}</p>
                                )}
                              </div>
                            </div>
                          ) : (
                            <p className="text-[#666] text-sm">Generando tu reporte de resultados...</p>
                          )
                        ) : (
                          <PagoCandidatoCTA
                            candidatoId={a.candidato_id}
                            tipo="resultados"
                            precio={500}
                            titulo="Recibe tus resultados"
                            descripcion="Por RD$500 recibes un reporte con tus fortalezas y áreas de oportunidad de este proceso."
                          />
                        )}
                      </div>
                    )}

                    <button
                      onClick={() => handleCorregirDatos(a.candidato_id, usuario?.nombre)}
                      className="mt-4 border border-[#2a2a2a] hover:border-[#C9A14A] text-white text-sm font-semibold py-2 px-4 transition"
                    >
                      ✏️ Corregir o actualizar mis datos
                    </button>
                  </>
                ) : (
                  <p className="text-[#B8BFC7] text-sm">
                    Tu perfil está en nuestra bolsa de talento. Te contactaremos cuando surja una posición que encaje contigo.
                  </p>
                )}
              </div>
            );
          })}
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
