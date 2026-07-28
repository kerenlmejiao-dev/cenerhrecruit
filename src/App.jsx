/**
 * CENERH RECRUIT OS - App Principal
 * Gestión de rutas y componentes
 */

import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import RegistroPage from './pages/RegistroPage';
import TestsPage from './pages/TestsPage';
import ResultadosPage from './pages/ResultadosPage';
import AdminDashboard from './pages/AdminDashboard';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Candidatos */}
        <Route path="/" element={<RegistroPage />} />
        <Route path="/tests" element={<TestsPage />} />
        <Route path="/resultados" element={<ResultadosPage />} />

        {/* Admin */}
        <Route path="/admin" element={<AdminDashboard />} />

        {/* 404 */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
