/**
 * CENERH RECRUIT OS - Login de Reclutador / Empresa
 */

import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { authAPI } from '../services/api';

export default function LoginPage() {
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
      if (usuario.rol === 'empresa') {
        navigate('/empresa');
      } else {
        navigate('/reclutador');
      }
    } catch (err) {
      setError('Email o contraseña incorrectos.');
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
            <p className="text-blue-100 text-xs mt-2">Portal de Reclutadores y Empresas</p>
          </div>

          <div className="p-8">
            <h1 className="text-2xl font-bold text-gray-900 mb-2">Iniciar sesión</h1>
            <p className="text-gray-600 text-sm mb-6">
              Acceso exclusivo para reclutadores y empresas registradas
            </p>

            {error && (
              <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6 text-sm">
                {error}
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
                  placeholder="tu@email.com"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Contraseña</label>
                <input
                  type="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
                  placeholder="••••••••"
                />
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full bg-gradient-to-r from-blue-600 to-blue-800 text-white font-semibold py-2.5 rounded-lg hover:from-blue-700 hover:to-blue-900 transition disabled:opacity-50 disabled:cursor-not-allowed mt-6"
              >
                {loading ? 'Ingresando...' : 'Ingresar'}
              </button>

              <p className="text-xs text-gray-500 text-center mt-4">
                Las cuentas de empresa son creadas por la administración de CENERH.
              </p>
              <p className="text-sm text-center mt-2">
                ¿Eres reclutador y no tienes cuenta?{' '}
                <Link to="/registro-reclutador" className="text-blue-600 hover:text-blue-800 font-medium">
                  Crea tu cuenta aquí
                </Link>
              </p>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
