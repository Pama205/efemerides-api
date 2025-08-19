# main.py

import os
from datetime import date
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from supabase import create_client, Client
from gemini_client import get_gemini_event

# --- Configuración Inicial ---
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Las variables de entorno no están configuradas correctamente. Revisa el archivo .env")

# --- Configurar el Cliente de Supabase ---
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Inicializar la Aplicación FastAPI ---
app = FastAPI()

# --- Endpoint de la API Principal ---
@app.get("/efemeride")
async def get_efemeride_for_date(fecha: date = date.today()):
    """
    Endpoint principal para buscar un evento histórico.
    """
    print(f"Consultando efeméride para la fecha: {fecha}")

    # Paso 1: Buscar la efeméride en Supabase
    try:
        query = supabase.from_('efemerides').select('*').eq('fecha_consulta', fecha).execute()
        data = query.data
        
        if data:
            print("Efeméride encontrada en la base de datos.")
            return data
            
    except Exception as e:
        print(f"Error al buscar en Supabase: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Error del servidor al buscar en la base de datos."
        )

    # Paso 2: Si no se encuentra, generar con Gemini y guardar en la DB
    print("Efeméride no encontrada. Generando con Gemini...")
    titulo, evento = await get_gemini_event(fecha)
    
    if titulo and evento:
        try:
            insert_data = {
                'fecha_consulta': str(fecha),
                'titulo': titulo,
                'evento': evento
            }
            inserted_item = supabase.from_('efemerides').insert(insert_data).execute()
            print("Efeméride generada y guardada exitosamente.")
            return inserted_item.data
            
        except Exception as e:
            print(f"Error al insertar en Supabase: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail="Error del servidor al guardar la efeméride."
            )
    else:
        print("No se pudo generar el evento con Gemini.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="No se pudo generar un evento histórico para la fecha solicitada."
        )