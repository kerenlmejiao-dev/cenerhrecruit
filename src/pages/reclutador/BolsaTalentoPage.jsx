/**
 * Portal Reclutador - Bolsa de Talento: candidatos que completaron su perfil
 * sin aplicar a una vacante específica. Visible para cualquier reclutador,
 * ya que no pertenecen a una vacante de nadie en particular.
 */

import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { candidatosAPI, reclutadorAPI } from '../../services/api';

export default function BolsaTalentoPage() {
  const [candidatos, setCandidatos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [descargandoCV, setDescargandoCV] = useState('');
  const [solicitando, setSolicitando] = useState('');
  const [solicitados, setSolicitados] = useState(new Set());

  useEffect(() => {
    cargar();
  }, []);

  const cargar = async () => {
    try {
      const data = await reclutadorAPI.bolsaTalento();
      setCandidatos(data.candidatos);
    } catch (err) {
      setError('Error al cargar la bolsa de talento');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const solicitarEvaluacion = async (candidatoId) => {
    setSolicitando(candidatoId);
    setError('');
    try {
      await reclutadorAPI.solicitarEvaluacion(candidatoId);
      setSolicitados(prev => new Set(prev).add(candidatoId));
    } catch (err) {
      setError('No se pudo enviar la solicitud de evaluación.');
      console.error(err);
    } finally {
      setSolicitando('');
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

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center text-gray-600">Cargando...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white shadow">
        <div className="max-w-6xl mx-auto px-4 py-6">
          <Link to="/reclutador" className="text-sm text-blue-600 hover:text-blue-800">&larr; Volver al dashboard</Link>
          <h1 className="text-3xl font-bold text-gray-900 mt-2">Bolsa de Talento</h1>
          <p className="text-gray-600 text-sm mt-1">Personas que completaron su perfil sin aplicar a una vacante todavía</p>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-4 py-8">
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">{error}</div>
        )}

        <div className="bg-white rounded-lg shadow overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-100 border-b">
                <tr>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Nombre</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Email</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Teléfono</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Ciudad</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Último cargo</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Evaluación</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Ficha</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">CV</th>
                </tr>
              </thead>
              <tbody>
                {candidatos.length > 0 ? (
                  candidatos.map(c => (
                    <tr key={c.id} className="border-b hover:bg-gray-50">
                      <td className="px-6 py-4 font-medium text-gray-900">{c.nombre}</td>
                      <td className="px-6 py-4 text-gray-600">{c.email}</td>
                      <td className="px-6 py-4 text-gray-600">{c.telefono || '-'}</td>
                      <td className="px-6 py-4 text-gray-600">{c.ciudad_provincia || '-'}</td>
                      <td className="px-6 py-4 text-gray-600">{c.ultimo_cargo || '-'}</td>
                      <td className="px-6 py-4 text-sm">
                        {c.evaluacion?.tipo === 'pruebas' && (
                          <span className="inline-block bg-green-100 text-green-800 px-2 py-1 rounded font-medium">
                            {Math.round(c.evaluacion.score_final)}/100 — {c.evaluacion.clasificacion}
                          </span>
                        )}
                        {c.evaluacion?.tipo === 'perfil_ia' && (
                          <span
                            className="inline-block bg-blue-100 text-blue-800 px-2 py-1 rounded font-medium cursor-help"
                            title={c.evaluacion.resumen || ''}
                          >
                            Perfil evaluado (IA)
                          </span>
                        )}
                        {(!c.evaluacion || c.evaluacion.tipo === 'pendiente') && (
                          solicitados.has(c.id) ? (
                            <span className="text-gray-500 italic">Solicitud enviada</span>
                          ) : (
                            <div>
                              <span className="inline-block bg-gray-200 text-gray-600 px-2 py-1 rounded font-medium mb-1">
                                Pendiente por evaluación
                              </span>
                              <button
                                onClick={() => solicitarEvaluacion(c.id)}
                                disabled={solicitando === c.id}
                                className="block text-blue-600 hover:text-blue-800 text-xs font-medium disabled:opacity-50"
                              >
                                {solicitando === c.id ? 'Enviando...' : 'Solicitar evaluación'}
                              </button>
                            </div>
                          )
                        )}
                      </td>
                      <td className="px-6 py-4">
                        <a
                          href="#"
                          onClick={async (e) => {
                            e.preventDefault();
                            try {
                              const pdfBlob = await candidatosAPI.generarPDF(c.id);
                              const url = window.URL.createObjectURL(pdfBlob);
                              const enlace = document.createElement('a');
                              enlace.href = url;
                              enlace.download = `Ficha_${c.nombre.replace(/\s+/g, '_')}.pdf`;
                              document.body.appendChild(enlace);
                              enlace.click();
                              enlace.remove();
                              window.URL.revokeObjectURL(url);
                            } catch (err) {
                              setError('No se pudo generar la ficha.');
                              console.error(err);
                            }
                          }}
                          className="text-blue-600 hover:text-blue-800 font-medium text-sm"
                        >
                          📄 PDF
                        </a>
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
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="8" className="px-6 py-8 text-center text-gray-500">
                      Nadie se ha registrado en la bolsa de talento todavía
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
