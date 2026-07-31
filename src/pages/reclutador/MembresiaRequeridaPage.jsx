/**
 * Portal Reclutador - Membresía requerida
 *
 * Se muestra cuando cualquier endpoint del panel de reclutador devuelve 402
 * (sin membresía activa, o vencida) -- ver require_membresia_activa en
 * auth_users.py. Ningún plan es gratuito, así que esto es lo primero que ve
 * un reclutador recién registrado, o uno cuya membresía de 27 días venció.
 */

import { Link } from 'react-router-dom';
import { authAPI } from '../../services/api';
import { FONT_SANS, FONT_SERIF } from '../../theme';

export default function MembresiaRequeridaPage() {
  const usuario = authAPI.usuarioActual();

  const handleLogout = () => {
    authAPI.logout();
    window.location.href = '/';
  };

  return (
    <div className="min-h-screen bg-[#0D0D0D] flex items-center justify-center p-4" style={FONT_SANS}>
      <div className="w-full max-w-lg text-center">
        <div className="border border-[#2a2a2a] p-10">
          <h1 className="text-2xl font-semibold text-white mb-2" style={FONT_SERIF}>
            Necesitas una membresía activa
          </h1>
          <p className="text-[#B8BFC7] text-sm mb-1">
            Hola, {usuario?.nombre}
          </p>
          <p className="text-[#B8BFC7] text-sm mb-8">
            Tu cuenta todavía no tiene una membresía activa, o la que tenías venció. Ningún plan de
            CENERH Recruit OS es gratuito -- confirma tu pago con CENERH Consulting para activar (o
            renovar) tu acceso al panel de reclutador.
          </p>

          <Link
            to="/planes"
            className="inline-block bg-[#D62828] hover:bg-[#b91f1f] text-white font-bold tracking-wide py-3 px-8 transition mb-4"
          >
            VER PLANES Y PRECIOS
          </Link>

          <p>
            <button onClick={handleLogout} className="text-[#666] hover:text-white text-sm">
              Salir
            </button>
          </p>
        </div>
      </div>
    </div>
  );
}
