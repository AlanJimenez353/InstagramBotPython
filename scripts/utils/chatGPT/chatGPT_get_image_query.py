import requests
import os
from dotenv import load_dotenv, set_key
from openai import OpenAI
import re  # Importar el módulo de expresiones regulares para limpiar los nombres de archivo

# Carga las variables de entorno desde el archivo .env
env_path = 'C:\\Users\\Alan\\Documents\\CodeProjects\\Project Instagram\\.env'
load_dotenv(env_path)

# Variables OpenAI y Pexels
openai_api_key = os.getenv("OPENAI_API_KEY")
pexels_api_key = os.getenv("PEXELS_API_KEY")
client= OpenAI(api_key=openai_api_key)

# Directorio para guardar imágenes, obtenido desde la variable de entorno
image_dir = os.getenv("IMAGE_SAVE_PATH")
os.makedirs(image_dir, exist_ok=True)

# Manejo de la variable de entorno para el contador de imágenes
image_count = int(os.getenv("IMAGE_COUNTER", 0))
fact_id = int(os.getenv("FACT_ID", 0))

def update_env_variable(key, value):
    """Actualiza la variable de entorno y la persiste en el archivo .env."""
    os.environ[key] = str(value)
    set_key(env_path, key, str(value))

def clean_filename(filename):
    # Elimina caracteres no permitidos y espacios extras
    return re.sub(r'[\\/*?:"<>|\n]', '', filename).strip()

def get_image_query(fact, num_keywords=2):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are an assistant that generates exactly {num_keywords} single-word keywords for image searches based on scientific facts. The keywords should be distinct and concise."},
            {"role": "user", "content": f"Provide {num_keywords} distinct, single-word keywords for an image search that reflects this scientific fact: '{fact}'"}
        ]
    )
    
    # Extract keywords from the response
    if completion.choices and hasattr(completion.choices[0].message, 'content'):
        keywords = completion.choices[0].message.content.strip().split(', ')
        return keywords[:num_keywords]
    else:
        return []

def get_images_from_pexels(query, fact_id):
    global image_count
    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": pexels_api_key}
    params = {"query": query, "per_page": 3}
    response = requests.get(url, headers=headers, params=params)
    images = response.json().get('photos', [])
    
    for i, image in enumerate(images):
        img_url = image['src']['original']
        img_data = requests.get(img_url).content
        filename = f"fact{fact_id}_{clean_filename(query)}_image_{image_count}.jpg"
        image_path = os.path.join(image_dir, filename)
        with open(image_path, 'wb') as handler:
            handler.write(img_data)
        print(f"Descargada {img_url} como {filename}")
        image_count += 1  # Incrementa el contador de imágenes

    # Actualizar la variable de entorno IMAGE_COUNTER
    update_env_variable('IMAGE_COUNTER', image_count)

# Ejemplo de cómo llamar a la función
fact = "Desarrollo de vacunas de ARN mensajero para combatir enfermedades como la COVID-19."
keywords = get_image_query(fact, num_keywords=2)

for keyword in keywords:
    print(keyword)  # Para verificar que cada palabra clave se está procesando por separado
    get_images_from_pexels(keyword, fact_id)
    # Incrementa fact_id después de procesar cada palabra clave
    fact_id += 1 
    update_env_variable('FACT_ID', fact_id)
    print(f"FACT_ID is now {fact_id}")
    print(f"IMAGE_COUNTER is now {image_count}")
