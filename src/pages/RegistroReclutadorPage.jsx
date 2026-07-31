/**
 * CENERH RECRUIT OS - Autorregistro de reclutador
 * Protegido con un código de invitación (REGISTRO_RECLUTADOR_CODIGO en .env).
 */

import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { authAPI } from '../services/api';

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

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-blue-900 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="bg-white rounded-lg shadow-2xl overflow-hidden">
          <div className="bg-gradient-to-r from-blue-600 to-blue-800 px-6 py-8 text-center">
            <div className="text-4xl font-bold text-white mb-2">CENERH</div>
            <div className="text-sm text-blue-100">CONSULTING</div>
            <p className="text-blue-100 text-xs mt-2">Crear cuenta de reclutador</p>
          </div>

          <div className="p-8">
            <h1 className="text-2xl font-bold text-gray-900 mb-2">Crea tu cuenta</h1>
            <p className="text-gray-600 text-sm mb-6">
              Necesitas un código de invitación para registrarte.
            </p>

            {error && (
              <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6 text-sm">
                {error}
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Nombre completo</label>
                <input
                  type="text" name="nombre" value={formData.nombre} onChange={handleChange} required
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                <input
                  type="email" name="email" value={formData.email} onChange={handleChange} required
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                  placeholder="tu@email.com"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Contraseña</label>
                <input
                  type="password" name="password" value={formData.password} onChange={handleChange} required
                  minLength={8}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                  placeholder="Mínimo 8 caracteres"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Código de invitación</label>
                <input
                  type="text" name="codigo_invitacion" value={formData.codigo_invitacion} onChange={handleChange} required
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                  placeholder="Te lo compartió la administración de CENERH"
                />
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full bg-gradient-to-r from-blue-600 to-blue-800 text-white font-semibold py-2.5 rounded-lg hover:from-blue-700 hover:to-blue-900 transition disabled:opacity-50 mt-6"
              >
                {loading ? 'Creando cuenta...' : 'Crear cuenta'}
              </button>

              <p className="text-sm text-center mt-2">
                ¿Ya tienes cuenta?{' '}
                <Link to="/login" className="text-blue-600 hover:text-blue-800 font-medium">Inicia sesión</Link>
              </p>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
