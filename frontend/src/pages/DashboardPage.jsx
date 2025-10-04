import React from 'react';

const styles = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
    height: '100vh',
    backgroundColor: '#f0f2f5',
  },
  title: {
    fontSize: '2.5rem',
    color: '#333',
  },
  subtitle: {
    fontSize: '1.2rem',
    color: '#6c757d',
  }
};

const DashboardPage = () => {
  return (
    <div style={styles.container}>
      <h1 style={styles.title}>¡Bienvenido a PitBox!</h1>
      <p style={styles.subtitle}>Has iniciado sesión correctamente.</p>
      {/* Aquí irá el contenido principal del dashboard */}
    </div>
  );
};

export default DashboardPage;
