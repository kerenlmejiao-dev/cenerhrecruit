/**
 * CENERH RECRUIT OS - Página de Registro
 * Donde candidatos se registran y comienzan la evaluación.
 *
 * Dos modos, según la ruta:
 * - "/aplicar/:vacanteId"   -> link directo a una vacante puntual (compartido
 *                              por el reclutador, o elegido en VacantesListPage)
 * - "/bolsa-de-talento"     -> completa su perfil sin aplicar a una vacante
 */

import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { candidatosAPI, vacantesAPI } from '../services/api';
import { FONT_SANS, FONT_SERIF } from '../theme';

export default function RegistroPage({ modo = 'aplicar' }) {
  const navigate = useNavigate();
  const { vacanteId: vacanteIdRuta } = useParams();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [vacanteFija, setVacanteFija] = useState(null);
  const [cargandoVacante, setCargandoVacante] = useState(modo === 'aplicar');
  const [formData, setFormData] = useState({
    nombre: '',
    email: '',
    telefono: '',
    vacante_id: '',
  });

  useEffect(() => {
    if (modo === 'aplicar' && vacanteIdRuta) {
      cargarVacanteFija();
    }
  }, [modo, vacanteIdRuta]);

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

  const inputClass = "w-full px-4 py-2.5 bg-[#0D0D0D] border border-[#2a2a2a] text-white rounded focus:ring-1 focus:ring-[#C9A14A] focus:border-[#C9A14A] outline-none transition placeholder:text-[#555]";
  const labelClass = "block text-sm font-medium text-[#B8BFC7] mb-1.5";

  if (modo === 'aplicar' && cargandoVacante) {
    return (
      <div className="min-h-screen bg-[#0D0D0D] flex items-center justify-center" style={FONT_SANS}>
        <p className="text-[#B8BFC7]">Cargando...</p>
      </div>
    );
  }

  if (modo === 'aplicar' && !vacanteFija) {
    return (
      <div className="min-h-screen bg-[#0D0D0D] flex items-center justify-center p-4" style={FONT_SANS}>
        <div className="border border-[#2a2a2a] p-8 max-w-md text-center">
          <p className="text-[#D62828] mb-4">{error || 'Esta vacante no está disponible.'}</p>
          <button onClick={() => navigate('/aplicar')} className="text-[#C9A14A] hover:text-white font-medium">
            Ver otras vacantes
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0D0D0D] flex items-center justify-center p-4" style={FONT_SANS}>
      {/* Container */}
      <div className="w-full max-w-md">
        {/* Card */}
        <div className="border border-[#2a2a2a] overflow-hidden">
          {/* Header */}
          <div className="border-b border-[#2a2a2a] px-6 py-8 text-center">
            <div className="font-extrabold text-3xl tracking-wide text-white">
              CEN<span className="text-[#D62828]">E</span>RH
            </div>
            <div className="text-[#C9A14A] text-xs tracking-[6px] mt-2">CONSULTING</div>
            <p className="text-[#B8BFC7] text-xs mt-4">Evaluación Estratégica de Gestión Humana</p>
          </div>

          {/* Body */}
          <div className="p-8">
            <h1 className="text-2xl font-semibold text-white mb-2" style={FONT_SERIF}>{titulo}</h1>
            <p className="text-[#B8BFC7] text-sm mb-6">{subtitulo}</p>

            {modo === 'aplicar' && vacanteFija && (
              <div className="border border-[#2a2a2a] px-4 py-3 mb-4">
                <p className="text-sm text-white font-semibold">{vacanteFija.nombre}</p>
                <p className="text-xs text-[#0050A0]">{vacanteFija.cliente}</p>
              </div>
            )}

            {error && (
              <div className="border border-[#D62828] text-[#D62828] px-4 py-3 mb-6 text-sm">
                {error}
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
              {/* Nombre */}
              <div>
                <label className={labelClass}>Nombre Completo *</label>
                <input
                  type="text"
                  name="nombre"
                  value={formData.nombre}
                  onChange={handleChange}
                  required
                  className={inputClass}
                  placeholder="Tu nombre completo"
                />
              </div>

              {/* Email */}
              <div>
                <label className={labelClass}>Email *</label>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  required
                  className={inputClass}
                  placeholder="tu@email.com"
                />
              </div>

              {/* Teléfono */}
              <div>
                <label className={labelClass}>Teléfono</label>
                <input
                  type="tel"
                  name="telefono"
                  value={formData.telefono}
                  onChange={handleChange}
                  className={inputClass}
                  placeholder="+1-809-000-0000"
                />
              </div>

              {/* Botón */}
              <button
                type="submit"
                disabled={loading}
                className="w-full bg-[#D62828] hover:bg-[#b91f1f] text-white font-bold tracking-wide py-3 transition disabled:opacity-50 disabled:cursor-not-allowed mt-6"
              >
                {loading ? 'REGISTRANDO...' : modo === 'bolsa' ? 'REGISTRAR MI PERFIL' : 'COMENZAR EVALUACIÓN'}
              </button>

              {/* Nota */}
              <p className="text-xs text-[#666] text-center mt-4">
                * Campos requeridos. Tu información será confidencial.
              </p>
            </form>
          </div>

          {/* Footer */}
          <div className="border-t border-[#2a2a2a] px-6 py-4 text-center text-xs text-[#666]">
            <p>CENERH Consulting — Punta Cana, República Dominicana</p>
          </div>
        </div>
      </div>
    </div>
  );
}
