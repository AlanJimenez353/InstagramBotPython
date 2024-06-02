# import os
# from scripts.utils.chatgpt_utils import get_fun_facts
# from scripts.utils.video_utils import generate_video_with_facts
# from scripts.utils.instagram_utils import post_video_to_instagram
# 
# # Cargar variables de entorno
# from dotenv import load_dotenv
# load_dotenv()
# 
# CHATGPT_API_KEY = os.getenv('CHATGPT_API_KEY')
# INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME')
# INSTAGRAM_PASSWORD = os.getenv('INSTAGRAM_PASSWORD')
# 
# # Obtener datos curiosos
# fun_facts = get_fun_facts(CHATGPT_API_KEY, n=10)
# 
# # Generar video
# video_path = "Resources/videos/fun_facts_video.mp4"
# generate_video_with_facts(fun_facts, video_path)
# 
# # Publicar en Instagram
# caption = "10 datos curiosos que no sabías! #funfacts #datoscuriosos"
# post_video_to_instagram(video_path, caption)


import requests

# Configuración
access_token = 'EAAQnFLoLYywBO0D0eCjO0MLhhBy84fHjAOxEycN9K0yCBbSbwetzNerrQIHCLg9Hct0SYVSrZChpE8ZADNtysSM32OTJpJ5Ej4CFirEJrN45mGkscv0dYq0Nvnu620YtzdNccZAaybafLpdofdusoxdJ1CkkWCaZCFqcy0ubTZBqIuV8OioG710SlrG7lBuyceZCef45QXYhRYYyIDxxJn8emUHgZDZD'
user_id = 'me'  # Puedes usar 'me' para obtener la información del usuario actual

# Paso 1: Obtener el ID del Usuario
def get_user_id(access_token):
    url = f'https://graph.facebook.com/v12.0/me?fields=id,name'
    params = {
        'access_token': access_token
    }
    response = requests.get(url, params=params)
    result = response.json()
    print(f'Respuesta del paso 1: {result}')  # Añadido para depuración
    return result.get('id')

# Paso 2: Obtener la página de Facebook vinculada
def get_facebook_page_id(user_id, access_token):
    url = f'https://graph.facebook.com/v12.0/{user_id}/accounts'
    params = {
        'access_token': access_token
    }
    response = requests.get(url, params=params)
    result = response.json()
    print(f'Respuesta del paso 2: {result}')  # Añadido para depuración
    if 'data' in result and len(result['data']) > 0:
        return result['data'][0]['id']
    else:
        return None

# Paso 3: Obtener el Instagram Business Account ID
def get_instagram_account_id(page_id, access_token):
    url = f'https://graph.facebook.com/v12.0/{page_id}?fields=instagram_business_account'
    params = {
        'access_token': access_token
    }
    response = requests.get(url, params=params)
    result = response.json()
    print(f'Respuesta del paso 3: {result}')  # Añadido para depuración
    if 'instagram_business_account' in result:
        return result['instagram_business_account']['id']
    else:
        return None

# Obtener el ID del Usuario
user_id = get_user_id(access_token)
print(f'User ID: {user_id}')

# Obtener la página de Facebook vinculada
page_id = get_facebook_page_id(user_id, access_token)
if page_id:
    # Obtener el Instagram Business Account ID
    instagram_account_id = get_instagram_account_id(page_id, access_token)
    if instagram_account_id:
        print(f'Instagram Account ID: {instagram_account_id}')
    else:
        print('No se encontró una cuenta de Instagram Business vinculada.')
else:
    print('No se encontró una página de Facebook vinculada.')
