# Nuestras Reglas de Oro para el Proyecto PitBox

Este documento es nuestro recordatorio vivo de las reglas y estándares que hemos acordado para mantener nuestro proyecto limpio, profesional y escalable. Es nuestra "Constitución del Proyecto".

### 1. Estructura de Backend Modular
Mantenemos una estricta separación de responsabilidades en el backend para un código limpio y escalable, dividida en:
- `routers/`: Define los endpoints de la API.
- `schemas/`: Define los modelos de datos de Pydantic para validación y serialización.
- `crud/`: Contiene las funciones de Lógica de Negocio y acceso a la base de datos (Crear, Leer, Actualizar, Borrar).
- `models/`: Define los modelos de la base de datos con SQLAlchemy.
- `database.py`: Configura la conexión a la base de datos.
- `security.py`: Maneja la autenticación, contraseñas y tokens.

### 2. Prefijo `/api` Global
Todas las rutas de la API deben estar unificadas bajo el prefijo `/api`. Esto proporciona una organización clara, evita colisiones de nombres y facilita la configuración de proxies inversos en producción.

### 3. Validación Rigurosa con Schemas
Los modelos de Pydantic definidos en `schemas.py` son la **única fuente de verdad** para los contratos de datos de nuestra API. La estructura de todos los datos que entran y salen debe corresponderse estrictamente con estos modelos.

### 4. Flujo de Trabajo Git Disciplinado
- **Commits Atómicos:** Cada commit debe representar un único cambio lógico completo.
- **Mensajes Claros:** Los mensajes de commit deben ser descriptivos (ej. "feat(auth): ...", "fix(crud): ...").
- **Tags para Hitos:** Usamos `git tag` para marcar versiones y puntos de control importantes del proyecto (ej. `v0.1-backend-up`).

### 5. Análisis de Impacto y Ciclo de Vida del Dato
Antes de realizar cualquier modificación, es obligatorio realizar un **análisis de impacto holístico**. Se debe trazar el ciclo de vida completo del dato o la lógica afectada:
- **Origen:** ¿Dónde se origina el dato? (ej. un formulario en el frontend).
- **Transporte:** ¿Cómo viaja? (ej. una llamada a la API).
- **Procesamiento:** ¿Qué partes del código (funciones, clases) lo consumen o lo transforman?
- **Destino:** ¿Dónde se almacena o utiliza finalmente? (ej. una o varias tablas en la base de datos).
Este análisis asegura que los cambios sean completos, consistentes y no dejen efectos secundarios inesperados.

### 6. Estandarización Profesional del Código
Adoptamos y aplicamos estándares de código profesionales para mantener la legibilidad, consistencia y mantenibilidad del proyecto a largo plazo.

#### A. Backend (Python / FastAPI)
- **Guía de Estilo:** Se sigue **PEP 8** de forma estricta.
- **Nombrado:**
    - Variables y Funciones: `snake_case` (ej. `workshop_name`).
    - Clases: `PascalCase` (ej. `TenantRegistration`).
    - Constantes: `UPPER_SNAKE_CASE` (ej. `DATABASE_URL`).
- **Importaciones:** Se ordenan según PEP 8 (librerías estándar, luego terceros, luego de la aplicación). Se puede usar `isort` para automatizarlo.
- **Docstrings:** Todas las funciones, clases y módulos públicos deben tener docstrings explicando su propósito.
- **Nombrado en API (JSON):** Se usará `snake_case` para los campos en los JSON de la API para mantener consistencia con el backend.

#### B. Frontend (JavaScript / Vue.js)
- **Guía de Estilo:** Se sigue la **Guía de Estilo Oficial de Vue.js**.
- **Nombrado:**
    - Nombres de archivos de componentes: `PascalCase` (ej. `RegisterForm.vue`).
    - Props (definición en JS): `camelCase` (ej. `myProp`).
    - Props (uso en plantilla HTML): `kebab-case` (ej. `:my-prop="..."`).
    - Variables y Funciones: `camelCase` (ej. `workshopName`).
- **Linting y Formateo:** Se recomienda el uso de `ESLint` y `Prettier` para garantizar la consistencia automática.
