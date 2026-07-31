/**
 * Portal Reclutador - Crear vacante con selector de tests del banco
 */

import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { reclutadorAPI } from '../../services/api';
import { FONT_SANS, FONT_SERIF } from '../../theme';

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

  const inputClass = "w-full px-4 py-2 bg-[#0D0D0D] border border-[#2a2a2a] text-white rounded focus:ring-1 focus:ring-[#C9A14A] focus:border-[#C9A14A] outline-none placeholder:text-[#555]";
  const labelClass = "block text-sm font-medium text-[#B8BFC7] mb-1";

  return (
    <div className="min-h-screen bg-[#0D0D0D]" style={FONT_SANS}>
      <div className="border-b border-[#2a2a2a]">
        <div className="max-w-4xl mx-auto px-4 py-6">
          <Link to="/reclutador" className="text-[#666] hover:text-white text-sm">← Volver al dashboard</Link>
          <h1 className="text-3xl font-semibold text-white mt-2" style={FONT_SERIF}>Nueva Vacante</h1>
          <p className="text-[#B8BFC7] mt-1">Define la vacante y selecciona los tests del banco</p>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 py-8">
        {error && (
          <div className="border border-[#D62828] text-[#D62828] px-4 py-3 mb-6">{error}</div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="border border-[#2a2a2a] p-6 space-y-4">
            <h2 className="text-lg font-semibold text-white" style={FONT_SERIF}>Datos de la vacante</h2>

            <div>
              <label className={labelClass}>Nombre de la vacante *</label>
              <input
                type="text" name="nombre" value={formData.nombre} onChange={handleChange} required
                className={inputClass}
                placeholder="Ej: Contador General"
              />
            </div>

            <div>
              <label className={labelClass}>Cliente *</label>
              <input
                type="text" name="cliente" value={formData.cliente} onChange={handleChange} required
                className={inputClass}
                placeholder="Ej: Constructora XYZ"
              />
            </div>

            <div>
              <label className={labelClass}>Descripción</label>
              <textarea
                name="descripcion" value={formData.descripcion} onChange={handleChange} rows="3"
                className={inputClass}
              />
            </div>

            <div>
              <label className={labelClass}>Empresa cliente</label>
              <select
                name="empresa_id" value={formData.empresa_id} onChange={handleChange}
                className={inputClass}
              >
                <option value="">Sin asociar todavía</option>
                {empresas.map(e => (
                  <option key={e.id} value={e.id}>{e.nombre}</option>
                ))}
              </select>
              <Link to="/reclutador/empresas/nueva" className="text-xs text-[#C9A14A] hover:text-white mt-1 inline-block">
                + Crear nueva empresa cliente
              </Link>
            </div>

            <div>
              <label className={labelClass}>Requisitos / competencias necesarias para la posición</label>
              <textarea
                name="requisitos" value={formData.requisitos} onChange={handleChange} rows="3"
                className={inputClass}
                placeholder="Ej: 3+ años en compras, experiencia negociando con proveedores, disponibilidad de viajar, residir en Santo Domingo..."
              />
              <p className="text-xs text-[#666] mt-1">Se usa para el análisis de compatibilidad candidato-vacante.</p>
            </div>
          </div>

          <div className="border border-[#2a2a2a] p-6">
            <h2 className="text-lg font-semibold text-white mb-1" style={FONT_SERIF}>Tests psicométricos</h2>
            <p className="text-sm text-[#B8BFC7] mb-4">Selecciona los tests que aplicarán los candidatos ({testsSeleccionados.length} seleccionados)</p>

            {cargandoBanco ? (
              <p className="text-[#666]">Cargando banco de tests...</p>
            ) : (
              <div className="space-y-5">
                {Object.entries(categorias).map(([categoria, tests]) => (
                  <div key={categoria}>
                    <h3 className="text-sm font-bold text-[#C9A14A] uppercase tracking-wide mb-2">{categoria}</h3>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                      {tests.map(test => (
                        <label
                          key={test.id}
                          className={`flex items-start p-3 border cursor-pointer transition ${
                            testsSeleccionados.includes(test.id)
                              ? 'border-[#D62828] bg-[#D62828]/10'
                              : 'border-[#2a2a2a] hover:border-[#3a3a3a]'
                          }`}
                        >
                          <input
                            type="checkbox"
                            checked={testsSeleccionados.includes(test.id)}
                            onChange={() => toggleTest(test.id)}
                            className="w-5 h-5 accent-[#D62828] mt-0.5"
                          />
                          <span className="ml-3">
                            <span className="block font-medium text-white text-sm">{test.nombre}</span>
                            <span className="block text-xs text-[#666]">{test.num_preguntas} preguntas</span>
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
            <div className="border border-[#2a2a2a] p-6">
              <h2 className="text-lg font-semibold text-white mb-1" style={FONT_SERIF}>Assessment Centers (evaluados por IA)</h2>
              <p className="text-sm text-[#B8BFC7] mb-4">Escenarios de respuesta abierta para roles estratégicos (opcional)</p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                {assessments.map(a => (
                  <label
                    key={a.id}
                    className={`flex items-start p-3 border cursor-pointer transition ${
                      assessmentsSeleccionados.includes(a.id)
                        ? 'border-[#0050A0] bg-[#0050A0]/10'
                        : 'border-[#2a2a2a] hover:border-[#3a3a3a]'
                    }`}
                  >
                    <input
                      type="checkbox"
                      checked={assessmentsSeleccionados.includes(a.id)}
                      onChange={() => toggleAssessment(a.id)}
                      className="w-5 h-5 accent-[#0050A0] mt-0.5"
                    />
                    <span className="ml-3">
                      <span className="block font-medium text-white text-sm">{a.nombre}</span>
                      <span className="block text-xs text-[#666]">{a.categoria}</span>
                    </span>
                  </label>
                ))}
              </div>
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-[#D62828] hover:bg-[#b91f1f] text-white font-bold tracking-wide py-3 transition disabled:opacity-50"
          >
            {loading ? 'CREANDO...' : 'CREAR VACANTE'}
          </button>
        </form>
      </div>
    </div>
  );
}
