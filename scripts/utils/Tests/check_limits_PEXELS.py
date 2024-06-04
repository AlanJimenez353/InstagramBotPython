import requests
import time
from dotenv import load_dotenv
import os

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Obtener la clave API desde las variables de entorno
pexels_api_key = os.getenv("PEXELS_API_KEY")
if not pexels_api_key:
    raise ValueError("PEXELS_API_KEY is not set in the environment variables.")

def check_rate_limits(headers):
    limit = int(headers.get('X-Ratelimit-Limit', 0))
    remaining = int(headers.get('X-Ratelimit-Remaining', 0))
    reset = int(headers.get('X-Ratelimit-Reset', 0))
    
    print(f"Total Requests Limit: {limit}")
    print(f"Requests Remaining: {remaining}")
    print(f"Limit Resets At: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(reset))}")

    if remaining == 0:
        reset_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(reset))
        raise Exception(f"Rate limit exceeded. Limit resets at {reset_time}.")

def get_images_from_pexels(query):
    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": pexels_api_key}
    params = {"query": query, "per_page": 3}
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        check_rate_limits(response.headers)
        images = response.json().get('photos', [])
        for image in images:
            print("Image URL:", image['src']['original'])
    else:
        print("Failed to fetch images from Pexels. Status code:", response.status_code)
        print("Response:", response.text)

# Uso de la función
get_images_from_pexels("Nature")
