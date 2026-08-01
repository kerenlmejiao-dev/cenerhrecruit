/**
 * Página de resultado tras volver de dLocal Checkout (suscripción o desbloqueo)
 * dLocal usa un único callback_url; el estado final se confirma consultando
 * el backend (que a su vez verifica contra dLocal si el webhook aún no llegó).
 */

import { useState, useEffect } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { pagosAPI, authAPI } from '../services/api';

export default function PagoResultadoPage() {
  const [searchParams] = useSearchParams();
  const orderId = searchParams.get('order_id');
  const [estado, setEstado] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!orderId) {
      setError('No se encontró información de la transacción');
      setLoading(false);
      return;
    }
    consultar();
  }, [orderId]);

  const consultar = async () => {
    try {
      const data = await pagosAPI.estadoTransaccion(orderId);
      setEstado(data);
    } catch (err) {
      setError('No se pudo verificar el estado del pago');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const usuario = authAPI.usuarioActual();
  const volverA = usuario?.rol === 'empresa' ? '/empresa' : usuario?.rol === 'candidato' ? '/mis-aplicaciones' : '/reclutador';

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center text-gray-600">Verificando el pago...</div>;
  }

  const TITULOS_POR_TIPO = {
    suscripcion: '¡Suscripción activada!',
    desbloqueo_candidato: '¡Candidato desbloqueado!',
    estatus_candidato: '¡Estatus desbloqueado!',
    resultados_candidato: '¡Resultados desbloqueados!',
    analisis_cv_candidato: '¡Análisis de CV desbloqueado!',
  };

  const contenido = (() => {
    if (error || !estado) {
      return { icono: '⚠️', titulo: 'No pudimos verificar el pago', texto: error || 'Intenta consultar tu estado más tarde.' };
    }
    if (estado.estado === 'completada') {
      return {
        icono: estado.tipo === 'suscripcion' ? '✅' : '🔓',
        titulo: TITULOS_POR_TIPO[estado.tipo] || '¡Pago completado!',
        texto: 'Tu pago se procesó correctamente.',
      };
    }
    if (estado.estado === 'fallida') {
      return { icono: '❌', titulo: 'El pago no se completó', texto: 'Puedes intentarlo de nuevo cuando quieras.' };
    }
    return { icono: '⏳', titulo: 'Pago en proceso', texto: 'Estamos confirmando tu pago con dLocal. Puede tardar unos minutos; recarga esta página más tarde.' };
  })();

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-lg p-10 text-center max-w-md">
        <div className="text-5xl mb-4">{contenido.icono}</div>
        <h1 className="text-2xl font-bold text-gray-900 mb-2">{contenido.titulo}</h1>
        <p className="text-gray-600 mb-6">{contenido.texto}</p>
        <Link
          to={volverA}
          className="inline-block bg-blue-600 text-white font-semibold py-2.5 px-6 rounded-lg hover:bg-blue-700 transition"
        >
          Volver al dashboard
        </Link>
      </div>
    </div>
  );
}
