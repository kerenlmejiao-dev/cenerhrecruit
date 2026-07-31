/**
 * Portal Reclutador - Planes de suscripción (dLocal Checkout Redirect)
 */

import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { authAPI, pagosAPI } from '../../services/api';

export default function SuscripcionPage() {
  const [suscripcion, setSuscripcion] = useState(null);
  const [planes, setPlanes] = useState([]);
  const [documento, setDocumento] = useState('');
  const [loading, setLoading] = useState(true);
  const [procesando, setProcesando] = useState('');
  const [cambiandoRenovacion, setCambiandoRenovacion] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    cargar();
  }, []);

  const cargar = async () => {
    try {
      const [data, perfil] = await Promise.all([
        pagosAPI.obtenerSuscripcion(),
        authAPI.obtenerPerfil(),
      ]);
      setSuscripcion(data.suscripcion);
      setPlanes(data.planes_disponibles);
      setDocumento(perfil.documento || '');
    } catch (err) {
      setError('Error al cargar información de suscripción');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const suscribirse = async (planId) => {
    setError('');
    if (!documento.trim()) {
      setError('Ingresa tu cédula o RNC para procesar el pago');
      return;
    }
    setProcesando(planId);
    try {
      const { checkout_url } = await pagosAPI.crearCheckoutSuscripcion(planId, documento);
      window.location.href = checkout_url;
    } catch (err) {
      if (err.response?.status === 503) {
        setError('Los pagos no están configurados todavía. Contacta a la administración.');
      } else {
        setError(err.response?.data?.detail || 'Error al iniciar el pago. Intenta nuevamente.');
      }
      console.error(err);
      setProcesando('');
    }
  };

  const toggleRenovacionAutomatica = async () => {
    setCambiandoRenovacion(true);
    setError('');
    try {
      const { renovacion_automatica } = await pagosAPI.cambiarRenovacionAutomatica(!suscripcion.renovacion_automatica);
      setSuscripcion(prev => ({ ...prev, renovacion_automatica }));
    } catch (err) {
      setError('No se pudo actualizar la preferencia de renovación.');
      console.error(err);
    } finally {
      setCambiandoRenovacion(false);
    }
  };

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center text-gray-600">Cargando...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white shadow">
        <div className="max-w-5xl mx-auto px-4 py-6">
          <Link to="/reclutador" className="text-sm text-blue-600 hover:text-blue-800">&larr; Volver al dashboard</Link>
          <h1 className="text-3xl font-bold text-gray-900 mt-2">Tu suscripción</h1>
          <p className="text-gray-600 text-sm mt-1">Renovación manual mensual &mdash; recibirás un enlace de pago cada mes</p>
        </div>
      </div>

      <div className="max-w-5xl mx-auto px-4 py-8">
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">{error}</div>
        )}

        {suscripcion && (
          <div className="bg-white rounded-lg shadow p-6 mb-8">
            <h2 className="text-lg font-semibold text-gray-900 mb-2">Plan actual</h2>
            <p className="text-gray-700">
              Plan <strong className="capitalize">{suscripcion.plan}</strong> &mdash; RD${suscripcion.precio_mensual}/mes
            </p>
            {suscripcion.fecha_renovacion && (
              <p className="text-sm text-gray-500 mt-1">Próxima renovación: {new Date(suscripcion.fecha_renovacion).toLocaleDateString()}</p>
            )}
            <span className={`inline-block mt-2 px-3 py-1 rounded-full text-xs font-semibold ${
              suscripcion.estado === 'activa' ? 'bg-green-100 text-green-700' :
              suscripcion.estado === 'vencida' ? 'bg-red-100 text-red-700' :
              'bg-gray-100 text-gray-700'
            }`}>
              {suscripcion.estado}
            </span>

            <div className="mt-4 pt-4 border-t">
              <label className="flex items-center gap-2 text-sm text-gray-700">
                <input
                  type="checkbox"
                  checked={suscripcion.renovacion_automatica}
                  onChange={toggleRenovacionAutomatica}
                  disabled={cambiandoRenovacion}
                  className="w-4 h-4"
                />
                Renovar automáticamente cada mes
              </label>
              <p className="text-xs text-gray-500 mt-1">
                Por ahora esto solo guarda tu preferencia — el cobro automático llega cuando se conecte el método de pago recurrente de dLocal. Mientras tanto, seguirás recibiendo el enlace de pago mensual.
              </p>
            </div>
          </div>
        )}

        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <label className="block text-sm font-medium text-gray-700 mb-1">Cédula o RNC</label>
          <input
            type="text" value={documento} onChange={(e) => setDocumento(e.target.value)}
            className="w-full max-w-xs px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
            placeholder="Requerido para procesar el pago"
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {planes.map(plan => (
            <div key={plan.id} className="bg-white rounded-lg shadow p-6 flex flex-col">
              <h3 className="text-xl font-bold text-gray-900 capitalize mb-1">{plan.nombre}</h3>
              <p className="text-3xl font-bold text-blue-600 mb-4">RD${plan.precio_mensual}<span className="text-sm text-gray-500 font-normal">/mes</span></p>
              <button
                onClick={() => suscribirse(plan.id)}
                disabled={procesando === plan.id}
                className="mt-auto bg-gradient-to-r from-blue-600 to-blue-800 text-white font-semibold py-2.5 rounded-lg hover:from-blue-700 hover:to-blue-900 transition disabled:opacity-50"
              >
                {suscripcion?.plan === plan.id && suscripcion?.estado === 'activa'
                  ? 'Renovar'
                  : procesando === plan.id ? 'Redirigiendo...' : 'Suscribirme'}
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
