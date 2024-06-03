import os
from scripts.utils.chatGPT.chatGPT_utils import get_facts
#from scripts.utils.videoAndImageGeneration.video_utils import generate_video_with_facts
#from scripts.utils.Instagram.instagram_utils import post_video_to_instagram

# Cargar variables de entorno
from dotenv import load_dotenv
load_dotenv()

CHATGPT_API_KEY = os.getenv('CHATGPT_API_KEY')
#INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME')
#INSTAGRAM_PASSWORD = os.getenv('INSTAGRAM_PASSWORD')

# Obtener datos curiosos
fun_facts = get_facts(n=3)

print("Datos curiosos de avances científicos:")
for i, fact in enumerate(fun_facts, 1):
    print(f"{fact}")














# # Generar video
# video_path = "Resources/videos/fun_facts_video.mp4"
# generate_video_with_facts(fun_facts, video_path)
# 
# # Publicar en Instagram
# caption = "10 datos curiosos que no sabías! #funfacts #datoscuriosos"
# post_video_to_instagram(video_path, caption)
