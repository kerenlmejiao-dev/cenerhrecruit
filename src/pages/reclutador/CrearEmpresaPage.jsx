/**
 * Portal Reclutador - Crear ficha de empresa cliente + su cuenta de acceso.
 * La empresa no se autorregistra: el reclutador levanta estos datos porque
 * incluyen información de facturación (RNC/comprobante fiscal).
 */

import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { reclutadorAPI } from '../../services/api';

export default function CrearEmpresaPage() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    nombre: '',
    contacto_email: '',
    password: '',
    razon_social: '',
    tiene_rnc: false,
    rnc: '',
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({ ...prev, [name]: type === 'checkbox' ? checked : value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      await reclutadorAPI.crearEmpresa(formData);
      navigate('/reclutador/vacantes/nueva');
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al crear la empresa. Intenta nuevamente.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white shadow">
        <div className="max-w-xl mx-auto px-4 py-6">
          <Link to="/reclutador" className="text-sm text-blue-600 hover:text-blue-800">&larr; Volver al dashboard</Link>
          <h1 className="text-3xl font-bold text-gray-900 mt-2">Nueva empresa cliente</h1>
          <p className="text-gray-600 text-sm mt-1">Tú levantas esta ficha — incluye los datos de facturación de la empresa</p>
        </div>
      </div>

      <div className="max-w-xl mx-auto px-4 py-8">
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">{error}</div>
        )}

        <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow p-6 space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Nombre de la empresa *</label>
            <input
              type="text" name="nombre" value={formData.nombre} onChange={handleChange} required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
              placeholder="Ej: Constructora XYZ"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Razón social (para factura)</label>
            <input
              type="text" name="razon_social" value={formData.razon_social} onChange={handleChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
              placeholder="Nombre legal, si es distinto al comercial"
            />
          </div>

          <div>
            <label className="flex items-center gap-2 text-sm text-gray-700">
              <input type="checkbox" name="tiene_rnc" checked={formData.tiene_rnc} onChange={handleChange} className="w-4 h-4" />
              Tiene RNC / comprobante fiscal
            </label>
          </div>

          {formData.tiene_rnc && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">RNC</label>
              <input
                type="text" name="rnc" value={formData.rnc} onChange={handleChange} required={formData.tiene_rnc}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                placeholder="1-01-00000-0"
              />
            </div>
          )}

          <div className="pt-4 border-t">
            <p className="text-sm font-semibold text-gray-700 mb-3">Cuenta de acceso al Portal Empresa</p>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Email de contacto *</label>
                <input
                  type="email" name="contacto_email" value={formData.contacto_email} onChange={handleChange} required
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                  placeholder="contacto@empresa.com"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Contraseña inicial *</label>
                <input
                  type="text" name="password" value={formData.password} onChange={handleChange} required minLength={8}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                  placeholder="Mínimo 8 caracteres — compártela con el cliente"
                />
              </div>
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-gradient-to-r from-blue-600 to-blue-800 text-white font-semibold py-2.5 rounded-lg hover:from-blue-700 hover:to-blue-900 transition disabled:opacity-50 mt-2"
          >
            {loading ? 'Creando...' : 'Crear empresa'}
          </button>
        </form>
      </div>
    </div>
  );
}
