/**
 * CENERH RECRUIT OS - Formulario público de referencia laboral
 *
 * Sin login: el token en la URL es la capacidad de acceso. Quien recibe el
 * link (una referencia que dio el candidato) responde unas preguntas
 * cortas sobre su experiencia trabajando con esa persona.
 */

import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { referenciasAPI } from '../services/api';
import { FONT_SANS, FONT_SERIF } from '../theme';

export default function ReferenciaFormPage() {
  const { token } = useParams();
  const [contexto, setContexto] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [enviando, setEnviando] = useState(false);
  const [enviado, setEnviado] = useState(false);
  const [calificacion, setCalificacion] = useState(0);
  const [recontrataria, setRecontrataria] = useState(null);
  const [comentarios, setComentarios] = useState('');

  useEffect(() => {
    (async () => {
      try {
        const data = await referenciasAPI.obtener(token);
        setContexto(data);
      } catch (err) {
        setError('Este link no es válido o ya expiró.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    })();
  }, [token]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!calificacion || recontrataria === null) {
      setError('Completa la calificación y si lo recontratarías antes de enviar.');
      return;
    }
    setError('');
    setEnviando(true);
    try {
      await referenciasAPI.responder(token, {
        calificacion_general: calificacion,
        recontrataria,
        comentarios: comentarios || null,
      });
      setEnviado(true);
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al enviar tu respuesta. Intenta de nuevo.');
      console.error(err);
    } finally {
      setEnviando(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-[#0D0D0D] flex items-center justify-center" style={FONT_SANS}>
        <p className="text-[#B8BFC7]">Cargando...</p>
      </div>
    );
  }

  if (error && !contexto) {
    return (
      <div className="min-h-screen bg-[#0D0D0D] flex items-center justify-center p-4" style={FONT_SANS}>
        <div className="border border-[#2a2a2a] p-8 max-w-md text-center">
          <p className="text-[#D62828]">{error}</p>
          <Link to="/" className="text-[#C9A14A] hover:text-white text-sm underline mt-4 inline-block">Ir al inicio</Link>
        </div>
      </div>
    );
  }

  if (enviado || contexto?.ya_respondida) {
    return (
      <div className="min-h-screen bg-[#0D0D0D] flex items-center justify-center p-4" style={FONT_SANS}>
        <div className="border border-[#2a2a2a] p-8 max-w-md text-center">
          <h1 className="text-2xl font-semibold text-white mb-2" style={FONT_SERIF}>¡Gracias!</h1>
          <p className="text-[#B8BFC7] text-sm">
            Tu respuesta quedó registrada. Gracias por tomarte el tiempo de ayudar a{' '}
            {contexto?.nombre_candidato} en su proceso.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0D0D0D] flex items-center justify-center p-4 py-10" style={FONT_SANS}>
      <div className="w-full max-w-lg">
        <div className="border border-[#2a2a2a] overflow-hidden">
          <div className="border-b border-[#2a2a2a] px-6 py-6 text-center">
            <div className="font-extrabold text-2xl tracking-wide text-white">
              CEN<span className="text-[#D62828]">E</span>RH
            </div>
            <div className="text-[#C9A14A] text-xs tracking-[6px] mt-2">CONSULTING</div>
          </div>

          <div className="p-8">
            <h1 className="text-xl font-semibold text-white mb-2" style={FONT_SERIF}>
              Verificación de referencia laboral
            </h1>
            <p className="text-[#B8BFC7] text-sm mb-6">
              Hola {contexto?.nombre_referencia}, <strong className="text-white">{contexto?.nombre_candidato}</strong> te
              incluyó como referencia. Tu respuesta es confidencial y se comparte solo con el reclutador.
            </p>

            {error && (
              <div className="border border-[#D62828] text-[#D62828] px-4 py-3 mb-6 text-sm">{error}</div>
            )}

            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-[#B8BFC7] mb-2">
                  En general, ¿cómo calificarías su desempeño?
                </label>
                <div className="flex gap-2">
                  {[1, 2, 3, 4, 5].map(n => (
                    <button
                      key={n}
                      type="button"
                      onClick={() => setCalificacion(n)}
                      className={`w-12 h-12 border font-bold transition ${
                        calificacion === n
                          ? 'bg-[#D62828] border-[#D62828] text-white'
                          : 'border-[#2a2a2a] text-[#B8BFC7] hover:border-[#C9A14A]'
                      }`}
                    >
                      {n}
                    </button>
                  ))}
                </div>
                <p className="text-xs text-[#666] mt-1">1 = deficiente, 5 = excelente</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-[#B8BFC7] mb-2">
                  ¿Volverías a contratarlo/a si tuvieras la oportunidad?
                </label>
                <div className="flex gap-3">
                  <button
                    type="button"
                    onClick={() => setRecontrataria(true)}
                    className={`flex-1 py-3 border font-semibold transition ${
                      recontrataria === true
                        ? 'bg-[#0050A0] border-[#0050A0] text-white'
                        : 'border-[#2a2a2a] text-[#B8BFC7] hover:border-[#0050A0]'
                    }`}
                  >
                    Sí
                  </button>
                  <button
                    type="button"
                    onClick={() => setRecontrataria(false)}
                    className={`flex-1 py-3 border font-semibold transition ${
                      recontrataria === false
                        ? 'bg-[#2a2a2a] border-[#666] text-white'
                        : 'border-[#2a2a2a] text-[#B8BFC7] hover:border-[#666]'
                    }`}
                  >
                    No
                  </button>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-[#B8BFC7] mb-2">
                  Comentarios (opcional)
                </label>
                <textarea
                  value={comentarios}
                  onChange={(e) => setComentarios(e.target.value)}
                  rows={4}
                  className="w-full px-4 py-2 bg-[#0D0D0D] border border-[#2a2a2a] text-white rounded focus:ring-1 focus:ring-[#C9A14A] focus:border-[#C9A14A] outline-none placeholder:text-[#555]"
                  placeholder="Cualquier detalle adicional que quieras compartir"
                />
              </div>

              <button
                type="submit"
                disabled={enviando}
                className="w-full bg-[#D62828] hover:bg-[#b91f1f] text-white font-bold tracking-wide py-3 transition disabled:opacity-50"
              >
                {enviando ? 'ENVIANDO...' : 'ENVIAR RESPUESTA'}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
