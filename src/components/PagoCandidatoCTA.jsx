/**
 * Tarjeta de pago genérica para las 3 compras del candidato sobre sí mismo:
 * estatus del proceso, resultados, análisis de CV (ver PRODUCTOS_CANDIDATO
 * en dlocal_service.py). Si dLocal exige cédula y todavía no la tenemos, la
 * pide inline antes de reintentar el checkout.
 */

import { useState } from 'react';
import { pagosCandidatoAPI } from '../services/api';

export default function PagoCandidatoCTA({ candidatoId, tipo, precio, titulo, descripcion }) {
  const [procesando, setProcesando] = useState(false);
  const [error, setError] = useState('');
  const [pidiendoDocumento, setPidiendoDocumento] = useState(false);
  const [documento, setDocumento] = useState('');

  const handlePagar = async (documentoActual) => {
    setProcesando(true);
    setError('');
    try {
      const data = await pagosCandidatoAPI.checkout(candidatoId, tipo, documentoActual);
      if (data.checkout_url) {
        window.location.href = data.checkout_url;
        return;
      }
      setError('No se pudo iniciar el pago. Intenta de nuevo.');
    } catch (err) {
      const detail = err.response?.data?.detail || '';
      if (detail.toLowerCase().includes('cédula')) {
        setPidiendoDocumento(true);
      } else {
        setError(detail || 'No se pudo iniciar el pago.');
      }
    } finally {
      setProcesando(false);
    }
  };

  return (
    <div className="border border-[#2a2a2a] p-6 text-center">
      <p className="text-white font-semibold mb-1">{titulo}</p>
      <p className="text-[#B8BFC7] text-sm mb-4">{descripcion}</p>

      {error && <p className="text-[#D62828] text-sm mb-3">{error}</p>}

      {pidiendoDocumento ? (
        <div className="max-w-xs mx-auto">
          <input
            type="text"
            value={documento}
            onChange={(e) => setDocumento(e.target.value)}
            placeholder="Tu cédula"
            className="w-full px-4 py-2.5 bg-[#0D0D0D] border border-[#2a2a2a] text-white text-center mb-3 focus:ring-1 focus:ring-[#C9A14A] focus:border-[#C9A14A] outline-none"
          />
          <button
            onClick={() => handlePagar(documento)}
            disabled={procesando || !documento.trim()}
            className="w-full bg-[#D62828] hover:bg-[#b91f1f] text-white font-bold tracking-wide py-2.5 px-6 transition disabled:opacity-50"
          >
            {procesando ? 'PROCESANDO...' : 'CONTINUAR'}
          </button>
        </div>
      ) : (
        <button
          onClick={() => handlePagar()}
          disabled={procesando}
          className="bg-[#D62828] hover:bg-[#b91f1f] text-white font-bold tracking-wide py-2.5 px-6 transition disabled:opacity-50"
        >
          {procesando ? 'PROCESANDO...' : `DESBLOQUEAR POR RD$${precio}`}
        </button>
      )}
    </div>
  );
}
