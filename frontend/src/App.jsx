import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardPage from './pages/DashboardPage'; // 1. Importar el nuevo componente

// Función para verificar si hay un token de acceso
const isAuthenticated = () => {
  return localStorage.getItem('accessToken') !== null;
};

// Componente de Ruta Privada
const PrivateRoute = ({ children }) => {
  return isAuthenticated() ? children : <Navigate to="/login" />;
};

function App() {
  return (
    <Router>
      <Routes>
        {/* Rutas públicas */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />

        {/* Ruta principal: redirige según el estado de autenticación */}
        <Route 
          path="/"
          element={ 
            isAuthenticated() ? <Navigate to="/dashboard" /> : <Navigate to="/login" />
          }
        />

        {/* Ruta privada para el Dashboard */}
        <Route 
          path="/dashboard" 
          element={
            <PrivateRoute>
              <DashboardPage />
            </PrivateRoute>
          }
        />

      </Routes>
    </Router>
  );
}

export default App;
