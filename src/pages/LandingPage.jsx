/**
 * CENERH RECRUIT OS - Página de inicio
 *
 * Punto de entrada único para los dos públicos de la plataforma: candidatos
 * que aplican a una vacante, y reclutadores/empresas que gestionan procesos.
 *
 * Línea gráfica tomada directamente del mockup real de cenerhconsulting.com
 * (fondo casi negro, Montserrat + Cormorant Garamond serif, rojo/dorado/azul
 * como acentos, tarjetas de borde fino sin esquinas redondeadas) -- no el
 * degradado azul+amarillo que usa el resto del flujo del candidato.
 */

import { Link } from 'react-router-dom';
import { FONT_SANS, FONT_SERIF } from '../theme';

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-[#0D0D0D] text-white" style={FONT_SANS}>
      {/* Header */}
      <header className="border-b border-[#2a2a2a] py-7">
        <div className="max-w-[1100px] mx-auto px-6 flex items-baseline gap-3">
          <div className="font-extrabold text-2xl tracking-wide">
            CEN<span className="text-[#D62828]">E</span>RH
          </div>
          <div className="text-[#C9A14A] font-medium text-xs tracking-[6px]">CONSULTING</div>
        </div>
      </header>

      {/* Hero */}
      <section className="text-center px-6 pt-24 pb-16">
        <h1
          className="max-w-3xl mx-auto text-[32px] md:text-[44px] font-semibold leading-tight mb-6"
          style={FONT_SERIF}
        >
          Aquí empieza tu proceso de reclutamiento, sin importar de qué lado estés.{' '}
          <span className="text-[#C9A14A]">Un mismo camino, para los dos.</span>
        </h1>
        <p className="text-[#B8BFC7] text-lg max-w-xl mx-auto mb-9">
          Buscas tu próxima oportunidad, o al candidato correcto para tu equipo -- aquí encuentras
          el mismo proceso: claro, objetivo y con datos reales.
        </p>
        <div className="w-20 h-0.5 bg-[#C9A14A] mx-auto"></div>
      </section>

      {/* Dos caminos */}
      <section className="border-t border-[#1f1f1f] py-16 px-6">
        <div className="max-w-[1100px] mx-auto">
          <div
            className="text-center text-3xl md:text-4xl font-semibold mb-12"
            style={FONT_SERIF}
          >
            ¿Cómo quiere <span className="text-[#C9A14A]">entrar?</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-3xl mx-auto">
            {/* Candidato */}
            <Link
              to="/aplicar"
              className="border border-[#2a2a2a] p-8 text-center hover:border-[#D62828] transition-colors duration-300"
            >
              <h3 className="text-[#0050A0] text-xl font-bold mb-3">Soy candidato</h3>
              <p className="text-[#B8BFC7] text-sm mb-8">
                Aplica a una vacante abierta o únete a nuestra bolsa de talento para futuras
                oportunidades.
              </p>
              <span className="inline-block bg-[#D62828] hover:bg-[#b91f1f] text-white font-bold text-sm tracking-wide py-4 px-8 transition-colors">
                VER VACANTES DISPONIBLES
              </span>
            </Link>

            {/* Reclutador / Empresa */}
            <Link
              to="/login"
              className="border border-[#2a2a2a] p-8 text-center hover:border-[#D62828] transition-colors duration-300"
            >
              <h3 className="text-[#0050A0] text-xl font-bold mb-3">Soy reclutador o empresa</h3>
              <p className="text-[#B8BFC7] text-sm mb-8">
                Gestiona vacantes, revisa candidatos y da seguimiento a tus procesos de
                selección.
              </p>
              <span className="inline-block bg-[#D62828] hover:bg-[#b91f1f] text-white font-bold text-sm tracking-wide py-4 px-8 transition-colors">
                INICIAR SESIÓN
              </span>
            </Link>
          </div>

          <p className="text-[#666] text-xs mt-8 text-center">
            ¿Eres reclutador y no tienes cuenta todavía?{' '}
            <Link to="/registro-reclutador" className="text-[#C9A14A] hover:text-white underline">
              Créala aquí
            </Link>
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-[#1f1f1f] py-8 px-6 text-center text-[#666] text-xs">
        <Link to="/como-usamos-la-ia" className="hover:text-[#C9A14A] underline">
          Cómo usamos la IA en este sistema
        </Link>
        <p className="mt-3">CENERH Consulting — Punta Cana, República Dominicana</p>
      </footer>
    </div>
  );
}
