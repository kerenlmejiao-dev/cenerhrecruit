/**
 * Portal Reclutador - Crear vacante con selector de tests del banco
 */

import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { reclutadorAPI } from '../../services/api';

export default function CrearVacante() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [cargandoBanco, setCargandoBanco] = useState(true);
  const [error, setError] = useState('');
  const [categorias, setCategorias] = useState({});
  const [assessments, setAssessments] = useState([]);
  const [empresas, setEmpresas] = useState([]);

  const [formData, setFormData] = useState({ nombre: '', cliente: '', descripcion: '', empresa_id: '', requisitos: '' });
  const [testsSeleccionados, setTestsSeleccionados] = useState([]);
  const [assessmentsSeleccionados, setAssessmentsSeleccionados] = useState([]);

  useEffect(() => {
    cargarBanco();
  }, []);

  const cargarBanco = async () => {
    try {
      const [testsData, assessmentsData, empresasData] = await Promise.all([
        reclutadorAPI.bancoTests(),
        reclutadorAPI.bancoAssessments(),
        reclutadorAPI.listarEmpresas(),
      ]);
      setCategorias(testsData.categorias);
      setAssessments(assessmentsData.assessments);
      setEmpresas(empresasData.empresas);
    } catch (err) {
      setError('Error al cargar el banco de tests');
      console.error(err);
    } finally {
      setCargandoBanco(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const toggleTest = (testId) => {
    setTestsSeleccionados(prev =>
      prev.includes(testId) ? prev.filter(id => id !== testId) : [...prev, testId]
    );
  };

  const toggleAssessment = (assessmentId) => {
    setAssessmentsSeleccionados(prev =>
      prev.includes(assessmentId) ? prev.filter(id => id !== assessmentId) : [...prev, assessmentId]
    );
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (testsSeleccionados.length === 0) {
      setError('Selecciona al menos un test para la vacante');
      return;
    }

    setLoading(true);
    try {
      const resultado = await reclutadorAPI.crearVacante({
        ...formData,
        empresa_id: formData.empresa_id ? parseInt(formData.empresa_id, 10) : null,
        test_ids: testsSeleccionados,
        assessment_ids: assessmentsSeleccionados,
      });
      navigate(`/reclutador/vacantes/${resultado.vacante_id}`);
    } catch (err) {
      setError('Error al crear la vacante. Intenta nuevamente.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white shadow">
        <div className="max-w-4xl mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-gray-900">Nueva Vacante</h1>
          <p className="text-gray-600 mt-1">Define la vacante y selecciona los tests del banco</p>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 py-8">
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">{error}</div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="bg-white rounded-lg shadow p-6 space-y-4">
            <h2 className="text-lg font-semibold text-gray-900">Datos de la vacante</h2>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Nombre de la vacante *</label>
              <input
                type="text" name="nombre" value={formData.nombre} onChange={handleChange} required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                placeholder="Ej: Contador General"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Cliente *</label>
              <input
                type="text" name="cliente" value={formData.cliente} onChange={handleChange} required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                placeholder="Ej: Constructora XYZ"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Descripción</label>
              <textarea
                name="descripcion" value={formData.descripcion} onChange={handleChange} rows="3"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Empresa cliente</label>
              <select
                name="empresa_id" value={formData.empresa_id} onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
              >
                <option value="">Sin asociar todavía</option>
                {empresas.map(e => (
                  <option key={e.id} value={e.id}>{e.nombre}</option>
                ))}
              </select>
              <Link to="/reclutador/empresas/nueva" className="text-xs text-blue-600 hover:text-blue-800 mt-1 inline-block">
                + Crear nueva empresa cliente
              </Link>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Requisitos / competencias necesarias para la posición</label>
              <textarea
                name="requisitos" value={formData.requisitos} onChange={handleChange} rows="3"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                placeholder="Ej: 3+ años en compras, experiencia negociando con proveedores, disponibilidad de viajar, residir en Santo Domingo..."
              />
              <p className="text-xs text-gray-500 mt-1">Se usa para el análisis de compatibilidad candidato-vacante.</p>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-1">Tests psicométricos</h2>
            <p className="text-sm text-gray-500 mb-4">Selecciona los tests que aplicarán los candidatos ({testsSeleccionados.length} seleccionados)</p>

            {cargandoBanco ? (
              <p className="text-gray-500">Cargando banco de tests...</p>
            ) : (
              <div className="space-y-5">
                {Object.entries(categorias).map(([categoria, tests]) => (
                  <div key={categoria}>
                    <h3 className="text-sm font-bold text-gray-700 mb-2">{categoria}</h3>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                      {tests.map(test => (
                        <label
                          key={test.id}
                          className={`flex items-start p-3 border-2 rounded-lg cursor-pointer transition ${
                            testsSeleccionados.includes(test.id)
                              ? 'border-blue-500 bg-blue-50'
                              : 'border-gray-200 hover:border-blue-300'
                          }`}
                        >
                          <input
                            type="checkbox"
                            checked={testsSeleccionados.includes(test.id)}
                            onChange={() => toggleTest(test.id)}
                            className="w-5 h-5 text-blue-600 mt-0.5"
                          />
                          <span className="ml-3">
                            <span className="block font-medium text-gray-900 text-sm">{test.nombre}</span>
                            <span className="block text-xs text-gray-500">{test.num_preguntas} preguntas</span>
                          </span>
                        </label>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {assessments.length > 0 && (
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-1">Assessment Centers (evaluados por IA)</h2>
              <p className="text-sm text-gray-500 mb-4">Escenarios de respuesta abierta para roles estratégicos (opcional)</p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                {assessments.map(a => (
                  <label
                    key={a.id}
                    className={`flex items-start p-3 border-2 rounded-lg cursor-pointer transition ${
                      assessmentsSeleccionados.includes(a.id)
                        ? 'border-blue-500 bg-blue-50'
                        : 'border-gray-200 hover:border-blue-300'
                    }`}
                  >
                    <input
                      type="checkbox"
                      checked={assessmentsSeleccionados.includes(a.id)}
                      onChange={() => toggleAssessment(a.id)}
                      className="w-5 h-5 text-blue-600 mt-0.5"
                    />
                    <span className="ml-3">
                      <span className="block font-medium text-gray-900 text-sm">{a.nombre}</span>
                      <span className="block text-xs text-gray-500">{a.categoria}</span>
                    </span>
                  </label>
                ))}
              </div>
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-gradient-to-r from-blue-600 to-blue-800 text-white font-semibold py-3 rounded-lg hover:from-blue-700 hover:to-blue-900 transition disabled:opacity-50"
          >
            {loading ? 'Creando...' : 'Crear Vacante'}
          </button>
        </form>
      </div>
    </div>
  );
}
