import os
from dotenv import load_dotenv, set_key

def load_env(env_path):
    load_dotenv(env_path)

def get_env_variable(key, default=None):
    return os.getenv(key, default)

def update_env_variable(env_path, key, value):
    os.environ[key] = str(value)
    set_key(env_path, key, str(value))
