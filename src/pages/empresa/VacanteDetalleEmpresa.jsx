/**
 * Portal Empresa - Candidatos de una vacante (solo lectura)
 */

import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { authAPI, empresaAPI } from '../../services/api';

export default function VacanteDetalleEmpresa() {
  const { vacanteId } = useParams();
  const [candidatos, setCandidatos] = useState([]);
  const [documento, setDocumento] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [desbloqueando, setDesbloqueando] = useState('');

  useEffect(() => {
    cargarCandidatos();
    authAPI.obtenerPerfil().then(perfil => setDocumento(perfil.documento || '')).catch(() => {});
  }, [vacanteId]);

  const cargarCandidatos = async () => {
    try {
      const data = await empresaAPI.candidatosVacante(vacanteId);
      setCandidatos(data.candidatos);
    } catch (err) {
      setError('Error al cargar candidatos');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const desbloquear = async (candidatoId) => {
    setError('');
    if (!documento.trim()) {
      setError('Ingresa tu cédula o RNC para procesar el pago');
      return;
    }
    setDesbloqueando(candidatoId);
    try {
      const { checkout_url } = await empresaAPI.desbloquearCandidato(candidatoId, documento);
      window.location.href = checkout_url;
    } catch (err) {
      if (err.response?.status === 503) {
        setError('Los pagos no están configurados todavía. Contacta a la administración.');
      } else {
        setError(err.response?.data?.detail || 'Error al iniciar el pago. Intenta nuevamente.');
      }
      console.error(err);
      setDesbloqueando('');
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

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white shadow">
        <div className="max-w-6xl mx-auto px-4 py-6">
          <Link to="/empresa" className="text-sm text-blue-600 hover:text-blue-800">&larr; Volver al dashboard</Link>
          <h1 className="text-3xl font-bold text-gray-900 mt-2">Candidatos</h1>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-4 py-8">
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">{error}</div>
        )}

        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-1">Cédula o RNC (requerido para desbloquear candidatos)</label>
          <input
            type="text" value={documento} onChange={(e) => setDocumento(e.target.value)}
            className="w-full max-w-xs px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
          />
        </div>

        <div className="bg-white rounded-lg shadow overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-100 border-b">
                <tr>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Candidato</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Estado</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Score</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Clasificación</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Acceso</th>
                </tr>
              </thead>
              <tbody>
                {candidatos.length > 0 ? (
                  candidatos.map(c => (
                    <tr key={c.id} className="border-b hover:bg-gray-50">
                      <td className="px-6 py-4 font-medium text-gray-900">
                        {c.desbloqueado ? c.nombre : `${c.nombre} 🔒`}
                        {c.desbloqueado && c.email && <div className="text-xs text-gray-500">{c.email}</div>}
                      </td>
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
                        {c.desbloqueado ? (
                          <span className="text-green-600 text-sm font-medium">Desbloqueado</span>
                        ) : (
                          <button
                            onClick={() => desbloquear(c.id)}
                            disabled={desbloqueando === c.id}
                            className="bg-yellow-500 hover:bg-yellow-600 text-gray-900 text-sm font-semibold px-3 py-1.5 rounded-lg transition disabled:opacity-50"
                          >
                            {desbloqueando === c.id ? 'Redirigiendo...' : `Desbloquear (RD$${c.precio_desbloqueo ?? 200})`}
                          </button>
                        )}
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="5" className="px-6 py-8 text-center text-gray-500">
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
