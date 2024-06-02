
import requests

# Configuración
access_token = ''
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
