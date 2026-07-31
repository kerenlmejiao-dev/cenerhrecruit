/**
 * Portal Reclutador - Métricas del embudo de reclutamiento
 *
 * Cuántos candidatos hay en cada etapa, tasa de conversión a contratado, y
 * tiempo promedio en completar la evaluación. Owner ve todas las vacantes;
 * el reclutador solo las suyas.
 */

import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { reclutadorAPI } from '../../services/api';

const ETAPAS = [
  'Aplicación recibida',
  'En evaluación',
  'Preseleccionado',
  'Entrevista',
  'Decisión final',
  'Contratado',
  'Rechazado',
];

export default function MetricasPage() {
  const [datos, setDatos] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    (async () => {
      try {
        const data = await reclutadorAPI.metricas();
        setDatos(data);
      } catch (err) {
        setError('Error al cargar las métricas.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center text-gray-600">Cargando...</div>;
  }

  const maximo = datos ? Math.max(1, ...ETAPAS.map(e => datos.por_status[e] || 0)) : 1;

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white shadow">
        <div className="max-w-4xl mx-auto px-4 py-6">
          <Link to="/reclutador" className="text-sm text-blue-600 hover:text-blue-800">&larr; Volver al dashboard</Link>
          <h1 className="text-3xl font-bold text-gray-900 mt-2">Métricas del embudo</h1>
          <p className="text-gray-600 mt-1">Cómo avanzan tus candidatos por el proceso de reclutamiento</p>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 py-8">
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">{error}</div>
        )}

        {datos && (
          <>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
              <div className="bg-white rounded-lg shadow p-5 text-center">
                <div className="text-3xl font-bold text-gray-900">{datos.total_candidatos}</div>
                <div className="text-xs text-gray-500 mt-1">Candidatos totales</div>
              </div>
              <div className="bg-white rounded-lg shadow p-5 text-center">
                <div className="text-3xl font-bold text-gray-900">{datos.total_vacantes}</div>
                <div className="text-xs text-gray-500 mt-1">Vacantes</div>
              </div>
              <div className="bg-white rounded-lg shadow p-5 text-center">
                <div className="text-3xl font-bold text-green-600">{datos.tasa_conversion_contratado}%</div>
                <div className="text-xs text-gray-500 mt-1">Tasa de contratación</div>
              </div>
              <div className="bg-white rounded-lg shadow p-5 text-center">
                <div className="text-3xl font-bold text-gray-900">
                  {datos.promedio_dias_evaluacion !== null ? `${datos.promedio_dias_evaluacion}d` : '—'}
                </div>
                <div className="text-xs text-gray-500 mt-1">Días promedio de evaluación</div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Candidatos por etapa</h2>
              {datos.total_candidatos === 0 ? (
                <p className="text-gray-500 text-center py-6">Todavía no tienes candidatos para mostrar métricas.</p>
              ) : (
                <div className="space-y-3">
                  {ETAPAS.map(etapa => {
                    const cantidad = datos.por_status[etapa] || 0;
                    const color = etapa === 'Contratado' ? 'bg-green-500' : etapa === 'Rechazado' ? 'bg-gray-400' : 'bg-blue-500';
                    return (
                      <div key={etapa}>
                        <div className="flex justify-between text-sm mb-1">
                          <span className="text-gray-700">{etapa}</span>
                          <span className="text-gray-500 font-medium">{cantidad}</span>
                        </div>
                        <div className="w-full bg-gray-100 rounded-full h-3">
                          <div
                            className={`h-3 rounded-full ${color} transition-all duration-500`}
                            style={{ width: `${(cantidad / maximo) * 100}%` }}
                          ></div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          </>
        )}
      </div>
    </div>
  );
}
