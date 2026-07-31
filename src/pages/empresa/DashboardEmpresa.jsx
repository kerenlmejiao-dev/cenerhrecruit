/**
 * Portal Empresa - Dashboard de vacantes (solo lectura, filtrado por empresa)
 */

import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { authAPI, empresaAPI } from '../../services/api';

export default function DashboardEmpresa() {
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
      const data = await empresaAPI.listarVacantes();
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
            <h1 className="text-3xl font-bold text-gray-900">Portal Empresa</h1>
            <p className="text-gray-600 mt-1">Hola, {usuario?.nombre}</p>
          </div>
          <button
            onClick={handleLogout}
            className="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg font-medium hover:bg-gray-200 transition"
          >
            Salir
          </button>
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
                    <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Candidatos</th>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {vacantes.length > 0 ? (
                    vacantes.map(v => (
                      <tr key={v.id} className="border-b hover:bg-gray-50">
                        <td className="px-6 py-4 font-medium text-gray-900">{v.nombre}</td>
                        <td className="px-6 py-4 text-gray-600">{v.total_candidatos}</td>
                        <td className="px-6 py-4">
                          <Link to={`/empresa/vacantes/${v.id}`} className="text-blue-600 hover:text-blue-800 font-medium text-sm">
                            Ver candidatos
                          </Link>
                        </td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan="3" className="px-6 py-8 text-center text-gray-500">
                        No hay vacantes disponibles para tu empresa todavía
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
