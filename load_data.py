import os
import pandas as pd
from dotenv import load_dotenv
from supabase import create_client, Client

# --- Configuración ---
# Cargar variables de entorno del archivo .env
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Las variables de entorno SUPABASE_URL y SUPABASE_KEY no están configuradas en el archivo .env")

# Crear el cliente de Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def load_data_to_supabase(file_path: str, table_name: str):
    """
    Carga los datos de un archivo CSV en una tabla de Supabase.

    Args:
        file_path (str): La ruta al archivo CSV.
        table_name (str): El nombre de la tabla de destino en Supabase.
    """
    print(f"Iniciando la carga de datos del archivo {file_path} a la tabla '{table_name}'...")
    
    try:
        # Lee el archivo CSV con pandas.
        # Asegúrate de que los nombres de las columnas en el CSV coincidan con los de tu tabla.
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{file_path}'.")
        return
    
    # Se crea una lista para almacenar los diccionarios de datos.
    data_to_insert = []
    
    # Itera sobre cada fila del DataFrame de pandas.
    for index, row in df.iterrows():
        # Crea un diccionario con los datos de la fila actual.
        # Los nombres de las claves deben coincidir con los de tus columnas de Supabase.
        record = {
            'fecha_consulta': row['fecha_consulta'],
            'titulo': row['titulo'],
            'evento': row['evento']
        }
        data_to_insert.append(record)

    # Intenta insertar todos los registros en un solo lote para mayor eficiencia.
    try:
        print(f"Intentando insertar {len(data_to_insert)} registros...")
        inserted_records = supabase.from_(table_name).insert(data_to_insert).execute()
        
        # Si la inserción fue exitosa, la respuesta tendrá datos.
        if inserted_records.data:
            print("✔ Carga masiva completada exitosamente.")
            print(f"Registros insertados: {len(inserted_records.data)}")
        else:
            print("No se insertaron registros. La tabla ya podría contener estos datos.")

    except Exception as e:
        # Maneja específicamente los errores de restricción de unicidad, que son comunes.
        if "unique_violation" in str(e):
            print("\nAdvertencia: Falló la carga masiva debido a registros duplicados.")
            print("Intentando la inserción de registros de forma individual...")
            
            # Intenta insertar uno por uno para saltar los duplicados.
            for record in data_to_insert:
                try:
                    supabase.from_(table_name).insert(record).execute()
                    print(f"-> Registro para '{record['fecha_consulta']}' insertado.")
                except Exception as individual_e:
                    if "unique_violation" in str(individual_e):
                        print(f"-> Registro para '{record['fecha_consulta']}' ya existe. Saltando...")
                    else:
                        print(f"-> Error al insertar el registro para '{record['fecha_consulta']}': {individual_e}")
        else:
            print(f"\nError fatal en la carga de datos: {e}")
            
# --- Punto de entrada del script ---
if __name__ == "__main__":
    load_data_to_supabase('efemerides_agosto.csv', 'efemerides')