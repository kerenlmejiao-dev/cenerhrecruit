/**
 * CENERH RECRUIT OS - Página de Registro
 * Donde candidatos se registran y comienzan la evaluación
 */

import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { candidatosAPI } from '../services/api';

export default function RegistroPage() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    nombre: '',
    email: '',
    telefono: '',
    vacante_id: 'contador_paraiso',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const resultado = await candidatosAPI.crear(formData);
      
      // Guardar candidato ID en localStorage
      localStorage.setItem('candidatoId', resultado.candidato_id);
      localStorage.setItem('candidatoNombre', resultado.nombre);

      // Redirigir a página de tests
      navigate('/tests');
    } catch (err) {
      setError('Error al registrar. Intenta nuevamente.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-blue-900 flex items-center justify-center p-4">
      {/* Container */}
      <div className="w-full max-w-md">
        {/* Card */}
        <div className="bg-white rounded-lg shadow-2xl overflow-hidden">
          {/* Header */}
          <div className="bg-gradient-to-r from-blue-600 to-blue-800 px-6 py-8 text-center">
            <div className="text-4xl font-bold text-white mb-2">CENERH</div>
            <div className="text-sm text-blue-100">CONSULTING</div>
            <p className="text-blue-100 text-xs mt-2">Evaluación Estratégica de Gestión Humana</p>
          </div>

          {/* Body */}
          <div className="p-8">
            <h1 className="text-2xl font-bold text-gray-900 mb-2">Bienvenido</h1>
            <p className="text-gray-600 text-sm mb-6">
              Completa el formulario para comenzar tu evaluación
            </p>

            {error && (
              <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6 text-sm">
                {error}
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
              {/* Nombre */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Nombre Completo *
                </label>
                <input
                  type="text"
                  name="nombre"
                  value={formData.nombre}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
                  placeholder="Tu nombre completo"
                />
              </div>

              {/* Email */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Email *
                </label>
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

              {/* Teléfono */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Teléfono
                </label>
                <input
                  type="tel"
                  name="telefono"
                  value={formData.telefono}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
                  placeholder="+1-809-000-0000"
                />
              </div>

              {/* Vacante */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Posición *
                </label>
                <select
                  name="vacante_id"
                  value={formData.vacante_id}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
                >
                  <option value="contador_paraiso">Contador General</option>
                  <option value="ingeniero_procesos">Ingeniero de Procesos</option>
                  <option value="gerente_operativo">Gerente Operativo</option>
                </select>
              </div>

              {/* Botón */}
              <button
                type="submit"
                disabled={loading}
                className="w-full bg-gradient-to-r from-blue-600 to-blue-800 text-white font-semibold py-2.5 rounded-lg hover:from-blue-700 hover:to-blue-900 transition disabled:opacity-50 disabled:cursor-not-allowed mt-6"
              >
                {loading ? 'Registrando...' : 'Comenzar Evaluación'}
              </button>

              {/* Nota */}
              <p className="text-xs text-gray-500 text-center mt-4">
                * Campos requeridos. Tu información será confidencial.
              </p>
            </form>
          </div>

          {/* Footer */}
          <div className="bg-gray-50 px-6 py-4 text-center text-xs text-gray-500 border-t">
            <p>© 2026 CENERH Consulting. Todos los derechos reservados.</p>
          </div>
        </div>
      </div>
    </div>
  );
}
