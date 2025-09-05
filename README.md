# 🚀 FastAPI Clean Architecture TodoList

Una API REST moderna para gestión de tareas (TODOs) construida con **FastAPI** y **PostgreSQL**, implementando **Clean Architecture** con autenticación JWT y paginación por cursor.

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Arquitectura](#-arquitectura)
- [Tecnologías](#-tecnologías)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Uso con Docker](#-uso-con-docker)
- [API Endpoints](#-api-endpoints)
- [Ejemplos de Uso](#-ejemplos-de-uso)
- [Desarrollo](#-desarrollo)

## ✨ Características

- **🔐 Autenticación JWT**: Sistema completo de autenticación con access tokens y refresh tokens
- **📄 Paginación por Cursor**: Paginación eficiente para grandes volúmenes de datos
- **🏗️ Clean Architecture**: Separación clara de responsabilidades entre capas
- **🐳 Docker Ready**: Configuración completa con Docker Compose
- **📊 PostgreSQL**: Base de datos robusta con migraciones con Alembic
- **🔄 Manejo de Excepciones**: Sistema de excepciones por capas arquitectónicas
- **📝 Documentación Automática**: Swagger UI integrado
- **⚡ Alto Rendimiento**: Optimizado para alta concurrencia

## 🏗️ Arquitectura

El proyecto implementa **Clean Architecture** con las siguientes capas:

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                       │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐  │
│  │   Auth Router   │  │   Task Router   │  │ Exceptions  │  │
│  └─────────────────┘  └─────────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                        │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐  │
│  │  Auth Service   │  │  Task Service   │  │ Exceptions  │  │
│  └─────────────────┘  └─────────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                      DOMAIN LAYER                           │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐  │
│  │   Entities      │  │   Repositories  │  │ Unit of Work │  │
│  └─────────────────┘  └─────────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                  INFRASTRUCTURE LAYER                       │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐  │
│  │   Repositories  │  │      DTOs       │  │   Database   │  │
│  └─────────────────┘  └─────────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Principios de Clean Architecture

- **Independencia de Frameworks**: La lógica de negocio no depende de FastAPI
- **Testabilidad**: Cada capa puede ser probada independientemente
- **Independencia de UI**: La interfaz puede cambiar sin afectar la lógica de negocio
- **Independencia de Base de Datos**: La lógica de negocio no depende de PostgreSQL
- **Independencia de Agentes Externos**: La lógica de negocio no conoce el mundo exterior

## 🛠️ Tecnologías

### Backend

- **FastAPI**: Framework web moderno y rápido para APIs
- **SQLModel**: ORM moderno basado en SQLAlchemy y Pydantic
- **PostgreSQL**: Base de datos relacional robusta
- **Alembic**: Sistema de migraciones de base de datos
- **JWT**: Autenticación basada en tokens
- **Pydantic**: Validación de datos y serialización

### Desarrollo

- **Poetry**: Gestión de dependencias
- **Docker**: Containerización
- **Docker Compose**: Orquestación de contenedores
- **Uvicorn**: Servidor ASGI

## 📁 Estructura del Proyecto

```
fastApi-cleanArch-todoList/
├── app/
│   ├── application/           # Capa de Aplicación
│   │   ├── services/         # Servicios de negocio
│   │   │   ├── auth_service.py
│   │   │   └── task_service.py
│   │   └── exceptions.py     # Excepciones de aplicación
│   ├── core/                 # Configuración central
│   │   └── config.py         # Configuración de la aplicación
│   ├── domain/               # Capa de Dominio
│   │   ├── entities/         # Entidades de negocio
│   │   │   ├── users.py
│   │   │   └── tasks.py
│   │   ├── repositories/     # Interfaces de repositorios
│   │   │   ├── iuser_repository.py
│   │   │   └── itask_repository.py
│   │   └── unit_of_work.py   # Patrón Unit of Work
│   ├── infrastructure/       # Capa de Infraestructura
│   │   ├── common/           # Servicios comunes
│   │   │   ├── auth_service.py
│   │   │   ├── paginated_results.py
│   │   │   └── sql_alchemy_unit_of_work.py
│   │   ├── dtos/             # Data Transfer Objects
│   │   │   ├── user_dtos.py
│   │   │   └── task_dtos.py
│   │   ├── persistence/      # Configuración de persistencia
│   │   │   └── entities_configuration.py
│   │   ├── repositories/     # Implementaciones de repositorios
│   │   │   ├── user_repository.py
│   │   │   └── task_repository.py
│   │   ├── database.py       # Configuración de base de datos
│   │   └── exceptions.py     # Excepciones de infraestructura
│   ├── presentation/         # Capa de Presentación
│   │   ├── routers/          # Routers de FastAPI
│   │   │   ├── auth_router.py
│   │   │   └── task_router.py
│   │   └── exceptions/       # Excepciones HTTP
│   │       └── exceptions.py
│   └── main.py              # Punto de entrada de la aplicación
├── alembic/                 # Migraciones de base de datos
├── docker-compose.yml       # Configuración de Docker Compose
├── dockerfile              # Imagen de Docker
├── env.example             # Variables de entorno de ejemplo
├── pyproject.toml          # Configuración de Poetry
├── run.py                  # Script de ejecución
└── README.md               # Este archivo
```

## 🚀 Instalación

### Prerrequisitos

- Python 3.11+
- Poetry
- PostgreSQL 16+
- Docker y Docker Compose (opcional)

### Instalación Local

1. **Clonar el repositorio**

   ```bash
   git clone <repository-url>
   cd fastApi-cleanArch-todoList
   ```

2. **Instalar dependencias con Poetry**

   ```bash
   poetry install
   ```

3. **Activar el entorno virtual**

   ```bash
   poetry shell
   ```

4. **Configurar variables de entorno**

   ```bash
   cp env.example .env
   # Editar .env con tus configuraciones
   ```

5. **Configurar la base de datos**

   ```bash
   # Crear la base de datos PostgreSQL
   createdb todolist_db
   ```

6. **Ejecutar migraciones**

   ```bash
   alembic upgrade head
   ```

7. **Ejecutar la aplicación**

   ```bash
   python run.py
   ```

La aplicación estará disponible en `http://localhost:8000`

## ⚙️ Configuración

### Variables de Entorno

Copia `env.example` a `.env` y configura las siguientes variables:

```env
# Application Configuration
APP_NAME=FastAPI Clean Architecture TodoList
DEBUG=True
ENVIRONMENT=development
HOST=0.0.0.0
PORT=8000

# Database Configuration
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/todolist_db
POSTGRES_DB=todolist_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### Configuración de Base de Datos

El proyecto usa **Alembic** para las migraciones. Para crear una nueva migración:

```bash
alembic revision --autogenerate -m "Descripción del cambio"
alembic upgrade head
```

## 🐳 Uso con Docker

### Levantar con Docker Compose

1. **Configurar variables de entorno**

   ```bash
   cp env.example .env
   ```

2. **Levantar los servicios**

   ```bash
   docker-compose up -d
   ```

3. **Ejecutar migraciones**

   ```bash
   docker-compose exec app alembic upgrade head
   ```

4. **Verificar que todo funciona**

   ```bash
   docker-compose ps
   ```

### Comandos Docker útiles

```bash
# Ver logs
docker-compose logs -f app

# Ejecutar comandos en el contenedor
docker-compose exec app bash

# Reiniciar servicios
docker-compose restart

# Detener servicios
docker-compose down

# Detener y eliminar volúmenes
docker-compose down -v
```

## 📚 API Endpoints

### Autenticación

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/v1/auth/signup` | Registrar nuevo usuario |
| POST | `/api/v1/auth/signin` | Iniciar sesión |
| POST | `/api/v1/auth/refresh` | Renovar access token |
| POST | `/api/v1/auth/logout` | Cerrar sesión |

### Tareas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/v1/tasks/` | Crear nueva tarea |
| GET | `/api/v1/tasks/` | Listar tareas (con paginación) |
| GET | `/api/v1/tasks/{id}` | Obtener tarea por ID |
| PUT | `/api/v1/tasks/{id}` | Actualizar tarea |
| DELETE | `/api/v1/tasks/{id}` | Eliminar tarea |

### Documentación

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 💡 Ejemplos de Uso

### Registro de Usuario

```bash
curl -X POST "http://localhost:8000/api/v1/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Juan Pérez",
    "email": "juan@example.com",
    "password": "password123"
  }'
```

### Inicio de Sesión

```bash
curl -X POST "http://localhost:8000/api/v1/auth/signin" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "juan@example.com",
    "password": "password123"
  }'
```

### Crear Tarea

```bash
curl -X POST "http://localhost:8000/api/v1/tasks/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "title": "Mi primera tarea",
    "description": "Esta es una tarea de ejemplo",
    "status": "PENDING",
    "user_id": "user-uuid-here"
  }'
```

### Listar Tareas con Paginación

```bash
curl -X GET "http://localhost:8000/api/v1/tasks/?user_id=user-uuid-here&page_size=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 🔧 Desarrollo


### Patrones Implementados

- **Repository Pattern**: Abstracción del acceso a datos
- **Unit of Work**: Coordinación de transacciones
- **Dependency Injection**: Inyección de dependencias con FastAPI
- **Cursor Pagination**: Paginación eficiente para grandes datasets

### Testing

```bash
# Ejecutar tests (cuando estén implementados)
poetry run pytest

# Con cobertura
poetry run pytest --cov=app
```

### Linting y Formateo

```bash
# Linting
poetry run flake8 app/

# Formateo
poetry run black app/

# Verificar tipos
poetry run mypy app/
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request


---
