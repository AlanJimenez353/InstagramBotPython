from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Leer la variable de entorno
video_dir = os.getenv('VIDEO_SAVE_PATH')
if not video_dir:
    raise Exception("Variable de entorno VIDEO_SAVE_PATH no definida")

os.makedirs(video_dir, exist_ok=True)

# Datos curiosos
fun_facts = [
    "Desarrollo de vacunas de ARN mensajero para combatir enfermedades como la COVID-19.",
    "Avances en la medicina regenerativa con el uso de células madre.",
    "Desarrollo de la tecnología CRISPR-Cas9 para editar el ADN."
]

# Generar imágenes y audio
clips = []
for i, fact in enumerate(fun_facts):
    # Crear imagen con texto
    img = Image.new('RGB', (1280, 720), color = (73, 109, 137))
    d = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    d.text((10,10), fact, fill=(255,255,255), font=font)
    img_path = os.path.join(video_dir, f"image{i}.png")
    img.save(img_path)
    
    # Texto a voz
    tts = gTTS(fact, lang='es')
    tts_path = os.path.join(video_dir, f"speech{i}.mp3")
    tts.save(tts_path)
    
    # Crear clip de video con audio
    audio_clip = AudioFileClip(tts_path)
    video_clip = ImageClip(img_path).set_duration(audio_clip.duration)
    video_clip = video_clip.set_audio(audio_clip)
    clips.append(video_clip)

# Concatenar todos los clips en un solo video
final_clip = concatenate_videoclips(clips)
final_video_path = os.path.join(video_dir, "final_video.mp4")
final_clip.write_videofile(final_video_path, fps=24)
