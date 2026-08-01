/**
 * CENERH RECRUIT OS - Olvidé mi contraseña
 * Sirve para cualquier rol (candidato, reclutador, empresa) -- todos inician
 * sesión con email + contraseña sobre la misma tabla Usuario.
 */

import { useState } from 'react';
import { Link } from 'react-router-dom';
import { authAPI } from '../services/api';
import { FONT_SANS, FONT_SERIF } from '../theme';

export default function OlvidePasswordPage() {
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [enviado, setEnviado] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      await authAPI.olvidePassword(email);
      setEnviado(true);
    } catch (err) {
      setError('No se pudo procesar la solicitud. Intenta de nuevo.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0D0D0D] flex items-center justify-center p-4" style={FONT_SANS}>
      <div className="w-full max-w-md">
        <Link to="/" className="inline-block text-[#666] hover:text-white text-sm mb-4">← Volver al inicio</Link>
        <div className="border border-[#2a2a2a] overflow-hidden">
          <div className="border-b border-[#2a2a2a] px-6 py-8 text-center">
            <div className="font-extrabold text-3xl tracking-wide text-white">
              CEN<span className="text-[#D62828]">E</span>RH
            </div>
            <div className="text-[#C9A14A] text-xs tracking-[6px] mt-2">CONSULTING</div>
          </div>

          <div className="p-8">
            <h1 className="text-2xl font-semibold text-white mb-2" style={FONT_SERIF}>¿Olvidaste tu contraseña?</h1>

            {enviado ? (
              <>
                <p className="text-[#B8BFC7] text-sm mb-6">
                  Si <strong className="text-white">{email}</strong> tiene una cuenta con nosotros, te enviamos un
                  enlace para restablecer tu contraseña. Revisa tu bandeja de entrada (y spam).
                </p>
                <Link to="/login" className="text-[#C9A14A] hover:text-white text-sm underline">Volver a iniciar sesión</Link>
              </>
            ) : (
              <>
                <p className="text-[#B8BFC7] text-sm mb-6">
                  Escribe el correo con el que te registraste y te enviaremos un enlace para crear una nueva contraseña.
                </p>

                {error && (
                  <div className="border border-[#D62828] text-[#D62828] px-4 py-3 mb-6 text-sm">{error}</div>
                )}

                <form onSubmit={handleSubmit} className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-[#B8BFC7] mb-1">Email</label>
                    <input
                      type="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      required
                      className="w-full px-4 py-2.5 bg-[#0D0D0D] border border-[#2a2a2a] text-white rounded focus:ring-1 focus:ring-[#C9A14A] focus:border-[#C9A14A] outline-none placeholder:text-[#555]"
                      placeholder="tu@email.com"
                    />
                  </div>
                  <button
                    type="submit"
                    disabled={loading}
                    className="w-full bg-[#D62828] hover:bg-[#b91f1f] text-white font-bold tracking-wide py-3 transition disabled:opacity-50"
                  >
                    {loading ? 'ENVIANDO...' : 'ENVIAR ENLACE'}
                  </button>
                </form>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
