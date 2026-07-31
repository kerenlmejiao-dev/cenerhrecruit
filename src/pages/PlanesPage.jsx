/**
 * CENERH RECRUIT OS - Planes de membresía (pública, sin login)
 *
 * Se enlaza desde el registro de reclutador ("No tengo código de
 * invitación"). Ningún plan es gratuito -- esto es solo para comparar antes
 * de contactar a CENERH y activar la membresía.
 */

import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { planesAPI } from '../services/api';
import { FONT_SANS, FONT_SERIF } from '../theme';

export default function PlanesPage() {
  const [planes, setPlanes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    (async () => {
      try {
        const data = await planesAPI.listar();
        setPlanes(data.planes || []);
      } catch (err) {
        setError('No se pudieron cargar los planes. Intenta de nuevo en un momento.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  return (
    <div className="min-h-screen bg-[#0D0D0D]" style={FONT_SANS}>
      <div className="max-w-5xl mx-auto px-4 py-16">
        <div className="text-center mb-14">
          <Link to="/" className="text-[#666] hover:text-white text-sm">← Volver al inicio</Link>
          <h1 className="text-3xl md:text-4xl font-semibold text-white mt-4" style={FONT_SERIF}>
            Planes de membresía
          </h1>
          <p className="text-[#B8BFC7] mt-2 max-w-xl mx-auto">
            Todos los planes son de pago. Compara y elige el que mejor se ajuste a ti.
          </p>
        </div>

        {loading && <p className="text-[#666] text-center">Cargando planes...</p>}
        {error && (
          <div className="border border-[#D62828] text-[#D62828] px-4 py-3 mb-6 text-center">{error}</div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {planes.map(plan => (
            <div key={plan.id} className="border border-[#2a2a2a] p-8 flex flex-col">
              <span className="text-[#C9A14A] text-xs font-semibold tracking-wide uppercase mb-2">
                {plan.para === 'empresa' ? 'Para empresas' : 'Para reclutadores'}
              </span>
              <h2 className="text-xl font-bold text-white mb-1">{plan.nombre}</h2>
              <p className="text-3xl font-bold text-white mb-6">
                RD${plan.precio_mensual.toLocaleString('es-DO')}
                <span className="text-sm text-[#666] font-normal">/mes</span>
              </p>
              <ul className="space-y-3 mb-8 flex-grow">
                {plan.caracteristicas.map((c, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-[#B8BFC7]">
                    <span className="text-[#0050A0] font-bold mt-0.5">✓</span>
                    <span>{c}</span>
                  </li>
                ))}
              </ul>
              {plan.para === 'empresa' ? (
                <p className="text-center text-[#666] text-xs border-t border-[#2a2a2a] pt-4">
                  Escríbenos para activar este plan
                </p>
              ) : (
                <Link
                  to="/registro-reclutador"
                  className="text-center bg-[#D62828] hover:bg-[#b91f1f] text-white font-bold tracking-wide py-3 transition"
                >
                  REGISTRARME
                </Link>
              )}
            </div>
          ))}
        </div>

        <div className="border border-[#2a2a2a] p-6 mt-10 text-center">
          <p className="text-white font-semibold mb-1">¿Cómo se activa mi membresía?</p>
          <p className="text-[#B8BFC7] text-sm">
            Regístrate con el código de invitación (o contáctanos si no tienes uno) y confirma tu pago con
            CENERH Consulting. En cuanto se confirme, activamos tu acceso.
          </p>
        </div>
      </div>
    </div>
  );
}
