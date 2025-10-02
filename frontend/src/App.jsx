import { useState, useEffect } from 'react';

function App() {
  const [apiStatus, setApiStatus] = useState('cargando...');

  useEffect(() => {
    // El proxy de Vite redirigirá esta petición a http://backend:8000/api/health
    fetch('/api/health')
      .then(res => res.json())
      .then(data => setApiStatus(data.status))
      .catch(() => setApiStatus('error'));
  }, []);

  return (
    <div>
      <h1>Bienvenido al ERP para Talleres</h1>
      <p>Estado de la conexión con el Backend: <strong>{apiStatus}</strong></p>
    </div>
  );
}

export default App;
