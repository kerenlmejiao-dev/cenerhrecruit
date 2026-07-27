/**
 * CENERH RECRUIT OS - API Service
 * Comunicación con backend
 */

import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  }
});

// Interceptor para errores
apiClient.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error);
    throw error;
  }
);

/**
 * CANDIDATOS
 */
export const candidatosAPI = {
  // Crear nuevo candidato
  crear: async (datos) => {
    const response = await apiClient.post('/api/candidatos', datos);
    return response.data;
  },

  // Obtener resultados
  obtenerResultados: async (candidatoId) => {
    const response = await apiClient.get(`/api/candidatos/${candidatoId}/resultados`);
    return response.data;
  },

  // Generar PDF
  generarPDF: async (candidatoId) => {
    const response = await apiClient.get(`/api/candidatos/${candidatoId}/ficha.pdf`);
    return response.data;
  },

  // Enviar email
  enviarEmail: async (candidatoId) => {
    const response = await apiClient.post(`/api/candidatos/${candidatoId}/email`);
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
 * VACANTES
 */
export const vacantesAPI = {
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
