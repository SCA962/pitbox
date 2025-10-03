document.addEventListener('DOMContentLoaded', () => {
    const API_URL = 'http://127.0.0.1:8000/api'; // La URL base de tu backend FastAPI

    const loginContainer = document.getElementById('login-container');
    const dashboardContainer = document.getElementById('dashboard-container');
    const loginForm = document.getElementById('login-form');
    const logoutButton = document.getElementById('logout-button');
    const fetchClientsButton = document.getElementById('fetch-clients-button');
    const welcomeMessage = document.getElementById('welcome-message');
    const clientsList = document.getElementById('clients-list');
    const loginError = document.getElementById('login-error');
    const dashboardError = document.getElementById('dashboard-error');

    // --- Verificación Inicial ---
    const token = localStorage.getItem('accessToken');
    if (token) {
        showDashboard();
    } else {
        showLogin();
    }

    // --- Event Listeners ---
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        loginError.textContent = '';
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        const formData = new URLSearchParams();
        formData.append('username', email);
        formData.append('password', password);

        try {
            const response = await fetch(`${API_URL}/token`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Error en el inicio de sesión');
            }

            const data = await response.json();
            localStorage.setItem('accessToken', data.access_token);
            showDashboard();
        } catch (error) {
            loginError.textContent = `Error: ${error.message}`;
        }
    });

    logoutButton.addEventListener('click', () => {
        localStorage.removeItem('accessToken');
        showLogin();
    });

    fetchClientsButton.addEventListener('click', async () => {
        dashboardError.textContent = '';
        clientsList.innerHTML = '<li>Cargando...</li>';
        const currentToken = localStorage.getItem('accessToken');

        try {
            const response = await fetch(`${API_URL}/clients/`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${currentToken}`,
                },
            });

            if (!response.ok) {
                const errorData = await response.json();
                // Si el token expiró (o es inválido), el backend devuelve 401
                if (response.status === 401) {
                    logoutButton.click(); // Forzamos logout
                }
                throw new Error(errorData.detail || 'No se pudo cargar los clientes');
            }

            const clients = await response.json();
            renderClients(clients);

        } catch (error) {
            dashboardError.textContent = `Error: ${error.message}`;
            clientsList.innerHTML = '';
        }
    });


    // --- Funciones de UI ---
    function showLogin() {
        loginContainer.style.display = 'block';
        dashboardContainer.style.display = 'none';
    }

    function showDashboard() {
        loginContainer.style.display = 'none';
        dashboardContainer.style.display = 'block';
        welcomeMessage.textContent = '¡Bienvenido! Dashboard de Demostración';
        clientsList.innerHTML = ''; // Limpiar lista al mostrar dashboard
        loginError.textContent = '';
        dashboardError.textContent = '';
    }
    
    function renderClients(clients) {
        clientsList.innerHTML = '';
        if (clients.length === 0) {
            clientsList.innerHTML = '<li>No tienes clientes registrados en tu tenant.</li>';
            return;
        }
        clients.forEach(client => {
            const li = document.createElement('li');
            li.textContent = `ID: ${client.id} - Nombre: ${client.name} - Email: ${client.email}`;
            clientsList.appendChild(li);
        });
    }
});
