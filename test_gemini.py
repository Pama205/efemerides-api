import asyncio
from datetime import date
from gemini_client import get_gemini_event
from dotenv import load_dotenv

# Carga las variables de entorno para que gemini_client pueda acceder a ellas
load_dotenv()

async def test_client():
    """
    Función asíncrona para probar el funcionamiento de get_gemini_event.
    """
    print("Iniciando prueba de conexión con la API de Gemini...")
    
    # Usa una fecha de prueba.
    test_date = date(2025, 8, 21)
    
    try:
        # Llama a la función get_gemini_event.
        titulo, evento = await get_gemini_event(test_date)

        if titulo and evento:
            print("\n✅ Conexión exitosa. ¡Datos recibidos!")
            print("-" * 40)
            print(f"Título: {titulo}")
            print(f"Evento: {evento}")
            print("-" * 40)
        else:
            print("\n❌ La conexión fue exitosa, pero la respuesta no tiene el formato esperado.")

    except Exception as e:
        print(f"\n❌ ¡Error en la prueba! No se pudo obtener la efeméride.")
        print(f"Detalles del error: {e}")

# Ejecuta la función de prueba.
if __name__ == "__main__":
    asyncio.run(test_client())