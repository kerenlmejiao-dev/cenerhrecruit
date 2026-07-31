/**
 * CENERH RECRUIT OS - Autorregistro de reclutador
 * Protegido con un código de invitación (REGISTRO_RECLUTADOR_CODIGO en .env).
 */

import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { authAPI } from '../services/api';
import { FONT_SANS, FONT_SERIF } from '../theme';

export default function RegistroReclutadorPage() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    nombre: '', email: '', password: '', codigo_invitacion: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      await authAPI.registroReclutador(formData);
      navigate('/reclutador');
    } catch (err) {
      if (err.response?.status === 401) {
        setError('Código de invitación inválido.');
      } else if (err.response?.status === 400) {
        setError(err.response.data.detail || 'Ya existe una cuenta con este email.');
      } else if (err.response?.status === 503) {
        setError('El autorregistro no está habilitado todavía. Contacta a la administración.');
      } else {
        setError('Error al crear la cuenta. Intenta nuevamente.');
      }
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const inputClass = "w-full px-4 py-2.5 bg-[#0D0D0D] border border-[#2a2a2a] text-white rounded focus:ring-1 focus:ring-[#C9A14A] focus:border-[#C9A14A] outline-none placeholder:text-[#555]";
  const labelClass = "block text-sm font-medium text-[#B8BFC7] mb-1";

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
            <p className="text-[#B8BFC7] text-xs mt-4">Crear cuenta de reclutador</p>
          </div>

          <div className="p-8">
            <h1 className="text-2xl font-semibold text-white mb-2" style={FONT_SERIF}>Crea tu cuenta</h1>
            <p className="text-[#B8BFC7] text-sm mb-6">
              Necesitas un código de invitación para registrarte.
            </p>

            {error && (
              <div className="border border-[#D62828] text-[#D62828] px-4 py-3 mb-6 text-sm">
                {error}
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className={labelClass}>Nombre completo</label>
                <input type="text" name="nombre" value={formData.nombre} onChange={handleChange} required className={inputClass} />
              </div>
              <div>
                <label className={labelClass}>Email</label>
                <input
                  type="email" name="email" value={formData.email} onChange={handleChange} required
                  className={inputClass}
                  placeholder="tu@email.com"
                />
              </div>
              <div>
                <label className={labelClass}>Contraseña</label>
                <input
                  type="password" name="password" value={formData.password} onChange={handleChange} required
                  minLength={8}
                  className={inputClass}
                  placeholder="Mínimo 8 caracteres"
                />
              </div>
              <div>
                <label className={labelClass}>Código de invitación</label>
                <input
                  type="text" name="codigo_invitacion" value={formData.codigo_invitacion} onChange={handleChange} required
                  className={inputClass}
                  placeholder="Te lo compartió la administración de CENERH"
                />
                <p className="text-xs text-[#666] mt-1">
                  ¿No tienes código todavía?{' '}
                  <Link to="/planes" className="text-[#C9A14A] hover:text-white underline">
                    Ver planes y membresías
                  </Link>
                </p>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full bg-[#D62828] hover:bg-[#b91f1f] text-white font-bold tracking-wide py-3 transition disabled:opacity-50 mt-6"
              >
                {loading ? 'CREANDO CUENTA...' : 'CREAR CUENTA'}
              </button>

              <p className="text-sm text-center mt-2 text-[#B8BFC7]">
                ¿Ya tienes cuenta?{' '}
                <Link to="/login" className="text-[#C9A14A] hover:text-white font-medium">Inicia sesión</Link>
              </p>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
