from openai import OpenAI
from dotenv import load_dotenv
import os


# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Variables OpenAI
api_key = os.getenv("OPENAI_API_KEY")
print(api_key)
client= OpenAI(api_key=api_key)


#Metodo para traer N cantidad de datos cientificos
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
