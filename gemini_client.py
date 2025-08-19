# gemini_client.py

import os
import time
import re
from datetime import date, datetime, timedelta
from dotenv import load_dotenv
import google.generativeai as genai
from fastapi import HTTPException, status

# --- Configuración del Cliente de Gemini ---
# Cargar variables de entorno del archivo .env.
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("La variable de entorno GEMINI_API_KEY no está configurada en el archivo .env.")

# Conectamos con la API de Gemini usando la clave obtenida.
genai.configure(api_key=GEMINI_API_KEY)

# Variables globales para el manejo de la cuota (rate limit) de Gemini.
last_gemini_call_time = datetime.now()
MIN_DELAY_SECONDS = int(os.getenv("MIN_DELAY_SECONDS", 60))

def get_model():
    """
    Función para buscar y retornar un modelo de Gemini disponible que soporte
    la generación de contenido (textos).
    """
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Usando el modelo disponible: {m.name}")
            return genai.GenerativeModel(m.name)
    raise Exception("No se encontró ningún modelo de Gemini que soporte 'generateContent'.")

try:
    # Intenta obtener un modelo válido al iniciar el módulo.
    model = get_model()
except Exception as e:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

async def get_gemini_event(event_date: date):
    """
    Función asíncrona que consulta a la API de Gemini para obtener un evento histórico,
    gestionando la cuota de llamadas.
    """
    global last_gemini_call_time
    """
    current_time = datetime.now()
    time_since_last_call = (current_time - last_gemini_call_time).total_seconds()
    
    if time_since_last_call < MIN_DELAY_SECONDS:
        wait_time = MIN_DELAY_SECONDS - time_since_last_call
        print(f"Esperando {wait_time:.2f} segundos para cumplir con la cuota de la API.")
        time.sleep(wait_time)
        
    try:
        """
    prompt = (f"Dame un evento histórico importante ocurrido el {event_date.day} de {event_date.strftime('%B')} "
                  "en español, con un título y una descripción corta. No uses comillas dobles, saltos de línea ni "
                  "caracteres especiales. Formato: Titulo del evento | Descripción del evento.")
        
    response = await model.generate_content_async(prompt)
    last_gemini_call_time = datetime.now()
    text_response = response.text.replace('**', '').strip()
        
    if '|' in text_response:
        titulo, evento = text_response.split('|', 1)
        return titulo.strip(), evento.strip()
    else:
        print(f"Advertencia: La respuesta de Gemini no tiene el formato esperado. Respuesta: {text_response}")
        return None, None
    """
    except Exception as e:
        error_string = str(e)
        if "429" in error_string:
            retry_delay_seconds = 60
            match = re.search(r"retry_delay {\s*seconds: (\d+)", error_string)
            if match:
                retry_delay_seconds = int(match.group(1))

            next_available_time = datetime.now() + timedelta(seconds=retry_delay_seconds)
            next_time_str = next_available_time.strftime("%H:%M:%S")
            
            error_details = ""
            if "generate_content_free_tier_requests" in error_string:
                error_details = "Se excedió el límite de peticiones (requests)."
            elif "generate_content_free_tier_input_token_count" in error_string:
                error_details = "Se excedió el límite de tokens de entrada (input token count)."
            else:
                error_details = "Se excedió un límite de cuota de la API."

            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS, 
                detail=f"Has excedido el límite de consultas a la API de Gemini. {error_details} Puedes intentarlo de nuevo a partir de las {next_time_str}."
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ocurrió un error inesperado al consultar la API de Gemini: {e}"
            )
    """
    
