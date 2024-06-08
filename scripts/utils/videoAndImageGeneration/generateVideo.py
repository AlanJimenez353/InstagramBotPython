import json
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS
import os
from dotenv import load_dotenv
from ..chatGPT.chatGPT_get_facts import get_facts  # Importar el método get_facts

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Directorio para guardar el video, obtenido desde la variable de entorno
video_dir = os.getenv('VIDEO_SAVE_PATH')
image_dir = os.getenv('IMAGE_SAVE_PATH')
state_file = os.path.join(os.path.dirname(__file__), 'video_generation_state.json')

if not video_dir:
    raise Exception("Variable de entorno VIDEO_SAVE_PATH no definida")
if not image_dir:
    raise Exception("Variable de entorno IMAGE_SAVE_PATH no definida")

os.makedirs(video_dir, exist_ok=True)

def load_state():
    if os.path.exists(state_file):
        with open(state_file, 'r') as file:
            return json.load(file)
    else:
        return {"last_fact_id": 0, "last_used_keywords": {}}

def save_state(state):
    with open(state_file, 'w') as file:
        json.dump(state, file)

def create_video_with_facts(facts, image_dir, last_fact_id):
    clips = []
    for fact_id, fact in enumerate(facts, start=last_fact_id):
        for keyword_index in range(2):  # Hay dos keywords por fact
            for image_index in range(3):  # Hay tres imágenes por keyword
                img_path = os.path.join(image_dir, f"fact{fact_id}_keyword{keyword_index}_image_{image_index}.jpg")
                if not os.path.exists(img_path):
                    print(f"Imagen no encontrada: {img_path}")
                    continue

                # Texto a voz
                tts = gTTS(fact, lang='es')
                tts_path = os.path.join(video_dir, f"speech{fact_id}_{keyword_index}_{image_index}.mp3")
                tts.save(tts_path)
                
                # Crear clip de video con audio
                audio_clip = AudioFileClip(tts_path)
                video_clip = ImageClip(img_path).set_duration(audio_clip.duration)
                video_clip = video_clip.set_audio(audio_clip)
                clips.append(video_clip)

    # Concatenar todos los clips en un solo video
    if clips:
        final_clip = concatenate_videoclips(clips)
        final_video_path = os.path.join(video_dir, f"final_video_{fact_id}.mp4")
        final_clip.write_videofile(final_video_path, fps=24)
    else:
        print("No se encontraron imágenes para crear el video.")
    return fact_id

# Cargar el estado
state = load_state()

# Obtener los datos científicos
facts = get_facts(n=3)
print("Scientific Facts:")
for fact in facts:
    print(fact)

# Crear el video con los datos científicos obtenidos
last_fact_id = state['last_fact_id']
new_fact_id = create_video_with_facts(facts, image_dir, last_fact_id)

# Actualizar y guardar el estado
state['last_fact_id'] = new_fact_id + 1
save_state(state)
