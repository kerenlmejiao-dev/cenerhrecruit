/**
 * CENERH RECRUIT OS - API Service
 * Comunicación con backend
 */

import axios from 'axios';

// En desarrollo (npm run dev), el frontend corre en :5173 y la API en :8000.
// En producción (npm run build), el frontend se sirve desde el mismo backend
// (ver api.py), así que las rutas relativas ("") apuntan al origen correcto.
const API_URL = import.meta.env.VITE_API_URL ?? (import.meta.env.DEV ? 'http://localhost:8000' : '');

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  }
});

// Interceptor: agrega el JWT de reclutador/empresa si hay sesión activa
apiClient.interceptors.request.use(config => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor para errores
apiClient.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error);
    if (error.response?.status === 401) {
      localStorage.removeItem('authToken');
      localStorage.removeItem('authUsuario');
    }
    // 402 = sin membresía activa (ver require_membresia_activa en
    // auth_users.py) -- único uso de este código en todo el sistema, así
    // que redirigir siempre a la pantalla de membresía es seguro.
    if (error.response?.status === 402 && !window.location.pathname.startsWith('/reclutador/membresia-requerida')) {
      window.location.href = '/reclutador/membresia-requerida';
    }
    throw error;
  }
);

/**
 * AUTENTICACIÓN (reclutador / empresa / owner)
 */
export const authAPI = {
  login: async (email, password) => {
    const response = await apiClient.post('/api/auth/login', { email, password });
    localStorage.setItem('authToken', response.data.access_token);
    localStorage.setItem('authUsuario', JSON.stringify(response.data.usuario));
    return response.data;
  },

  registroReclutador: async (datos) => {
    const response = await apiClient.post('/api/auth/registro', datos);
    localStorage.setItem('authToken', response.data.access_token);
    localStorage.setItem('authUsuario', JSON.stringify(response.data.usuario));
    return response.data;
  },

  logout: () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('authUsuario');
  },

  usuarioActual: () => {
    const raw = localStorage.getItem('authUsuario');
    return raw ? JSON.parse(raw) : null;
  },

  estaAutenticado: () => !!localStorage.getItem('authToken'),

  obtenerPerfil: async () => {
    const response = await apiClient.get('/api/auth/me');
    localStorage.setItem('authUsuario', JSON.stringify(response.data));
    return response.data;
  },
};

/**
 * PORTAL RECLUTADOR
 */
export const reclutadorAPI = {
  bancoTests: async () => {
    const response = await apiClient.get('/api/reclutador/banco/tests');
    return response.data;
  },

  bancoAssessments: async () => {
    const response = await apiClient.get('/api/reclutador/banco/assessments');
    return response.data;
  },

  crearEmpresa: async (datos) => {
    const response = await apiClient.post('/api/reclutador/empresas', datos);
    return response.data;
  },

  listarEmpresas: async () => {
    const response = await apiClient.get('/api/reclutador/empresas');
    return response.data;
  },

  crearVacante: async (datos) => {
    const response = await apiClient.post('/api/reclutador/vacantes', datos);
    return response.data;
  },

  listarVacantes: async () => {
    const response = await apiClient.get('/api/reclutador/vacantes');
    return response.data;
  },

  detalleVacante: async (vacanteId) => {
    const response = await apiClient.get(`/api/reclutador/vacantes/${vacanteId}`);
    return response.data;
  },

  sugerenciasBolsa: async (vacanteId) => {
    const response = await apiClient.get(`/api/reclutador/vacantes/${vacanteId}/sugerencias-bolsa`);
    return response.data;
  },

  cambiarEstadoVacante: async (vacanteId, nuevoEstado) => {
    const response = await apiClient.post(`/api/reclutador/vacantes/${vacanteId}/estado?nuevo_estado=${nuevoEstado}`);
    return response.data;
  },

  bolsaTalento: async () => {
    const response = await apiClient.get('/api/reclutador/candidatos/bolsa-talento');
    return response.data;
  },

  cambiarStatusCandidato: async (candidatoId, status) => {
    const response = await apiClient.post(`/api/reclutador/candidatos/${candidatoId}/status`, { status });
    return response.data;
  },

  candidatosVacante: async (vacanteId) => {
    const response = await apiClient.get(`/api/reclutador/vacantes/${vacanteId}/candidatos`);
    return response.data;
  },

  assessmentsCandidato: async (candidatoId) => {
    const response = await apiClient.get(`/api/reclutador/candidatos/${candidatoId}/assessments`);
    return response.data;
  },

  marcarAssessmentRevisado: async (candidatoId, assessmentId) => {
    const response = await apiClient.post(`/api/reclutador/candidatos/${candidatoId}/assessments/${assessmentId}/marcar-revisado`);
    return response.data;
  },

  descargarCV: async (candidatoId) => {
    const response = await apiClient.get(`/api/reclutador/candidatos/${candidatoId}/cv`, {
      responseType: 'blob',
    });
    const disposition = response.headers['content-disposition'] || '';
    const match = disposition.match(/filename="?([^"]+)"?/);
    return { blob: response.data, filename: match ? match[1] : `CV_${candidatoId}` };
  },

  metricas: async () => {
    const response = await apiClient.get('/api/reclutador/metricas');
    return response.data;
  },

  referenciasCandidato: async (candidatoId) => {
    const response = await apiClient.get(`/api/reclutador/candidatos/${candidatoId}/referencias`);
    return response.data;
  },

  enviarSolicitudReferencia: async (candidatoId, referenciaId) => {
    const response = await apiClient.post(`/api/reclutador/candidatos/${candidatoId}/referencias/${referenciaId}/enviar`);
    return response.data;
  },
};

/**
 * PORTAL EMPRESA
 */
export const empresaAPI = {
  listarVacantes: async () => {
    const response = await apiClient.get('/api/empresa/vacantes');
    return response.data;
  },

  candidatosVacante: async (vacanteId) => {
    const response = await apiClient.get(`/api/empresa/vacantes/${vacanteId}/candidatos`);
    return response.data;
  },

  desbloquearCandidato: async (candidatoId, documento) => {
    const response = await apiClient.post(`/api/empresa/candidatos/${candidatoId}/desbloquear`, { documento });
    return response.data;
  },
};

/**
 * PAGOS (suscripción reclutador + desbloqueo de candidatos)
 */
// Planes de membresía, públicos (sin login) -- para la página de comparación
export const planesAPI = {
  listar: async () => {
    const response = await apiClient.get('/api/planes');
    return response.data;
  },
};

export const pagosAPI = {
  obtenerSuscripcion: async () => {
    const response = await apiClient.get('/api/reclutador/suscripcion');
    return response.data;
  },

  crearCheckoutSuscripcion: async (plan, documento) => {
    const response = await apiClient.post(`/api/reclutador/suscripcion/checkout?plan=${plan}`, { documento });
    return response.data;
  },

  cambiarRenovacionAutomatica: async (activar) => {
    const response = await apiClient.post('/api/reclutador/suscripcion/renovacion-automatica', { activar });
    return response.data;
  },

  estadoTransaccion: async (orderId) => {
    const response = await apiClient.get(`/api/pagos/estado/${orderId}`);
    return response.data;
  },
};

/**
 * PAGOS DEL CANDIDATO (estatus del proceso / resultados / análisis de CV)
 */
export const pagosCandidatoAPI = {
  compras: async (candidatoId) => {
    const response = await apiClient.get(`/api/candidatos/${candidatoId}/compras`);
    return response.data;
  },

  checkout: async (candidatoId, tipo, documento) => {
    const response = await apiClient.post(`/api/candidatos/${candidatoId}/pagos/checkout`, { tipo, documento });
    return response.data;
  },

  reporteResultados: async (candidatoId) => {
    const response = await apiClient.get(`/api/candidatos/${candidatoId}/reporte-resultados`);
    return response.data;
  },

  analisisCV: async (candidatoId) => {
    const response = await apiClient.get(`/api/candidatos/${candidatoId}/analisis-cv`);
    return response.data;
  },
};

/**
 * CANDIDATOS
 */
export const candidatosAPI = {
  // Crear nuevo candidato. Crea (o valida) su cuenta de candidato con la
  // contraseña dada, y la deja con sesión iniciada (mismas llaves de
  // localStorage que usa el login de reclutador/empresa).
  crear: async (datos) => {
    const response = await apiClient.post('/api/candidatos', datos);
    if (response.data.access_token) {
      localStorage.setItem('authToken', response.data.access_token);
      localStorage.setItem('authUsuario', JSON.stringify(response.data.usuario));
    }
    return response.data;
  },

  // Obtener resultados
  obtenerResultados: async (candidatoId) => {
    const response = await apiClient.get(`/api/candidatos/${candidatoId}/resultados`);
    return response.data;
  },

  // Todas las aplicaciones del candidato autenticado (requiere sesión de candidato)
  misAplicaciones: async () => {
    const response = await apiClient.get('/api/candidatos/mis-aplicaciones');
    return response.data;
  },

  // Generar y descargar el PDF real de la ficha (solo reclutador/owner -- ver reclutador_router.py)
  generarPDF: async (candidatoId) => {
    const response = await apiClient.get(`/api/candidatos/${candidatoId}/ficha.pdf`, {
      responseType: 'blob',
    });
    return response.data;
  },
};

/**
 * TESTS
 */
export const testsAPI = {
  // Obtener tests disponibles
  obtenerDisponibles: async () => {
    const response = await apiClient.get('/api/tests/disponibles');
    return response.data;
  },

  // Obtener información de un test
  obtenerInfo: async (testId) => {
    const response = await apiClient.get(`/api/tests/${testId}/info`);
    return response.data;
  },

  // Obtener preguntas de un test
  obtenerPreguntas: async (testId, candidatoId) => {
    const response = await apiClient.get(`/api/tests/${testId}/${candidatoId}`);
    return response.data;
  },

  // Guardar respuestas
  guardarRespuestas: async (testId, candidatoId, respuestas) => {
    const response = await apiClient.post(
      `/api/tests/${testId}/${candidatoId}/respuestas`,
      { respuestas }
    );
    return response.data;
  },
};

/**
 * PERFIL DE CANDIDATO (cuestionario + CV)
 */
export const perfilAPI = {
  obtenerCuestionario: async (candidatoId) => {
    const response = await apiClient.get(`/api/candidatos/${candidatoId}/cuestionario`);
    return response.data;
  },

  guardarCuestionario: async (candidatoId, datos) => {
    const response = await apiClient.post(`/api/candidatos/${candidatoId}/cuestionario`, datos);
    return response.data;
  },

  subirCV: async (candidatoId, archivo) => {
    const formData = new FormData();
    formData.append('archivo', archivo);
    const response = await apiClient.post(`/api/candidatos/${candidatoId}/cv`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },

  obtenerReferencias: async (candidatoId) => {
    const response = await apiClient.get(`/api/candidatos/${candidatoId}/referencias`);
    return response.data;
  },

  guardarReferencias: async (candidatoId, referencias) => {
    const response = await apiClient.post(`/api/candidatos/${candidatoId}/referencias`, referencias);
    return response.data;
  },
};

/**
 * REFERENCIAS - formulario público (token-based, sin login)
 */
export const referenciasAPI = {
  obtener: async (token) => {
    const response = await apiClient.get(`/api/referencias/${token}`);
    return response.data;
  },

  responder: async (token, datos) => {
    const response = await apiClient.post(`/api/referencias/${token}/responder`, datos);
    return response.data;
  },
};

/**
 * ASSESSMENT CENTERS (evaluados por IA)
 */
export const assessmentAPI = {
  listar: async (candidatoId) => {
    const response = await apiClient.get(`/api/candidatos/${candidatoId}/assessments`);
    return response.data;
  },

  guardarRespuesta: async (candidatoId, preguntaId, respuestaTexto) => {
    const response = await apiClient.post(
      `/api/candidatos/${candidatoId}/assessments/preguntas/${preguntaId}/respuesta`,
      { respuesta_texto: respuestaTexto }
    );
    return response.data;
  },
};

/**
 * VACANTES
 */
export const vacantesAPI = {
  // Listar vacantes activas (formulario público de postulación)
  listar: async () => {
    const response = await apiClient.get('/api/vacantes');
    return response.data;
  },

  // Obtener configuración de vacante
  obtenerConfig: async (vacanteId) => {
    const response = await apiClient.get(`/api/vacantes/${vacanteId}/config`);
    return response.data;
  },
};

/**
 * HEALTH CHECK
 */
export const healthAPI = {
  check: async () => {
    try {
      const response = await apiClient.get('/health');
      return response.status === 200;
    } catch {
      return false;
    }
  },
};

export default apiClient;
