/**
 * CENERH RECRUIT OS - Cuestionario + CV
 * Paso intermedio entre el registro y los tests psicométricos.
 * Recolecta los datos completos del candidato para la base de datos
 * de reclutamiento (datos personales, domicilio, formación, experiencia).
 */

import { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { perfilAPI } from '../services/api';
import { FONT_SANS, FONT_SERIF } from '../theme';

const ESTADOS_CIVILES = ['Soltero(a)', 'Casado(a)', 'Unión libre', 'Divorciado(a)', 'Viudo(a)'];
const NIVELES_ACADEMICOS = [
  'Secundaria/Bachillerato',
  'Técnico',
  'Universitario (en curso)',
  'Universitario (graduado)',
  'Postgrado',
  'Maestría',
  'Doctorado',
];
const FUENTES_RECLUTAMIENTO = [
  'Referido por un empleado',
  'LinkedIn',
  'Redes sociales (Facebook/Instagram)',
  'Portal de empleos',
  'Página web de la empresa',
  'Otro',
];

function SeccionTitulo({ children }) {
  return <h2 className="text-sm font-bold text-[#C9A14A] uppercase tracking-wide mt-6 mb-3 border-b border-[#2a2a2a] pb-1">{children}</h2>;
}

function Campo({ label, children }) {
  return (
    <div>
      <label className="block text-sm font-medium text-[#B8BFC7] mb-1">{label}</label>
      {children}
    </div>
  );
}

const inputClass = "w-full px-4 py-2 bg-[#0D0D0D] border border-[#2a2a2a] text-white rounded focus:ring-1 focus:ring-[#C9A14A] focus:border-[#C9A14A] outline-none placeholder:text-[#555]";

export default function PerfilPage() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const volverAResultados = searchParams.get('retorno') === 'resultados';
  const esBolsaTalento = searchParams.get('retorno') === 'bolsa';
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [guardadoBolsa, setGuardadoBolsa] = useState(false);
  const [archivo, setArchivo] = useState(null);
  const [formData, setFormData] = useState({
    // Datos personales
    cedula: '',
    edad: '',
    estado_civil: '',
    cantidad_hijos: '',
    edades_hijos: '',
    // Domicilio
    ciudad_provincia: '',
    direccion_exacta: '',
    // Formación académica
    nivel_academico: '',
    carrera: '',
    universidad: '',
    // Experiencia laboral
    anos_experiencia: '',
    ultimo_cargo: '',
    ultimo_salario: '',
    funciones_ultimo_empleo: '',
    pretension_salarial: '',
    // Contexto de la aplicación
    fuente_reclutamiento: '',
    posiciones_interes: '',
    contacto_emergencia_nombre: '',
    contacto_emergencia_telefono: '',
    // Otros
    ubicacion: '',
    disponibilidad: 'Inmediata',
    tiene_vehiculo: false,
    tiene_visa: false,
  });

  const [cvExistente, setCvExistente] = useState('');
  const [analizandoCV, setAnalizandoCV] = useState(false);
  const [camposDetectados, setCamposDetectados] = useState(false);

  const candidatoId = localStorage.getItem('candidatoId');

  useEffect(() => {
    if (!candidatoId) return;
    (async () => {
      try {
        const data = await perfilAPI.obtenerCuestionario(candidatoId);
        if (data.perfil) {
          setFormData(prev => {
            const actualizado = { ...prev };
            for (const [campo, valor] of Object.entries(data.perfil)) {
              if (valor === null || valor === undefined) continue;
              actualizado[campo] = valor;
            }
            return actualizado;
          });
        }
        if (data.cv_filename) {
          setCvExistente(data.cv_filename);
        }
      } catch (err) {
        console.error('No se pudo precargar el perfil existente:', err);
      }
    })();
  }, [candidatoId]);

  if (!candidatoId) {
    navigate('/');
    return null;
  }

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({ ...prev, [name]: type === 'checkbox' ? checked : value }));
  };

  const handleFileChange = async (e) => {
    const nuevoArchivo = e.target.files[0] || null;
    setArchivo(nuevoArchivo);
    if (!nuevoArchivo) return;

    setAnalizandoCV(true);
    setCamposDetectados(false);
    try {
      const resultado = await perfilAPI.subirCV(candidatoId, nuevoArchivo);
      setCvExistente(resultado.cv_filename);
      const sugeridos = resultado.campos_sugeridos || {};
      if (Object.keys(sugeridos).length > 0) {
        // Solo precarga los campos que el candidato todavía no llenó a mano
        // -- nunca pisa lo que ya escribió.
        setFormData(prev => {
          const actualizado = { ...prev };
          for (const [campo, valor] of Object.entries(sugeridos)) {
            if (!actualizado[campo]) actualizado[campo] = valor;
          }
          return actualizado;
        });
        setCamposDetectados(true);
      }
    } catch (err) {
      console.error('Error al subir/leer el CV:', err);
    } finally {
      setAnalizandoCV(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // ciudad_provincia ya cubre "dónde vive"; mantenemos ubicacion = ciudad_provincia
      // por compatibilidad con el campo legado que usa el resto del sistema.
      const payload = {
        ...formData,
        ubicacion: formData.ciudad_provincia || formData.ubicacion,
        edad: formData.edad ? parseInt(formData.edad, 10) : null,
        cantidad_hijos: formData.cantidad_hijos ? parseInt(formData.cantidad_hijos, 10) : null,
        anos_experiencia: formData.anos_experiencia ? parseInt(formData.anos_experiencia, 10) : null,
      };
      await perfilAPI.guardarCuestionario(candidatoId, payload);
      if (esBolsaTalento) {
        setGuardadoBolsa(true);
      } else {
        navigate(volverAResultados ? '/resultados' : '/tests');
      }
    } catch (err) {
      setError('Error al guardar tu información. Intenta nuevamente.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (guardadoBolsa) {
    return (
      <div className="min-h-screen bg-[#0D0D0D] flex items-center justify-center p-4" style={FONT_SANS}>
        <div className="border border-[#2a2a2a] p-8 max-w-md text-center">
          <h1 className="text-2xl font-semibold text-white mb-2" style={FONT_SERIF}>¡Gracias!</h1>
          <p className="text-[#B8BFC7] text-sm">
            Tu perfil quedó registrado en nuestra bolsa de talento. Te contactaremos cuando surja una posición que encaje contigo.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0D0D0D] flex items-center justify-center p-4 py-10" style={FONT_SANS}>
      <div className="w-full max-w-2xl">
        <div className="border border-[#2a2a2a] overflow-hidden">
          <div className="border-b border-[#2a2a2a] px-6 py-6 text-center">
            <h1 className="text-xl font-semibold text-white" style={FONT_SERIF}>
              {volverAResultados ? 'Corrige o actualiza tus datos' : esBolsaTalento ? 'Únete a nuestra bolsa de talento' : 'Cuéntanos un poco más de ti'}
            </h1>
            <p className="text-[#B8BFC7] text-xs mt-1">
              {volverAResultados ? 'Al guardar volverás a tus resultados' : esBolsaTalento ? 'Completa tu perfil para que te tengamos en cuenta' : 'Antes de comenzar los tests'}
            </p>
          </div>

          <div className="p-8">
            {error && (
              <div className="border border-[#D62828] text-[#D62828] px-4 py-3 mb-6 text-sm">
                {error}
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
              <SeccionTitulo>Datos personales</SeccionTitulo>
              <div className="grid grid-cols-2 gap-4">
                <Campo label="Cédula">
                  <input type="text" name="cedula" value={formData.cedula} onChange={handleChange} className={inputClass} placeholder="000-0000000-0" />
                </Campo>
                <Campo label="Edad">
                  <input type="number" min="16" max="90" name="edad" value={formData.edad} onChange={handleChange} className={inputClass} />
                </Campo>
                <Campo label="Estado civil">
                  <select name="estado_civil" value={formData.estado_civil} onChange={handleChange} className={inputClass}>
                    <option value="">Selecciona...</option>
                    {ESTADOS_CIVILES.map(op => <option key={op} value={op}>{op}</option>)}
                  </select>
                </Campo>
                <Campo label="Cantidad de hijos">
                  <input type="number" min="0" name="cantidad_hijos" value={formData.cantidad_hijos} onChange={handleChange} className={inputClass} />
                </Campo>
              </div>
              {Number(formData.cantidad_hijos) > 0 && (
                <Campo label="Edades de los hijos">
                  <input type="text" name="edades_hijos" value={formData.edades_hijos} onChange={handleChange} className={inputClass} placeholder="Ej: 5, 8, 12" />
                </Campo>
              )}

              <SeccionTitulo>Domicilio</SeccionTitulo>
              <div className="grid grid-cols-2 gap-4">
                <Campo label="Ciudad o provincia">
                  <input type="text" name="ciudad_provincia" value={formData.ciudad_provincia} onChange={handleChange} className={inputClass} placeholder="Ej: Santo Domingo" />
                </Campo>
                <Campo label="Teléfono/WhatsApp de contacto en caso de emergencia">
                  <input type="tel" name="contacto_emergencia_telefono" value={formData.contacto_emergencia_telefono} onChange={handleChange} className={inputClass} />
                </Campo>
              </div>
              <Campo label="Dirección exacta">
                <textarea name="direccion_exacta" value={formData.direccion_exacta} onChange={handleChange} rows={2} className={inputClass} placeholder="Calle, número, sector, referencia" />
              </Campo>
              <Campo label="Nombre del contacto de emergencia">
                <input type="text" name="contacto_emergencia_nombre" value={formData.contacto_emergencia_nombre} onChange={handleChange} className={inputClass} />
              </Campo>

              <SeccionTitulo>Formación académica</SeccionTitulo>
              <Campo label="Nivel académico">
                <select name="nivel_academico" value={formData.nivel_academico} onChange={handleChange} className={inputClass}>
                  <option value="">Selecciona...</option>
                  {NIVELES_ACADEMICOS.map(op => <option key={op} value={op}>{op}</option>)}
                </select>
              </Campo>
              <div className="grid grid-cols-2 gap-4">
                <Campo label="Carrera">
                  <input type="text" name="carrera" value={formData.carrera} onChange={handleChange} className={inputClass} placeholder="Ej: Ingeniería Industrial" />
                </Campo>
                <Campo label="Universidad">
                  <input type="text" name="universidad" value={formData.universidad} onChange={handleChange} className={inputClass} />
                </Campo>
              </div>

              <SeccionTitulo>Experiencia laboral</SeccionTitulo>
              <div className="grid grid-cols-2 gap-4">
                <Campo label="Años de experiencia en el área">
                  <input type="number" min="0" name="anos_experiencia" value={formData.anos_experiencia} onChange={handleChange} className={inputClass} />
                </Campo>
                <Campo label="Último cargo desempeñado">
                  <input type="text" name="ultimo_cargo" value={formData.ultimo_cargo} onChange={handleChange} className={inputClass} />
                </Campo>
                <Campo label="Último salario">
                  <input type="text" name="ultimo_salario" value={formData.ultimo_salario} onChange={handleChange} className={inputClass} placeholder="Ej: RD$ 45,000" />
                </Campo>
                <Campo label="Expectativa salarial">
                  <input type="text" name="pretension_salarial" value={formData.pretension_salarial} onChange={handleChange} className={inputClass} placeholder="Ej: RD$ 50,000 - 60,000" />
                </Campo>
              </div>
              <Campo label="Funciones desempeñadas en el último empleo">
                <textarea name="funciones_ultimo_empleo" value={formData.funciones_ultimo_empleo} onChange={handleChange} rows={3} className={inputClass} />
              </Campo>

              <SeccionTitulo>Sobre tu aplicación</SeccionTitulo>
              <Campo label="¿Cómo te enteraste de esta vacante?">
                <select name="fuente_reclutamiento" value={formData.fuente_reclutamiento} onChange={handleChange} className={inputClass}>
                  <option value="">Selecciona...</option>
                  {FUENTES_RECLUTAMIENTO.map(op => <option key={op} value={op}>{op}</option>)}
                </select>
              </Campo>
              <Campo label="¿Qué otras posiciones te interesaría aplicar?">
                <input type="text" name="posiciones_interes" value={formData.posiciones_interes} onChange={handleChange} className={inputClass} placeholder="Opcional" />
              </Campo>

              <div className="grid grid-cols-2 gap-4">
                <Campo label="Disponibilidad">
                  <select name="disponibilidad" value={formData.disponibilidad} onChange={handleChange} className={inputClass}>
                    <option value="Inmediata">Inmediata</option>
                    <option value="2 semanas">2 semanas</option>
                    <option value="1 mes">1 mes</option>
                    <option value="Más de 1 mes">Más de 1 mes</option>
                  </select>
                </Campo>
                <div className="flex items-end gap-6 pb-2">
                  <label className="flex items-center gap-2 text-sm text-[#B8BFC7]">
                    <input type="checkbox" name="tiene_vehiculo" checked={formData.tiene_vehiculo} onChange={handleChange} className="w-4 h-4 accent-[#D62828]" />
                    Tengo vehículo
                  </label>
                  <label className="flex items-center gap-2 text-sm text-[#B8BFC7]">
                    <input type="checkbox" name="tiene_visa" checked={formData.tiene_visa} onChange={handleChange} className="w-4 h-4 accent-[#D62828]" />
                    Tengo visa
                  </label>
                </div>
              </div>

              <Campo label="Currículum (PDF, DOC o DOCX)">
                {cvExistente && !analizandoCV && (
                  <p className="text-xs text-[#666] mb-1">Ya tienes cargado: {cvExistente}. Sube uno nuevo solo si quieres reemplazarlo.</p>
                )}
                <input
                  type="file" accept=".pdf,.doc,.docx" onChange={handleFileChange}
                  className="w-full text-sm text-[#B8BFC7] file:mr-3 file:py-2 file:px-4 file:border-0 file:bg-[#2a2a2a] file:text-white hover:file:bg-[#3a3a3a]"
                />
                {analizandoCV && (
                  <p className="text-xs text-[#C9A14A] mt-1">Leyendo tu CV para precargar el formulario...</p>
                )}
                {camposDetectados && !analizandoCV && (
                  <p className="text-xs text-[#0050A0] mt-1">
                    Completamos algunos campos según tu CV -- revísalos y corrígelos si hace falta.
                  </p>
                )}
              </Campo>

              <button
                type="submit"
                disabled={loading}
                className="w-full bg-[#D62828] hover:bg-[#b91f1f] text-white font-bold tracking-wide py-3 transition disabled:opacity-50 mt-6"
              >
                {loading ? 'GUARDANDO...' : volverAResultados ? 'GUARDAR CAMBIOS' : esBolsaTalento ? 'REGISTRAR MI PERFIL' : 'CONTINUAR A LOS TESTS'}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
