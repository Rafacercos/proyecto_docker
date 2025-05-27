# Proyecto API con FastAPI, Streamlit y SQLAlchemy

## Descripción

Este proyecto es una API desarrollada con **FastAPI** que integra procesamiento de lenguaje natural mediante modelos de transformers, junto con un frontend sencillo usando **Streamlit**. 

El backend utiliza **SQLAlchemy (async)** para gestionar la persistencia de datos en una base SQLite, incluyendo autenticación de usuarios y almacenamiento de preguntas y respuestas. La API está diseñada para ser consumida por el frontend y para manejar de forma eficiente consultas relacionadas con inteligencia artificial.

---

## Resultados positivos logrados

- **API funcional y documentada:** Se logró desplegar una API con FastAPI que expone endpoints claros y bien definidos, accesibles desde `/docs`.
- **Persistencia de datos asíncrona:** Implementación exitosa de SQLite con SQLAlchemy en modo async, para manejar usuarios y dudas.
- **Frontend básico con Streamlit:** Una interfaz simple y accesible que consume la API y permite interacción con el usuario final.
- **Dockerización:** El proyecto está dockerizado, facilitando la gestión y despliegue en entornos controlados.
- **Manejo de dependencias y conflictos:** Resolución de conflictos de versiones para dependencias como numpy, transformers y demás librerías clave.

---

## Organización del repositorio

# Estructura del Proyecto

```bash
/proyecto_docker
│
├── backend/                       # Código del backend FastAPI
│   ├── main.py                   # Punto de entrada del servidor API
│   ├── models.py                 # Modelos ORM SQLAlchemy
│   ├── schemas.py                # Pydantic schemas para validación
│   ├── database.py               # Configuración de conexión y sesión async
│   ├── routers/                  # Endpoints organizados por funcionalidades
│   ├── requirements.txt          # Dependencias del backend
│   └── Dockerfile                # Dockerfile para backend
│
├── frontend/                     # Código del frontend Streamlit
│   ├── app.py                    # Script principal de Streamlit
│   ├── requirements.txt          # Dependencias del frontend
│   └── Dockerfile                # Dockerfile para frontend
│
├── docker-compose.yml            # Orquestación de servicios backend y frontend
└── README.md                     # Este archivo
'''

## Cómo ejecutar

1. Clona el repositorio:
   ```bash
   git clone <url-del-repositorio>
   cd proyecto_docker
2. Accede a:

- API FastAPI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Frontend Streamlit: [http://localhost:8501](http://localhost:8501)
3. Para detener y eliminar contenedores cuando termines:

```bash
docker-compose down


