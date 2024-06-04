import os
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Lista de todas las variables de entorno utilizadas en tu aplicación
env_vars = [
    "OPENAI_API_KEY", "PEXELS_API_KEY", "INSTAGRAM_USERNAME",
    "INSTAGRAM_PASSWORD", "ACCESS_TOKEN", "USER_ID",
    "VIDEO_SAVE_PATH", "IMAGE_SAVE_PATH", "IMAGE_COUNTER", "FACT_ID"
]

# Imprimir los valores de las variables para verificar su correcta carga
for var in env_vars:
    value = os.getenv(var)
    if value:
        print(f"{var}: {value}")
    else:
        print(f"{var} is not set or loaded incorrectly.")
