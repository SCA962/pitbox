import { useState, useEffect } from 'react';

function App() {
  const [apiStatus, setApiStatus] = useState('cargando...');

  useEffect(() => {
    // Esta petición se dirige al backend gracias a la configuración del proxy en vite.config.js
    // Apuntamos a la ruta de chequeo de salud que creamos en FastAPI.
    fetch('/api/health-check')
      .then(res => {
        if (!res.ok) {
          throw new Error('La respuesta del backend no fue OK');
        }
        return res.json();
      })
      .then(data => {
        // El backend responde con {"status": "ok", ...}, así que usamos data.status
        setApiStatus(data.status);
      })
      .catch((error) => {
        console.error('Error al contactar el backend:', error);
        setApiStatus('error');
      });
  }, []);

  return (
    <div>
      <h1>Bienvenido al ERP para Talleres</h1>
      <p>Estado de la conexión con el Backend: <strong>{apiStatus}</strong></p>
    </div>
  );
}

export default App;
