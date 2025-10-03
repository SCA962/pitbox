import React, { useState } from 'react';
import { Link } from 'react-router-dom'; // Importamos Link

// Estilos...
const styles = {
  container: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    height: '100vh',
    backgroundColor: '#f0f2f5',
  },
  formContainer: {
    padding: '2rem',
    boxShadow: '0 4px 8px 0 rgba(0,0,0,0.2)',
    borderRadius: '8px',
    backgroundColor: 'white',
    width: '100%',
    maxWidth: '400px',
  },
  title: {
    textAlign: 'center',
    marginBottom: '1.5rem',
    color: '#333',
  },
  input: {
    width: '100%',
    padding: '0.75rem',
    border: '1px solid #ccc',
    borderRadius: '4px',
    marginBottom: '1rem',
    boxSizing: 'border-box',
  },
  button: {
    width: '100%',
    padding: '0.75rem',
    border: 'none',
    borderRadius: '4px',
    backgroundColor: '#007bff',
    color: 'white',
    fontSize: '1rem',
    cursor: 'pointer',
  },
  separator: {
    textAlign: 'center',
    margin: '1rem 0',
    color: '#6c757d',
  },
  link: {
    display: 'block',
    textAlign: 'center',
    color: '#007bff',
    textDecoration: 'none',
    marginTop: '0.5rem',
  }
};

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    console.log('Intentando iniciar sesión con:', { email, password });
  };

  return (
    <div style={styles.container}>
      <div style={styles.formContainer}>
        <h2 style={styles.title}>Iniciar Sesión</h2>
        <form onSubmit={handleSubmit}>
          <input
            type="email"
            placeholder="Correo Electrónico"
            style={styles.input}
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Contraseña"
            style={styles.input}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <button type="submit" style={styles.button}>
            Entrar
          </button>
        </form>
        <div style={styles.separator}>o</div>
        {/* Enlace a la página de registro */}
        <Link to="/registro" style={styles.link}>
          Regístrese
        </Link>
      </div>
    </div>
  );
};

export default LoginPage;
