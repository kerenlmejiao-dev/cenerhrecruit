/**
 * Portal Reclutador - Dashboard de vacantes
 */

import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { authAPI, reclutadorAPI } from '../../services/api';

export default function DashboardReclutador() {
  const navigate = useNavigate();
  const [vacantes, setVacantes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const usuario = authAPI.usuarioActual();

  useEffect(() => {
    cargarVacantes();
  }, []);

  const cargarVacantes = async () => {
    try {
      const data = await reclutadorAPI.listarVacantes();
      setVacantes(data.vacantes);
    } catch (err) {
      setError('Error al cargar vacantes');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    authAPI.logout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Portal Reclutador</h1>
            <p className="text-gray-600 mt-1">Hola, {usuario?.nombre}</p>
          </div>
          <div className="flex gap-3">
            <Link
              to="/reclutador/bolsa-talento"
              className="bg-white border border-purple-600 text-purple-600 px-4 py-2 rounded-lg font-medium hover:bg-purple-50 transition"
            >
              Bolsa de Talento
            </Link>
            <Link
              to="/reclutador/suscripcion"
              className="bg-white border border-blue-600 text-blue-600 px-4 py-2 rounded-lg font-medium hover:bg-blue-50 transition"
            >
              Mi suscripción
            </Link>
            <Link
              to="/reclutador/vacantes/nueva"
              className="bg-blue-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-blue-700 transition"
            >
              + Nueva Vacante
            </Link>
            <button
              onClick={handleLogout}
              className="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg font-medium hover:bg-gray-200 transition"
            >
              Salir
            </button>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8">
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">{error}</div>
        )}

        {loading ? (
          <p className="text-gray-600">Cargando vacantes...</p>
        ) : (
          <div className="bg-white rounded-lg shadow overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-100 border-b">
                  <tr>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Vacante</th>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Cliente</th>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Tests</th>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Candidatos</th>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Estado</th>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {vacantes.length > 0 ? (
                    vacantes.map(v => (
                      <tr key={v.id} className="border-b hover:bg-gray-50">
                        <td className="px-6 py-4 font-medium text-gray-900">{v.nombre}</td>
                        <td className="px-6 py-4 text-gray-600">{v.cliente}</td>
                        <td className="px-6 py-4 text-gray-600">{v.total_tests}</td>
                        <td className="px-6 py-4 text-gray-600">{v.total_candidatos}</td>
                        <td className="px-6 py-4">
                          <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                            v.estado === 'activa' ? 'bg-green-100 text-green-700' :
                            v.estado === 'inactiva' ? 'bg-red-100 text-red-700' :
                            'bg-gray-100 text-gray-600'
                          }`}>
                            {v.estado === 'activa' ? 'Activa' : v.estado === 'inactiva' ? 'Inactiva' : 'Borrador'}
                          </span>
                        </td>
                        <td className="px-6 py-4">
                          <Link to={`/reclutador/vacantes/${v.id}`} className="text-blue-600 hover:text-blue-800 font-medium text-sm">
                            Ver candidatos
                          </Link>
                        </td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan="6" className="px-6 py-8 text-center text-gray-500">
                        No hay vacantes creadas todavía
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )}

        <Link to="/como-usamos-la-ia" target="_blank" className="text-xs text-gray-400 hover:text-gray-600 underline mt-6 inline-block">
          Cómo usamos la IA en este sistema
        </Link>
      </div>
    </div>
  );
}
