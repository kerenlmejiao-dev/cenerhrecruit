/**
 * CENERH RECRUIT OS - Vacantes disponibles
 *
 * El candidato ve todas las vacantes activas como tarjetas clicables. Al
 * hacer clic entra a /aplicar/:vacanteId, el formulario específico de esa
 * posición (el mismo que usa el link directo que comparte el reclutador).
 */

import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { vacantesAPI } from '../services/api';
import { FONT_SANS, FONT_SERIF } from '../theme';

export default function VacantesListPage() {
  const [vacantes, setVacantes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    (async () => {
      try {
        const data = await vacantesAPI.listar();
        setVacantes(data.vacantes || []);
      } catch (err) {
        setError('No se pudieron cargar las vacantes. Intenta de nuevo en un momento.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  return (
    <div className="min-h-screen bg-[#0D0D0D]" style={FONT_SANS}>
      <div className="max-w-4xl mx-auto px-4 py-16">
        <div className="text-center mb-12">
          <Link to="/" className="text-[#666] hover:text-white text-sm">← Volver al inicio</Link>
          <h1 className="text-3xl md:text-4xl font-semibold text-white mt-4" style={FONT_SERIF}>
            Vacantes disponibles
          </h1>
          <p className="text-[#B8BFC7] mt-2">Elige la posición que te interesa para aplicar</p>
          <p className="text-[#666] text-xs mt-3">
            ¿Ya aplicaste antes?{' '}
            <Link to="/login-candidato" className="text-[#C9A14A] hover:text-white underline">
              Inicia sesión
            </Link>
          </p>
        </div>

        {loading && <p className="text-[#666] text-center">Cargando vacantes...</p>}

        {error && (
          <div className="border border-[#D62828] text-[#D62828] px-4 py-3 mb-6 text-center">{error}</div>
        )}

        {!loading && !error && vacantes.length === 0 && (
          <div className="border border-[#2a2a2a] p-8 text-center">
            <p className="text-white font-semibold mb-2">No hay vacantes abiertas en este momento.</p>
            <p className="text-[#B8BFC7] text-sm mb-6">
              Puedes unirte a nuestra bolsa de talento y te contactaremos cuando surja una posición que encaje contigo.
            </p>
            <Link
              to="/bolsa-de-talento"
              className="inline-block bg-[#D62828] hover:bg-[#b91f1f] text-white font-bold tracking-wide py-3 px-8 transition"
            >
              UNIRME A LA BOLSA DE TALENTO
            </Link>
          </div>
        )}

        <div className="space-y-4">
          {vacantes.map(v => (
            <Link
              key={v.id}
              to={`/aplicar/${v.id}`}
              className="group block border border-[#2a2a2a] hover:border-[#D62828] p-6 transition-colors duration-300"
            >
              <div className="flex items-center justify-between gap-4">
                <div>
                  <h2 className="text-lg font-bold text-white group-hover:text-[#D62828] transition-colors">{v.nombre}</h2>
                  <p className="text-[#0050A0] text-sm mt-0.5">{v.cliente}</p>
                  {v.descripcion && (
                    <p className="text-[#B8BFC7] text-sm mt-2 line-clamp-2">{v.descripcion}</p>
                  )}
                </div>
                <span className="text-[#C9A14A] text-sm font-semibold whitespace-nowrap tracking-wide">
                  APLICAR →
                </span>
              </div>
            </Link>
          ))}
        </div>

        {!loading && vacantes.length > 0 && (
          <p className="text-center text-[#666] text-xs mt-10">
            ¿No ves una posición para ti?{' '}
            <Link to="/bolsa-de-talento" className="text-[#C9A14A] hover:text-white underline">
              Únete a nuestra bolsa de talento
            </Link>
          </p>
        )}
      </div>
    </div>
  );
}
