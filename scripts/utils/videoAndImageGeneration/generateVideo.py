import json
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
from gtts import gTTS
import os

def load_keywords():
    # Establece la ruta al archivo keywords.json en el mismo directorio que este script
    keywords_file = os.path.join(os.path.dirname(__file__), 'keywords.json')

    # Verifica si el archivo existe
    if not os.path.exists(keywords_file):
        # Si el archivo no existe, crea uno nuevo con contenido inicial
        initial_data = {'facts': []}  # Asume una estructura de datos inicial
        with open(keywords_file, 'w') as file:
            json.dump(initial_data, file)
        return initial_data['facts']
    else:
        # Si el archivo existe, simplemente carga su contenido
        with open(keywords_file, 'r') as file:
            data = json.load(file)
        return data['facts']


def create_video_with_facts(image_dir, video_dir):
    facts = load_keywords()
    clips = []

    for fact in facts:
        fact_id = fact['id']
        for keyword_index, keyword in enumerate(fact['keywords']):
            for image_index in range(3):  # Suponiendo tres imágenes por keyword
                img_path = os.path.join(image_dir, f"fact{fact_id}_{keyword}_image_{image_index}.jpg")
                if not os.path.exists(img_path):
                    print(f"Imagen no encontrada: {img_path}")
                    continue

                # Texto a voz
                tts = gTTS(f"Fact {fact_id}, Keyword {keyword}, Image {image_index}", lang='es')
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
        final_video_path = os.path.join(video_dir, "final_video.mp4")
        final_clip.write_videofile(final_video_path, fps=24)
    else:
        print("No se encontraron imágenes para crear el video.")

# Rutas de los directorios donde se guardan las imágenes y videos
image_dir = "C:\\Users\\Alan\\Documents\\CodeProjects\\Project Instagram\\Resources\\Images"
video_dir = "C:\\Users\\Alan\\Documents\\CodeProjects\\Project Instagram\\Resources\\Videos"

