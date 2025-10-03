import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';

// Por ahora, asumimos que no hay un usuario autenticado.
// Más adelante, aquí habrá lógica para verificar el token JWT.
const isAuthenticated = false;

function App() {
  return (
    <Router>
      <Routes>
        {/* Ruta principal: si estás autenticado va al dashboard, si no, al login */}
        <Route 
          path="/" 
          element={isAuthenticated ? <Navigate to="/dashboard" /> : <Navigate to="/login" />}
        />
        
        {/* Rutas públicas */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/registro" element={<RegisterPage />} />

        {/* Rutas privadas (ejemplo) */}
        {/* <Route path="/dashboard" element={isAuthenticated ? <DashboardPage /> : <Navigate to="/login" />} /> */}

      </Routes>
    </Router>
  );
}

export default App;
