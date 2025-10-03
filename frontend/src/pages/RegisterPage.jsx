import React, { useState } from 'react';

// Reutilizamos los mismos estilos que LoginPage por ahora
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
    backgroundColor: '#28a745', // Un color verde para diferenciar
    color: 'white',
    fontSize: '1rem',
    cursor: 'pointer',
  },
};

const RegisterPage = () => {
  const [tenantName, setTenantName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    // Lógica de registro irá aquí
    console.log('Intentando registrar con:', { tenantName, email, password });
  };

  return (
    <div style={styles.container}>
      <div style={styles.formContainer}>
        <h2 style={styles.title}>Crear Nueva Cuenta</h2>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Nombre del Taller"
            style={styles.input}
            value={tenantName}
            onChange={(e) => setTenantName(e.target.value)}
            required
          />
          <input
            type="email"
            placeholder="Correo Electrónico del Administrador"
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
          <input
            type="password"
            placeholder="Confirmar Contraseña"
            style={styles.input}
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
          />
          <button type="submit" style={styles.button}>
            Registrarse
          </button>
        </form>
      </div>
    </div>
  );
};

export default RegisterPage;
