# API Efemérides del Día 🗓️

Este proyecto es una aplicación móvil desarrollada en **Flutter** que muestra efemérides (eventos históricos importantes) para cualquier fecha. La aplicación se conecta a un API de **Python** que funciona como un servicio de backend, utilizando la inteligencia artificial de **Google Gemini** y una base de datos de **Supabase**.

El objetivo es tener una aplicación funcional y escalable que sea capaz de generar y almacenar contenido histórico dinámicamente.

## 🚀 Funcionalidades

### **API de Backend (Python/FastAPI)**
* **API RESTful**: Provee un endpoint para obtener efemérides.
* **Persistencia de Datos**: El API primero consulta la base de datos de **Supabase** para ver si la efeméride de una fecha ya existe.
* **Generación Inteligente**: Si la efeméride no se encuentra en la base de datos, el API utiliza la **IA de Google Gemini** para generar un evento histórico relevante para esa fecha.
* **Caché en Base de Datos**: Las efemérides generadas por Gemini se guardan automáticamente en Supabase, lo que reduce las peticiones a la API de Gemini y mejora la velocidad de respuesta para futuras consultas.


## ⚙️ Tecnologías y Herramientas

### **Backend (API)**
* **Python**: Lenguaje de programación.
* **FastAPI**: Framework web para construir APIs de alto rendimiento.
* **`uvicorn`**: Servidor web para correr la aplicación FastAPI.
* **`google-generativeai`**: Cliente de Python para la API de Gemini.
* **`supabase-py`**: Cliente para interactuar con la base de datos de Supabase.

### **Infraestructura**
* **Base de Datos**: Supabase.
* **Despliegue del API**: Render (Web Service).
* **Control de Versiones**: Git y GitHub.

## 📂 Estructura del Proyecto

El proyecto sigue una estructura de monorepo para mantener la aplicación y el API en un solo repositorio de forma organizada: