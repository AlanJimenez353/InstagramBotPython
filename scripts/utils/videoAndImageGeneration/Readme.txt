# Video and Image Generation Script

Este script genera videos utilizando imágenes y datos curiosos obtenidos de una API. Cada video se crea a partir de imágenes previamente generadas y almacenadas, y se sincroniza con audio generado a partir de texto utilizando `gTTS`. El script gestiona el estado mediante un archivo JSON para asegurar que los videos se generen de manera consistente cada día.


## Dependencias

- `moviepy`
- `Pillow`
- `gTTS`
- `dotenv`
- `openai`

Instala las dependencias con:

```sh
pip install moviepy Pillow gTTS python-dotenv openai


## Archivos Importantes

-.env

    OPENAI_API_KEY=tu_api_key_de_openai
    VIDEO_SAVE_PATH=C: Ruta donde se guardaran las imagenes 
    IMAGE_SAVE_PATH=C: Ruta donde se guardaran los videos

-generateVideo.py

    Este es el script principal que genera los videos. Contiene las siguientes partes importantes:

    - Carga de Variables de Entorno: Carga las variables de entorno desde el archivo .env.
    - Funciones de Estado: load_state y save_state manejan el estado utilizando un archivo JSON.
    - Función create_video_with_facts: Crea el video utilizando las imágenes y el audio generados.
    - Obtención de Datos Curiosos: Utiliza la función get_facts para obtener los datos curiosos.

-video_generation_state.json

    Este archivo JSON guarda el estado actual, incluyendo el último fact_id utilizado y las últimas keywords utilizadas.
    Es importante ya que al generar el video debe utilizar las keywords que contengan en su nombre el fact_id asociado a ellas 


## Ejecución del Script

    Para ejecutar el script, simplemente ejecuta generateVideo.py. El script:

    - Cargará el estado actual desde video_generation_state.json.
    - Obtendrá nuevos datos curiosos utilizando get_facts.
    - Creará un video utilizando las imágenes y el audio generados.   
    - Actualizará el estado en video_generation_state.json.
