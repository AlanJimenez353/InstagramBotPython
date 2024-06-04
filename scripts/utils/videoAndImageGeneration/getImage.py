import requests
import os

def get_images_from_pexels(query):
    API_KEY = 'YOUR_PEXELS_API_KEY'  # Reemplaza con tu API key de Pexels
    url = "https://api.pexels.com/v1/search"
    headers = {
        "Authorization": API_KEY
    }
    params = {
        "query": query,
        "per_page": 10  # Número de imágenes a retornar
    }
    response = requests.get(url, headers=headers, params=params)
    images = response.json()['photos']
    for i, image in enumerate(images):
        # Descargar las imágenes
        img_url = image['src']['original']
        img_data = requests.get(img_url).content
        with open(os.path.join('downloaded_images', f'image_{i}.jpg'), 'wb') as handler:
            handler.write(img_data)
        print(f"Descargada {img_url}")
