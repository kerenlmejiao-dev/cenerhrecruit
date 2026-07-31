/**
 * CENERH RECRUIT OS - Login de Candidato
 * Para volver a entrar con email + contraseña en vez de llenar todo de nuevo.
 */

import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { authAPI } from '../services/api';
import { FONT_SANS, FONT_SERIF } from '../theme';

export default function LoginCandidatoPage() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({ email: '', password: '' });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const { usuario } = await authAPI.login(formData.email, formData.password);
      if (usuario.rol !== 'candidato') {
        authAPI.logout();
        setError('Esta cuenta no es de candidato. Si eres reclutador o empresa, inicia sesión aquí.');
        return;
      }
      navigate('/mis-aplicaciones');
    } catch (err) {
      setError('Email o contraseña incorrectos.');
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
            <p className="text-[#B8BFC7] text-xs mt-4">Portal de Candidatos</p>
          </div>

          <div className="p-8">
            <h1 className="text-2xl font-semibold text-white mb-2" style={FONT_SERIF}>Iniciar sesión</h1>
            <p className="text-[#B8BFC7] text-sm mb-6">
              Consulta el estado de tus aplicaciones sin llenar todo de nuevo
            </p>

            {error && (
              <div className="border border-[#D62828] text-[#D62828] px-4 py-3 mb-6 text-sm">
                {error}
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-[#B8BFC7] mb-1">Email</label>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-2.5 bg-[#0D0D0D] border border-[#2a2a2a] text-white rounded focus:ring-1 focus:ring-[#C9A14A] focus:border-[#C9A14A] outline-none transition placeholder:text-[#555]"
                  placeholder="tu@email.com"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-[#B8BFC7] mb-1">Contraseña</label>
                <input
                  type="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-2.5 bg-[#0D0D0D] border border-[#2a2a2a] text-white rounded focus:ring-1 focus:ring-[#C9A14A] focus:border-[#C9A14A] outline-none transition placeholder:text-[#555]"
                  placeholder="••••••••"
                />
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full bg-[#D62828] hover:bg-[#b91f1f] text-white font-bold tracking-wide py-3 transition disabled:opacity-50 disabled:cursor-not-allowed mt-6"
              >
                {loading ? 'INGRESANDO...' : 'INGRESAR'}
              </button>

              <p className="text-sm text-center mt-2 text-[#B8BFC7]">
                ¿No tienes cuenta todavía?{' '}
                <Link to="/aplicar" className="text-[#C9A14A] hover:text-white font-medium">
                  Ver vacantes disponibles
                </Link>
              </p>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
