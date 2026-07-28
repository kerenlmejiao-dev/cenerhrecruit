/**
 * CENERH RECRUIT OS - Admin Dashboard
 * Panel de control para gestionar candidatos
 */

import { useState, useEffect } from 'react';

export default function AdminDashboard() {
  const [candidatos, setCandidatos] = useState([]);
  const [filtro, setFiltro] = useState('todos');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    cargarCandidatos();
  }, []);

  const cargarCandidatos = async () => {
    // Simular carga de candidatos
    // En producción, hacer request a API
    setTimeout(() => {
      setCandidatos([
        {
          id: 'cand_001',
          nombre: 'Juan García',
          email: 'juan@example.com',
          vacante: 'Contador General',
          score: 85,
          estado: 'prioritario',
          fecha: '2026-01-15',
        },
        {
          id: 'cand_002',
          nombre: 'María López',
          email: 'maria@example.com',
          vacante: 'Contador General',
          score: 72,
          estado: 'viable',
          fecha: '2026-01-14',
        },
        {
          id: 'cand_003',
          nombre: 'Carlos Rodríguez',
          email: 'carlos@example.com',
          vacante: 'Ingeniero de Procesos',
          score: 55,
          estado: 'considerar',
          fecha: '2026-01-13',
        },
      ]);
      setLoading(false);
    }, 1000);
  };

  const getEstadoColor = (estado) => {
    const colores = {
      prioritario: { bg: 'bg-green-100', text: 'text-green-700', label: '⭐⭐⭐ Prioritario' },
      viable: { bg: 'bg-blue-100', text: 'text-blue-700', label: '⭐⭐ Viable' },
      considerar: { bg: 'bg-yellow-100', text: 'text-yellow-700', label: '⭐ Considerar' },
      no_recomendado: { bg: 'bg-red-100', text: 'text-red-700', label: 'No Recomendado' },
    };
    return colores[estado] || colores.considerar;
  };

  const candidatosFiltrados = candidatos.filter(c => {
    if (filtro === 'todos') return true;
    return c.estado === filtro;
  });

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
          <p className="text-gray-600">Cargando datos...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-gray-900">CENERH Admin</h1>
          <p className="text-gray-600 mt-1">Gestión de candidatos y evaluaciones</p>
        </div>
      </div>

      {/* KPIs */}
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <p className="text-gray-600 text-sm font-semibold">Total Candidatos</p>
            <p className="text-3xl font-bold text-gray-900 mt-2">{candidatos.length}</p>
          </div>
          <div className="bg-green-50 rounded-lg shadow p-6 border-l-4 border-green-600">
            <p className="text-green-600 text-sm font-semibold">Prioritarios</p>
            <p className="text-3xl font-bold text-green-700 mt-2">
              {candidatos.filter(c => c.estado === 'prioritario').length}
            </p>
          </div>
          <div className="bg-blue-50 rounded-lg shadow p-6 border-l-4 border-blue-600">
            <p className="text-blue-600 text-sm font-semibold">Viables</p>
            <p className="text-3xl font-bold text-blue-700 mt-2">
              {candidatos.filter(c => c.estado === 'viable').length}
            </p>
          </div>
          <div className="bg-yellow-50 rounded-lg shadow p-6 border-l-4 border-yellow-600">
            <p className="text-yellow-600 text-sm font-semibold">A Considerar</p>
            <p className="text-3xl font-bold text-yellow-700 mt-2">
              {candidatos.filter(c => c.estado === 'considerar').length}
            </p>
          </div>
        </div>

        {/* Filtros */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Filtrar por Estado</h2>
          <div className="flex gap-2 flex-wrap">
            {[
              { value: 'todos', label: 'Todos' },
              { value: 'prioritario', label: 'Prioritarios' },
              { value: 'viable', label: 'Viables' },
              { value: 'considerar', label: 'A Considerar' },
            ].map(opcion => (
              <button
                key={opcion.value}
                onClick={() => setFiltro(opcion.value)}
                className={`px-4 py-2 rounded-lg font-medium transition ${
                  filtro === opcion.value
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {opcion.label}
              </button>
            ))}
          </div>
        </div>

        {/* Tabla de Candidatos */}
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-100 border-b">
                <tr>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Nombre</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Email</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Vacante</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Score</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Estado</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Fecha</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Acciones</th>
                </tr>
              </thead>
              <tbody>
                {candidatosFiltrados.length > 0 ? (
                  candidatosFiltrados.map(candidato => {
                    const estadoInfo = getEstadoColor(candidato.estado);
                    return (
                      <tr key={candidato.id} className="border-b hover:bg-gray-50">
                        <td className="px-6 py-4 font-medium text-gray-900">{candidato.nombre}</td>
                        <td className="px-6 py-4 text-gray-600">{candidato.email}</td>
                        <td className="px-6 py-4 text-gray-600">{candidato.vacante}</td>
                        <td className="px-6 py-4">
                          <div className="flex items-center gap-2">
                            <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center font-bold text-blue-600 text-sm">
                              {candidato.score}
                            </div>
                          </div>
                        </td>
                        <td className="px-6 py-4">
                          <span className={`px-3 py-1 rounded-full text-sm font-semibold ${estadoInfo.bg} ${estadoInfo.text}`}>
                            {estadoInfo.label}
                          </span>
                        </td>
                        <td className="px-6 py-4 text-gray-600 text-sm">{candidato.fecha}</td>
                        <td className="px-6 py-4">
                          <button className="text-blue-600 hover:text-blue-800 font-medium text-sm">
                            Ver PDF
                          </button>
                        </td>
                      </tr>
                    );
                  })
                ) : (
                  <tr>
                    <td colSpan="7" className="px-6 py-8 text-center text-gray-500">
                      No hay candidatos con este filtro
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
