import os
from scripts.utils.helpers.environment_helpers import load_env, get_env_variable, update_env_variable
from scripts.utils.helpers.openai_helpers import get_alternate_keyword, get_facts, get_image_query
from scripts.utils.helpers.pexels_helpers import get_images_from_pexels
from scripts.utils.helpers.filename_helpers import clean_filename

# Carga las variables de entorno desde el archivo .env
env_path = 'C:\\Users\\Alan\\Documents\\CodeProjects\\Project Instagram\\.env'
load_env(env_path)

# Variables OpenAI y Pexels
openai_api_key = get_env_variable("OPENAI_API_KEY")
pexels_api_key = get_env_variable("PEXELS_API_KEY")


# Directorio para guardar imágenes, obtenido desde la variable de entorno
image_dir = get_env_variable("IMAGE_SAVE_PATH")
os.makedirs(image_dir, exist_ok=True)

# Manejo de la variable de entorno para el contador de imágenes
image_count = int(get_env_variable("IMAGE_COUNTER", 0))
fact_id = int(get_env_variable("FACT_ID", 0))


# Obtener datos científicos
facts = get_facts(openai_api_key, 3)
print("Scientific Facts:")
for fact in facts:
    print(fact)

for fact in facts:
    keywords = get_image_query(fact, num_keywords=2)
    if not keywords:
        print("Skipping fact due to insufficient valid keywords.")
        continue  # Saltar este hecho si no se encontraron suficientes palabras clave válidas

    total_images_downloaded = 0
    previous_alternates = set()
    for keyword in keywords:
        keyword = clean_filename(keyword) 
        print("Processing keyword:", keyword)  # Para debug
        
        downloaded, image_count = get_images_from_pexels(keyword, pexels_api_key, image_dir, fact_id, image_count, required_images=3)
        total_images_downloaded += downloaded

        while downloaded < 3 and total_images_downloaded < 6:
            alternate_keyword = get_alternate_keyword(keyword, previous_alternates)
            if alternate_keyword:
                previous_alternates.add(alternate_keyword)
                alternate_keyword = clean_filename(alternate_keyword)
                print(f"Trying alternate keyword: {alternate_keyword}")
                downloaded, image_count = get_images_from_pexels(alternate_keyword, pexels_api_key, image_dir, fact_id, image_count, required_images=3-downloaded)
                total_images_downloaded += downloaded
            else:
                break

        if total_images_downloaded >= 6:
            break

    if total_images_downloaded < 6:
        print(f"Warning: Could not download 6 images for fact_id {fact_id}. Downloaded {total_images_downloaded} images.")
        
    fact_id += 1
    update_env_variable(env_path, 'FACT_ID', fact_id)
    update_env_variable(env_path, 'IMAGE_COUNTER', image_count)
    print(f"FACT_ID is now {fact_id}")
    print(f"IMAGE_COUNTER is now {image_count}")
