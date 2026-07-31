/**
 * CENERH RECRUIT OS - Página de inicio
 *
 * Punto de entrada único para los dos públicos de la plataforma: candidatos
 * que aplican a una vacante, y reclutadores/empresas que gestionan procesos.
 * Antes "/" llevaba directo al formulario de candidato sin ningún camino
 * visible hacia el portal de reclutador -- esta página resuelve eso.
 */

import { Link } from 'react-router-dom';

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-950 via-blue-900 to-blue-950 flex flex-col relative overflow-hidden">
      {/* Resplandor decorativo */}
      <div className="pointer-events-none absolute -top-40 left-1/2 -translate-x-1/2 w-[36rem] h-[36rem] bg-yellow-400/10 rounded-full blur-3xl"></div>
      <div className="pointer-events-none absolute bottom-0 right-0 w-[28rem] h-[28rem] bg-blue-500/20 rounded-full blur-3xl"></div>

      <div className="relative flex-grow flex flex-col items-center justify-center px-4 py-16">
        {/* Marca */}
        <div className="text-center mb-14">
          <div className="inline-flex items-center gap-3 mb-3">
            <div className="text-5xl md:text-6xl font-bold text-white tracking-tight">CENERH</div>
          </div>
          <div className="text-sm md:text-base text-yellow-300 font-semibold tracking-[0.3em] mb-4">CONSULTING</div>
          <p className="text-blue-100 text-lg max-w-xl mx-auto">
            Evaluación Estratégica de Gestión Humana
          </p>
        </div>

        {/* Dos caminos */}
        <div className="w-full max-w-3xl grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Candidato */}
          <Link
            to="/aplicar"
            className="group bg-white/95 backdrop-blur rounded-2xl shadow-2xl p-8 text-center hover:-translate-y-1 hover:shadow-yellow-400/20 transition-all duration-300"
          >
            <div className="w-16 h-16 mx-auto mb-5 rounded-full bg-blue-100 flex items-center justify-center text-3xl group-hover:bg-blue-600 group-hover:text-white transition-colors">
              🎯
            </div>
            <h2 className="text-xl font-bold text-gray-900 mb-2">Soy candidato</h2>
            <p className="text-gray-600 text-sm mb-6">
              Aplica a una vacante abierta o únete a nuestra bolsa de talento para futuras oportunidades.
            </p>
            <span className="inline-block bg-gradient-to-r from-blue-600 to-blue-800 text-white font-semibold py-2.5 px-6 rounded-lg group-hover:from-blue-700 group-hover:to-blue-900 transition">
              Ver vacantes disponibles
            </span>
          </Link>

          {/* Reclutador / Empresa */}
          <Link
            to="/login"
            className="group bg-white/95 backdrop-blur rounded-2xl shadow-2xl p-8 text-center hover:-translate-y-1 hover:shadow-yellow-400/20 transition-all duration-300"
          >
            <div className="w-16 h-16 mx-auto mb-5 rounded-full bg-yellow-100 flex items-center justify-center text-3xl group-hover:bg-yellow-400 transition-colors">
              💼
            </div>
            <h2 className="text-xl font-bold text-gray-900 mb-2">Soy reclutador o empresa</h2>
            <p className="text-gray-600 text-sm mb-6">
              Gestiona vacantes, revisa candidatos y da seguimiento a tus procesos de selección.
            </p>
            <span className="inline-block bg-gradient-to-r from-yellow-400 to-yellow-500 text-gray-900 font-bold py-2.5 px-6 rounded-lg group-hover:from-yellow-500 group-hover:to-yellow-600 transition">
              Iniciar sesión
            </span>
          </Link>
        </div>

        <p className="text-blue-200 text-xs mt-8 text-center max-w-md">
          ¿Eres reclutador y no tienes cuenta todavía?{' '}
          <Link to="/registro-reclutador" className="underline hover:text-white">Créala aquí</Link>
        </p>
      </div>

      {/* Footer */}
      <div className="relative border-t border-blue-800/60 py-6 px-4 text-center">
        <Link to="/como-usamos-la-ia" className="text-blue-200 text-xs hover:text-white underline">
          Cómo usamos la IA en este sistema
        </Link>
        <p className="text-blue-300/70 text-xs mt-2">© 2026 CENERH Consulting. Todos los derechos reservados.</p>
      </div>
    </div>
  );
}
