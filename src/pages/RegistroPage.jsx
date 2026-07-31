/**
 * CENERH RECRUIT OS - Página de Registro
 * Donde candidatos se registran y comienzan la evaluación.
 *
 * Tres modos, según la ruta:
 * - "/"                     -> elige entre todas las vacantes publicadas
 * - "/aplicar/:vacanteId"   -> link directo a una vacante puntual (sin selector)
 * - "/bolsa-de-talento"     -> completa su perfil sin aplicar a una vacante
 */

import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { candidatosAPI, vacantesAPI } from '../services/api';

export default function RegistroPage({ modo = 'normal' }) {
  const navigate = useNavigate();
  const { vacanteId: vacanteIdRuta } = useParams();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [vacantes, setVacantes] = useState([]);
  const [vacanteFija, setVacanteFija] = useState(null);
  const [cargandoVacante, setCargandoVacante] = useState(modo === 'aplicar');
  const [formData, setFormData] = useState({
    nombre: '',
    email: '',
    telefono: '',
    vacante_id: '',
  });

  useEffect(() => {
    if (modo === 'normal') {
      cargarVacantes();
    } else if (modo === 'aplicar' && vacanteIdRuta) {
      cargarVacanteFija();
    }
  }, [modo, vacanteIdRuta]);

  const cargarVacantes = async () => {
    try {
      const data = await vacantesAPI.listar();
      setVacantes(data.vacantes);
      if (data.vacantes.length > 0) {
        setFormData(prev => ({ ...prev, vacante_id: data.vacantes[0].id }));
      }
    } catch (err) {
      console.error('Error cargando vacantes:', err);
    }
  };

  const cargarVacanteFija = async () => {
    setCargandoVacante(true);
    try {
      const config = await vacantesAPI.obtenerConfig(vacanteIdRuta);
      if (config.estado !== 'activa') {
        setError('Esta vacante ya no está disponible para aplicar.');
      } else {
        setVacanteFija(config);
        setFormData(prev => ({ ...prev, vacante_id: vacanteIdRuta }));
      }
    } catch (err) {
      setError('Esta vacante no existe o ya no está disponible.');
      console.error(err);
    } finally {
      setCargandoVacante(false);
    }
  };

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
      const payload = modo === 'bolsa'
        ? { nombre: formData.nombre, email: formData.email, telefono: formData.telefono }
        : formData;
      const resultado = await candidatosAPI.crear(payload);

      localStorage.setItem('candidatoId', resultado.candidato_id);
      localStorage.setItem('candidatoNombre', resultado.nombre);
      if (payload.vacante_id) {
        localStorage.setItem('vacanteId', payload.vacante_id);
      } else {
        localStorage.removeItem('vacanteId');
      }

      // Redirigir al cuestionario + CV. Si es bolsa de talento no hay tests
      // que responder (PerfilPage detecta esto y no intenta avanzar a /tests).
      navigate(resultado.es_bolsa_talento ? '/perfil?retorno=bolsa' : '/perfil');
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al registrar. Intenta nuevamente.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const titulo = modo === 'bolsa' ? 'Únete a nuestra bolsa de talento' : 'Bienvenido';
  const subtitulo = modo === 'bolsa'
    ? 'Completa tu perfil. Te contactaremos cuando surja una posición para ti.'
    : 'Completa el formulario para comenzar tu evaluación';

  if (modo === 'aplicar' && cargandoVacante) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-blue-900 flex items-center justify-center">
        <p className="text-white">Cargando...</p>
      </div>
    );
  }

  if (modo === 'aplicar' && !vacanteFija) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-blue-900 flex items-center justify-center p-4">
        <div className="bg-white rounded-lg shadow-2xl p-8 max-w-md text-center">
          <p className="text-red-600 mb-4">{error || 'Esta vacante no está disponible.'}</p>
          <button onClick={() => navigate('/aplicar')} className="text-blue-600 hover:text-blue-800 font-medium">
            Ver otras vacantes
          </button>
        </div>
      </div>
    );
  }

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
            <h1 className="text-2xl font-bold text-gray-900 mb-2">{titulo}</h1>
            <p className="text-gray-600 text-sm mb-6">{subtitulo}</p>

            {modo === 'aplicar' && vacanteFija && (
              <div className="bg-blue-50 border border-blue-200 rounded-lg px-4 py-3 mb-4">
                <p className="text-sm text-blue-900 font-semibold">{vacanteFija.nombre}</p>
                <p className="text-xs text-blue-700">{vacanteFija.cliente}</p>
              </div>
            )}

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

              {/* Vacante: solo en el modo normal (dropdown de todas las publicadas) */}
              {modo === 'normal' && (
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
                    {vacantes.map(v => (
                      <option key={v.id} value={v.id}>{v.nombre} - {v.cliente}</option>
                    ))}
                  </select>
                </div>
              )}

              {/* Botón */}
              <button
                type="submit"
                disabled={loading}
                className="w-full bg-gradient-to-r from-blue-600 to-blue-800 text-white font-semibold py-2.5 rounded-lg hover:from-blue-700 hover:to-blue-900 transition disabled:opacity-50 disabled:cursor-not-allowed mt-6"
              >
                {loading ? 'Registrando...' : modo === 'bolsa' ? 'Registrar mi perfil' : 'Comenzar Evaluación'}
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
