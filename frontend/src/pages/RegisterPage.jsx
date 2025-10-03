import React, { useState } from 'react';

// Estilos (los mismos que en LoginPage para consistencia)
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
    backgroundColor: '#28a745', // Un verde para diferenciar de login
    color: 'white',
    fontSize: '1rem',
    cursor: 'pointer',
  },
  // Estilo para mensajes de error o éxito
  message: {
      textAlign: 'center',
      padding: '10px',
      marginTop: '10px',
      borderRadius: '5px',
      color: 'white',
  },
  error: {
      backgroundColor: '#dc3545', // Rojo para errores
  },
  success: {
      backgroundColor: '#28a745', // Verde para éxito
  }
};

const RegisterPage = () => {
  const [workshopName, setWorkshopName] = useState('');
  const [adminEmail, setAdminEmail] = useState('');
  const [adminPassword, setAdminPassword] = useState('');
  const [message, setMessage] = useState(null);
  const [isError, setIsError] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setMessage(null);
    setIsError(false);

    try {
      const response = await fetch('http://localhost:8000/api/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          workshop_name: workshopName,
          admin_email: adminEmail,
          admin_password: adminPassword,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        // Si la respuesta no es 2xx, lanza un error con el detalle del backend
        throw new Error(data.detail || 'Ocurrió un error al registrar.');
      }

      // Si el registro es exitoso
      setIsError(false);
      setMessage('¡Registro exitoso! Ahora puedes iniciar sesión.');
      // Opcional: Redirigir a la página de login después de unos segundos

    } catch (error) {
      setIsError(true);
      setMessage(error.message);
    }
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
            value={workshopName}
            onChange={(e) => setWorkshopName(e.target.value)}
            required
          />
          <input
            type="email"
            placeholder="Correo Electrónico del Administrador"
            style={styles.input}
            value={adminEmail}
            onChange={(e) => setAdminEmail(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Contraseña del Administrador"
            style={styles.input}
            value={adminPassword}
            onChange={(e) => setAdminPassword(e.target.value)}
            required
          />
          <button type="submit" style={styles.button}>
            Registrarse
          </button>
        </form>
        {message && (
            <div style={{ ...styles.message, ...(isError ? styles.error : styles.success) }}>
                {message}
            </div>
        )}
      </div>
    </div>
  );
};

export default RegisterPage;
