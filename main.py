import os
from scripts.utils.helpers.environment_helpers import load_env, get_env_variable, update_env_variable
from scripts.utils.helpers.ImageGeneration.generate_images_for_facts import generate_images_for_facts
from scripts.utils.videoAndImageGeneration.generateVideo import create_video_with_facts
from scripts.utils.chatGPT.chatGPT_get_facts import get_facts 

# Cargar variables de entorno
env_path = 'C:\\Users\\Alan\\Documents\\CodeProjects\\Project Instagram\\.env'
load_env(env_path)

# Obtener claves API y directorios de trabajo
openai_api_key = get_env_variable("OPENAI_API_KEY")
pexels_api_key = get_env_variable("PEXELS_API_KEY")
image_dir = get_env_variable("IMAGE_SAVE_PATH")
video_dir = get_env_variable("VIDEO_SAVE_PATH")

# Crear directorios si no existen
os.makedirs(image_dir, exist_ok=True)
os.makedirs(video_dir, exist_ok=True)

# Manejo de la variable de entorno para el contador de imágenes y el fact_id
image_count = int(get_env_variable("IMAGE_COUNTER", 0))
fact_id = int(get_env_variable("FACT_ID", 0))

# Obtener datos científicos
facts = get_facts(openai_api_key,n=3)
print("Scientific Facts:")
for fact in facts:
    print(fact)

# Llamar a la función para generar imágenes
generate_images_for_facts(openai_api_key, pexels_api_key, image_dir, env_path, fact_id, image_count)

# Crear el video con los datos científicos obtenidos
create_video_with_facts(facts, image_dir, video_dir)

# Actualizar y guardar el estado
update_env_variable(env_path, 'FACT_ID', fact_id + 1)
update_env_variable(env_path, 'IMAGE_COUNTER', image_count)
print(f"FACT_ID is now {fact_id + 1}")
print(f"IMAGE_COUNTER is now {image_count}")
