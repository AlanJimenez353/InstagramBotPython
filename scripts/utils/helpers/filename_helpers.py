import re

def clean_filename(filename):
    return re.sub(r'[\\/*?:"<>|\n]', '', filename).strip()

def clean_and_validate_keywords(raw_keywords):
    clean_keywords = []
    for keyword in raw_keywords:
        # Limpiar y validar cada palabra clave aquí
        keyword = keyword.strip().replace('.', '').replace('"', '')
        if keyword:
            clean_keywords.append(keyword)
    return clean_keywords
