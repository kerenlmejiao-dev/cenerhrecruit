/**
 * Portal Reclutador - Detalle de vacante: tests aplicados + candidatos
 */

import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { candidatosAPI, reclutadorAPI } from '../../services/api';

const STATUS_RECLUTAMIENTO = [
  'Aplicación recibida',
  'En evaluación',
  'Preseleccionado',
  'Entrevista',
  'Decisión final',
  'Contratado',
  'Rechazado',
];

export default function VacanteDetalle() {
  const { vacanteId } = useParams();
  const [vacante, setVacante] = useState(null);
  const [candidatos, setCandidatos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [descargando, setDescargando] = useState('');
  const [descargandoCV, setDescargandoCV] = useState('');
  const [cambiandoEstado, setCambiandoEstado] = useState(false);
  const [cambiandoStatus, setCambiandoStatus] = useState('');
  const [linkCopiado, setLinkCopiado] = useState(false);
  const [sugerencias, setSugerencias] = useState(null);
  const [cargandoSugerencias, setCargandoSugerencias] = useState(false);
  const [errorSugerencias, setErrorSugerencias] = useState('');

  useEffect(() => {
    cargarDatos();
  }, [vacanteId]);

  const cargarDatos = async () => {
    try {
      const [detalle, candidatosData] = await Promise.all([
        reclutadorAPI.detalleVacante(vacanteId),
        reclutadorAPI.candidatosVacante(vacanteId),
      ]);
      setVacante(detalle);
      setCandidatos(candidatosData.candidatos);
    } catch (err) {
      setError('Error al cargar la vacante');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const descargarFicha = async (candidato) => {
    setError('');
    setDescargando(candidato.id);
    try {
      const pdfBlob = await candidatosAPI.generarPDF(candidato.id);
      const url = window.URL.createObjectURL(pdfBlob);
      const enlace = document.createElement('a');
      enlace.href = url;
      enlace.download = `Ficha_${candidato.nombre.replace(/\s+/g, '_')}.pdf`;
      document.body.appendChild(enlace);
      enlace.click();
      enlace.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setError('No se pudo generar la ficha. El candidato debe tener al menos un test completado.');
      console.error(err);
    } finally {
      setDescargando('');
    }
  };

  const descargarCV = async (candidato) => {
    setError('');
    setDescargandoCV(candidato.id);
    try {
      const { blob, filename } = await reclutadorAPI.descargarCV(candidato.id);
      const url = window.URL.createObjectURL(blob);
      const enlace = document.createElement('a');
      enlace.href = url;
      enlace.download = filename;
      document.body.appendChild(enlace);
      enlace.click();
      enlace.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setError('No se pudo descargar el CV.');
      console.error(err);
    } finally {
      setDescargandoCV('');
    }
  };

  const linkAplicar = `${window.location.origin}/aplicar/${vacanteId}`;

  const cambiarEstadoVacante = async (nuevoEstado) => {
    setError('');
    setCambiandoEstado(true);
    try {
      await reclutadorAPI.cambiarEstadoVacante(vacanteId, nuevoEstado);
      setVacante(prev => ({ ...prev, estado: nuevoEstado }));
    } catch (err) {
      setError('No se pudo actualizar el estado de la vacante.');
      console.error(err);
    } finally {
      setCambiandoEstado(false);
    }
  };

  const copiarLink = async () => {
    try {
      await navigator.clipboard.writeText(linkAplicar);
      setLinkCopiado(true);
      setTimeout(() => setLinkCopiado(false), 2000);
    } catch (err) {
      console.error('No se pudo copiar el link:', err);
    }
  };

  const buscarSugerenciasBolsa = async () => {
    setErrorSugerencias('');
    setCargandoSugerencias(true);
    try {
      const data = await reclutadorAPI.sugerenciasBolsa(vacanteId);
      setSugerencias(data.sugerencias);
    } catch (err) {
      setErrorSugerencias('No se pudieron cargar sugerencias.');
      console.error(err);
    } finally {
      setCargandoSugerencias(false);
    }
  };

  const cambiarStatusCandidato = async (candidatoId, status) => {
    setError('');
    setCambiandoStatus(candidatoId);
    try {
      await reclutadorAPI.cambiarStatusCandidato(candidatoId, status);
      setCandidatos(prev => prev.map(c => c.id === candidatoId ? { ...c, status_reclutamiento: status } : c));
    } catch (err) {
      setError('No se pudo actualizar el status del candidato.');
      console.error(err);
    } finally {
      setCambiandoStatus('');
    }
  };

  const getClasificacionColor = (clasificacion) => {
    const colores = {
      PRIORITARIO: 'bg-green-100 text-green-700',
      VIABLE: 'bg-blue-100 text-blue-700',
      CONSIDERAR: 'bg-yellow-100 text-yellow-700',
      NO_RECOMENDADO: 'bg-red-100 text-red-700',
    };
    return colores[clasificacion] || 'bg-gray-100 text-gray-700';
  };

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center text-gray-600">Cargando...</div>;
  }

  if (error || !vacante) {
    return <div className="min-h-screen flex items-center justify-center text-red-600">{error || 'Vacante no encontrada'}</div>;
  }

  const numColumnas = 9;

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white shadow">
        <div className="max-w-6xl mx-auto px-4 py-6">
          <Link to="/reclutador" className="text-sm text-blue-600 hover:text-blue-800">&larr; Volver al dashboard</Link>
          <div className="flex items-start justify-between gap-4 mt-2">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">{vacante.nombre}</h1>
              <p className="text-gray-600">{vacante.cliente}</p>
            </div>
            <div className="text-right">
              <span className={`inline-block px-3 py-1 rounded-full text-xs font-semibold mb-2 ${
                vacante.estado === 'activa' ? 'bg-green-100 text-green-700' :
                vacante.estado === 'inactiva' ? 'bg-red-100 text-red-700' :
                'bg-gray-100 text-gray-600'
              }`}>
                {vacante.estado === 'activa' ? 'Activa' : vacante.estado === 'inactiva' ? 'Inactiva (proceso finalizado)' : 'Borrador (proceso no iniciado)'}
              </span>
              <br />
              {vacante.estado === 'borrador' && (
                <button
                  onClick={() => cambiarEstadoVacante('activa')}
                  disabled={cambiandoEstado}
                  className="px-4 py-2 rounded-lg font-medium text-sm transition disabled:opacity-50 bg-green-600 text-white hover:bg-green-700"
                >
                  {cambiandoEstado ? 'Actualizando...' : 'Abrir proceso de búsqueda'}
                </button>
              )}
              {vacante.estado === 'activa' && (
                <button
                  onClick={() => cambiarEstadoVacante('inactiva')}
                  disabled={cambiandoEstado}
                  className="px-4 py-2 rounded-lg font-medium text-sm transition disabled:opacity-50 bg-white border border-gray-300 text-gray-700 hover:bg-gray-50"
                >
                  {cambiandoEstado ? 'Actualizando...' : 'Finalizar proceso'}
                </button>
              )}
              {vacante.estado === 'inactiva' && (
                <button
                  onClick={() => cambiarEstadoVacante('activa')}
                  disabled={cambiandoEstado}
                  className="px-4 py-2 rounded-lg font-medium text-sm transition disabled:opacity-50 bg-white border border-gray-300 text-gray-700 hover:bg-gray-50"
                >
                  {cambiandoEstado ? 'Actualizando...' : 'Reabrir proceso'}
                </button>
              )}
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-4 py-8 space-y-6">
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">{error}</div>
        )}

        {vacante.estado === 'activa' && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 flex items-center justify-between gap-4 flex-wrap">
            <div>
              <p className="text-sm font-semibold text-blue-900">Link para que los candidatos apliquen</p>
              <p className="text-sm text-blue-700 break-all">{linkAplicar}</p>
            </div>
            <button
              onClick={copiarLink}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg font-medium text-sm hover:bg-blue-700 transition whitespace-nowrap"
            >
              {linkCopiado ? '✓ Copiado' : 'Copiar link'}
            </button>
          </div>
        )}

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-3">Tests aplicados ({vacante.tests.length})</h2>
          <div className="flex flex-wrap gap-2">
            {vacante.tests.map(t => (
              <span key={t.id} className="bg-blue-50 text-blue-700 px-3 py-1 rounded-full text-sm">{t.nombre}</span>
            ))}
          </div>
          {vacante.assessments.length > 0 && (
            <>
              <h3 className="text-sm font-semibold text-gray-700 mt-4 mb-2">Assessment Centers</h3>
              <div className="flex flex-wrap gap-2">
                {vacante.assessments.map(a => (
                  <span key={a.id} className="bg-purple-50 text-purple-700 px-3 py-1 rounded-full text-sm">{a.nombre}</span>
                ))}
              </div>
            </>
          )}
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between gap-4 flex-wrap mb-1">
            <h2 className="text-lg font-semibold text-gray-900">Sugerencias de la Bolsa de Talento</h2>
            <button
              onClick={buscarSugerenciasBolsa}
              disabled={cargandoSugerencias}
              className="bg-purple-600 text-white px-4 py-2 rounded-lg font-medium text-sm hover:bg-purple-700 transition disabled:opacity-50"
            >
              {cargandoSugerencias ? 'Cargando...' : 'Ver candidatos de la Bolsa de Talento'}
            </button>
          </div>
          <p className="text-sm text-gray-500 mb-3">Candidatos de la Bolsa de Talento con su evaluación general (la misma que ve cualquier reclutador o empresa que los revise). No es una aplicación formal — es solo una sugerencia de a quién invitar.</p>

          {errorSugerencias && (
            <div className="bg-amber-50 border border-amber-300 text-amber-800 text-sm px-4 py-3 rounded mb-3">{errorSugerencias}</div>
          )}

          {sugerencias && sugerencias.length === 0 && !errorSugerencias && (
            <p className="text-sm text-gray-500 italic">Nadie se ha registrado en la Bolsa de Talento todavía.</p>
          )}

          {sugerencias && sugerencias.length > 0 && (
            <div className="space-y-3 mt-2">
              {sugerencias.map(s => (
                <div key={s.candidato_id} className="border border-gray-200 rounded-lg p-4 flex items-start justify-between gap-4">
                  <div>
                    <p className="font-semibold text-gray-900 text-sm">{s.nombre}</p>
                    <p className="text-xs text-gray-500 mb-1">{s.email}</p>
                    {s.evaluacion?.tipo === 'perfil_ia' && (
                      <p className="text-sm text-gray-600">{s.evaluacion.resumen}</p>
                    )}
                    {(!s.evaluacion || s.evaluacion.tipo === 'pendiente') && (
                      <p className="text-sm text-gray-400 italic">Sin evaluación todavía</p>
                    )}
                  </div>
                  {s.evaluacion?.tipo === 'pruebas' && (
                    <div className="text-2xl font-bold text-purple-600 whitespace-nowrap">
                      {Math.round(s.evaluacion.score_final)}<span className="text-sm text-gray-400">/100</span>
                    </div>
                  )}
                  {s.evaluacion?.tipo === 'perfil_ia' && (
                    <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded font-medium text-xs whitespace-nowrap">Perfil evaluado (IA)</span>
                  )}
                  {(!s.evaluacion || s.evaluacion.tipo === 'pendiente') && (
                    <span className="bg-gray-200 text-gray-600 px-2 py-1 rounded font-medium text-xs whitespace-nowrap">Pendiente</span>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="bg-white rounded-lg shadow overflow-hidden">
          <div className="px-6 py-4 border-b">
            <h2 className="text-lg font-semibold text-gray-900">Candidatos ({candidatos.length})</h2>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-100 border-b">
                <tr>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Nombre</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Email</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Estado</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Score</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Clasificación</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Status de reclutamiento</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Ficha</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">CV</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Análisis IA</th>
                </tr>
              </thead>
              <tbody>
                {candidatos.length > 0 ? (
                  candidatos.map(c => (
                    <tr key={c.id} className="border-b hover:bg-gray-50">
                      <td className="px-6 py-4 font-medium text-gray-900">{c.nombre}</td>
                      <td className="px-6 py-4 text-gray-600">{c.email}</td>
                      <td className="px-6 py-4 text-gray-600">{c.estado}</td>
                      <td className="px-6 py-4 text-gray-600">{c.score_final ?? '-'}</td>
                      <td className="px-6 py-4">
                        {c.clasificacion && (
                          <span className={`px-3 py-1 rounded-full text-xs font-semibold ${getClasificacionColor(c.clasificacion)}`}>
                            {c.clasificacion}
                          </span>
                        )}
                      </td>
                      <td className="px-6 py-4">
                        <select
                          value={c.status_reclutamiento || 'Aplicación recibida'}
                          onChange={(e) => cambiarStatusCandidato(c.id, e.target.value)}
                          disabled={cambiandoStatus === c.id}
                          className="text-sm border border-gray-300 rounded-lg px-2 py-1 focus:ring-2 focus:ring-blue-500 outline-none disabled:opacity-50"
                        >
                          {STATUS_RECLUTAMIENTO.map(s => (
                            <option key={s} value={s}>{s}</option>
                          ))}
                        </select>
                      </td>
                      <td className="px-6 py-4">
                        <button
                          onClick={() => descargarFicha(c)}
                          disabled={descargando === c.id}
                          className="text-blue-600 hover:text-blue-800 font-medium text-sm disabled:opacity-50"
                        >
                          {descargando === c.id ? 'Generando...' : '📄 PDF'}
                        </button>
                      </td>
                      <td className="px-6 py-4">
                        {c.tiene_cv ? (
                          <button
                            onClick={() => descargarCV(c)}
                            disabled={descargandoCV === c.id}
                            className="text-green-700 hover:text-green-900 font-medium text-sm disabled:opacity-50"
                          >
                            {descargandoCV === c.id ? 'Descargando...' : '📎 CV'}
                          </button>
                        ) : (
                          <span className="text-gray-400 text-sm">Sin CV</span>
                        )}
                      </td>
                      <td className="px-6 py-4">
                        <Link
                          to={`/reclutador/candidatos/${c.id}/assessments`}
                          className="text-purple-600 hover:text-purple-800 font-medium text-sm"
                        >
                          🧩 Ver análisis
                        </Link>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan={numColumnas} className="px-6 py-8 text-center text-gray-500">
                      Ningún candidato se ha postulado todavía
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
