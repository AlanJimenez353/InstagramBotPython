import re

def clean_filename(filename):
    return re.sub(r'[\\/*?:"<>|\n]', '', filename).strip()
