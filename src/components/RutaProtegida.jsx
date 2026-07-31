/**
 * RutaProtegida - Redirige a /login si no hay sesión, o si el rol no coincide
 */

import { Navigate } from 'react-router-dom';
import { authAPI } from '../services/api';

export default function RutaProtegida({ children, rolesPermitidos }) {
  const usuario = authAPI.usuarioActual();

  if (!authAPI.estaAutenticado() || !usuario) {
    return <Navigate to="/login" replace />;
  }

  if (rolesPermitidos && !rolesPermitidos.includes(usuario.rol)) {
    return <Navigate to="/login" replace />;
  }

  return children;
}
