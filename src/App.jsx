/**
 * CENERH RECRUIT OS - App Principal
 * Gestión de rutas y componentes
 */

import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { useEffect } from 'react';
import LandingPage from './pages/LandingPage';
import VacantesListPage from './pages/VacantesListPage';
import RegistroPage from './pages/RegistroPage';
import PerfilPage from './pages/PerfilPage';
import TestsPage from './pages/TestsPage';
import AssessmentsPage from './pages/AssessmentsPage';
import ResultadosPage from './pages/ResultadosPage';
import ComoUsamosLaIAPage from './pages/ComoUsamosLaIAPage';
import LoginPage from './pages/LoginPage';
import RegistroReclutadorPage from './pages/RegistroReclutadorPage';
import RutaProtegida from './components/RutaProtegida';
import DashboardReclutador from './pages/reclutador/DashboardReclutador';
import CrearVacante from './pages/reclutador/CrearVacante';
import CrearEmpresaPage from './pages/reclutador/CrearEmpresaPage';
import VacanteDetalle from './pages/reclutador/VacanteDetalle';
import SuscripcionPage from './pages/reclutador/SuscripcionPage';
import CandidatoAssessments from './pages/reclutador/CandidatoAssessments';
import BolsaTalentoPage from './pages/reclutador/BolsaTalentoPage';
import DashboardEmpresa from './pages/empresa/DashboardEmpresa';
import VacanteDetalleEmpresa from './pages/empresa/VacanteDetalleEmpresa';
import PagoResultadoPage from './pages/PagoResultadoPage';

function ScrollToTop() {
  const { pathname } = useLocation();

  useEffect(() => {
    window.scrollTo(0, 0);
  }, [pathname]);

  return null;
}

export default function App() {
  return (
    <BrowserRouter>
      <ScrollToTop />
      <Routes>
        {/* Inicio */}
        <Route path="/" element={<LandingPage />} />

        {/* Candidatos */}
        <Route path="/aplicar" element={<VacantesListPage />} />
        <Route path="/aplicar/:vacanteId" element={<RegistroPage modo="aplicar" />} />
        <Route path="/bolsa-de-talento" element={<RegistroPage modo="bolsa" />} />
        <Route path="/perfil" element={<PerfilPage />} />
        <Route path="/tests" element={<TestsPage />} />
        <Route path="/assessments" element={<AssessmentsPage />} />
        <Route path="/resultados" element={<ResultadosPage />} />
        <Route path="/como-usamos-la-ia" element={<ComoUsamosLaIAPage />} />

        {/* Login reclutador/empresa */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/registro-reclutador" element={<RegistroReclutadorPage />} />

        {/* Portal Reclutador */}
        <Route path="/reclutador" element={
          <RutaProtegida rolesPermitidos={['owner', 'reclutador']}>
            <DashboardReclutador />
          </RutaProtegida>
        } />
        <Route path="/reclutador/vacantes/nueva" element={
          <RutaProtegida rolesPermitidos={['owner', 'reclutador']}>
            <CrearVacante />
          </RutaProtegida>
        } />
        <Route path="/reclutador/vacantes/:vacanteId" element={
          <RutaProtegida rolesPermitidos={['owner', 'reclutador']}>
            <VacanteDetalle />
          </RutaProtegida>
        } />
        <Route path="/reclutador/suscripcion" element={
          <RutaProtegida rolesPermitidos={['owner', 'reclutador']}>
            <SuscripcionPage />
          </RutaProtegida>
        } />
        <Route path="/reclutador/candidatos/:candidatoId/assessments" element={
          <RutaProtegida rolesPermitidos={['owner', 'reclutador']}>
            <CandidatoAssessments />
          </RutaProtegida>
        } />
        <Route path="/reclutador/bolsa-talento" element={
          <RutaProtegida rolesPermitidos={['owner', 'reclutador']}>
            <BolsaTalentoPage />
          </RutaProtegida>
        } />
        <Route path="/reclutador/empresas/nueva" element={
          <RutaProtegida rolesPermitidos={['owner', 'reclutador']}>
            <CrearEmpresaPage />
          </RutaProtegida>
        } />

        {/* Portal Empresa */}
        <Route path="/empresa" element={
          <RutaProtegida rolesPermitidos={['owner', 'empresa']}>
            <DashboardEmpresa />
          </RutaProtegida>
        } />
        <Route path="/empresa/vacantes/:vacanteId" element={
          <RutaProtegida rolesPermitidos={['owner', 'empresa']}>
            <VacanteDetalleEmpresa />
          </RutaProtegida>
        } />

        {/* Resultado de pago (suscripción o desbloqueo, dLocal usa un solo callback) */}
        <Route path="/pagos/resultado" element={
          <RutaProtegida rolesPermitidos={['owner', 'reclutador', 'empresa']}>
            <PagoResultadoPage />
          </RutaProtegida>
        } />

        {/* 404 */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
