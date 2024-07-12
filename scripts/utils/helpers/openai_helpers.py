import re
from openai import OpenAI
import os
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
env_path = 'C:\\Users\\Alan\\Documents\\CodeProjects\\Project Instagram\\.env'
load_dotenv(env_path)

openai_api_key = os.getenv("OPENAI_API_KEY")
client= OpenAI(api_key=openai_api_key)


#Esta funcion genera 2 keywords en base a el fact que recibe por parametro para luego enviarlo a la api de pixels y obtener imagenes relacionadas a el fact 
def get_image_query(fact, num_keywords=2):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are an assistant that generates exactly {num_keywords} distinct and concise single-word keywords for image searches based on scientific facts."},
            {"role": "user", "content": f"Provide {num_keywords} distinct, single-word keywords for an image search that reflects this scientific fact: '{fact}'"}
        ]
    )

    if completion.choices and hasattr(completion.choices[0].message, 'content'):
        raw_keywords = completion.choices[0].message.content.strip().split('\n')
        print("Raw keywords:", raw_keywords)  # Para debug

        keywords = []
        for line in raw_keywords:
            # Eliminar prefijos numéricos y palabras irrelevantes
            words = re.split('[,|]', line.replace("1.", "").replace("2.", "").replace("Keywords:", "").replace('"', ''))
            keywords.extend([word.strip() for word in words if word.strip() and not word.lower() in ["keywords", "keyword"]])
        
        print("Processed keywords:", keywords)  # Para debug

        if len(keywords) < num_keywords:
            print("Warning: Not enough valid keywords found. Skipping fact.")
            return None  # Indicar que no se encontraron suficientes palabras clave válidas
        
        return keywords[:num_keywords]
    else:
        print("Warning: No valid content found in API response. Skipping fact.")
        return None



#Esta funcion obtiene 3 datos cientificos en una lista enumerada
def get_facts(api_key, n=3):
    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert in nature."},
            {"role": "user", "content": f"Give me {n} interesting facts about nature."}
        ]
    )

    content = completion.choices[0].message.content if hasattr(completion.choices[0].message, 'content') else "No content available"
    facts = [line.strip() for line in content.split('\n') if line.strip()]
    return facts


#Este metodo se utiliza en get_images_from_pexels en el caso de que alguna de las keywords no tenga resultados al llamar a la API 
# De esta forma el script nunca fallara y siempre se generaran la cantidad de imagenes necesarias
def get_alternate_keyword(keyword, previous_alternates=set(), max_attempts=5):
    if max_attempts <= 0:
        print("Maximum attempts reached for finding alternate keywords.")
        return None
    
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant that generates alternative single-word keywords."},
            {"role": "user", "content": f"Provide an alternative single-word keyword for: '{keyword}'"}
        ]
    )
    
    if completion.choices and hasattr(completion.choices[0].message, 'content'):
        alternate_keyword = completion.choices[0].message.content.strip()
        if alternate_keyword in previous_alternates:
            print(f"Alternate keyword '{alternate_keyword}' is a duplicate. Trying again.")
            return get_alternate_keyword(keyword, previous_alternates, max_attempts - 1)
        else:
            previous_alternates.add(alternate_keyword)
            print("Alternate keyword:", alternate_keyword)  # Para debug
            return alternate_keyword
    else:
        print("Warning: No valid content found for alternate keyword.")
        return None
