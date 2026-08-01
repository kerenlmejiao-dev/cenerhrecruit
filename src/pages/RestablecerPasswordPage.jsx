/**
 * CENERH RECRUIT OS - Restablecer contraseña
 * Llega desde el enlace del correo de "olvidé mi contraseña" (token en la URL).
 * Al tener éxito, deja la sesión iniciada (mismo patrón que login) y redirige
 * según el rol de la cuenta.
 */

import { useState } from 'react';
import { useNavigate, useParams, Link } from 'react-router-dom';
import { authAPI } from '../services/api';
import { FONT_SANS, FONT_SERIF } from '../theme';

const DESTINO_POR_ROL = {
  candidato: '/mis-aplicaciones',
  empresa: '/empresa',
  reclutador: '/reclutador',
  owner: '/reclutador',
};

export default function RestablecerPasswordPage() {
  const { token } = useParams();
  const navigate = useNavigate();
  const [password, setPassword] = useState('');
  const [confirmar, setConfirmar] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (password.length < 8) {
      setError('La contraseña debe tener al menos 8 caracteres.');
      return;
    }
    if (password !== confirmar) {
      setError('Las contraseñas no coinciden.');
      return;
    }

    setLoading(true);
    try {
      const { usuario } = await authAPI.restablecerPassword(token, password);
      navigate(DESTINO_POR_ROL[usuario.rol] || '/');
    } catch (err) {
      setError(err.response?.data?.detail || 'El enlace es inválido o ya expiró. Solicita uno nuevo.');
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
            <h1 className="text-2xl font-semibold text-white mb-2" style={FONT_SERIF}>Crea tu nueva contraseña</h1>
            <p className="text-[#B8BFC7] text-sm mb-6">Escribe tu nueva contraseña dos veces para confirmar.</p>

            {error && (
              <div className="border border-[#D62828] text-[#D62828] px-4 py-3 mb-6 text-sm">
                {error}{' '}
                <Link to="/olvide-password" className="underline">Solicitar un nuevo enlace</Link>
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-[#B8BFC7] mb-1">Nueva contraseña</label>
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  minLength={8}
                  className="w-full px-4 py-2.5 bg-[#0D0D0D] border border-[#2a2a2a] text-white rounded focus:ring-1 focus:ring-[#C9A14A] focus:border-[#C9A14A] outline-none placeholder:text-[#555]"
                  placeholder="Mínimo 8 caracteres"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-[#B8BFC7] mb-1">Confirma tu contraseña</label>
                <input
                  type="password"
                  value={confirmar}
                  onChange={(e) => setConfirmar(e.target.value)}
                  required
                  minLength={8}
                  className="w-full px-4 py-2.5 bg-[#0D0D0D] border border-[#2a2a2a] text-white rounded focus:ring-1 focus:ring-[#C9A14A] focus:border-[#C9A14A] outline-none placeholder:text-[#555]"
                />
              </div>
              <button
                type="submit"
                disabled={loading}
                className="w-full bg-[#D62828] hover:bg-[#b91f1f] text-white font-bold tracking-wide py-3 transition disabled:opacity-50"
              >
                {loading ? 'GUARDANDO...' : 'GUARDAR NUEVA CONTRASEÑA'}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
