import json
import os
from scripts.utils.chatGPT.chatGPT_get_facts import get_facts
from scripts.utils.helpers.environment_helpers import update_env_variable, get_env_variable
from scripts.utils.helpers.filename_helpers import clean_filename
from scripts.utils.helpers.openai_helpers import get_alternate_keyword, get_image_query
from scripts.utils.helpers.pexels_helpers import get_images_from_pexels

def save_image_data(image_data, json_path):
    if os.path.exists(json_path):
        with open(json_path, 'r') as file:
            data = json.load(file)
    else:
        data = {}

    data.update(image_data)
    with open(json_path, 'w') as file:
        json.dump(data, file)

def generate_images_for_facts(openai_api_key, pexels_api_key, image_dir, env_path, fact_id, image_count):
    facts = get_facts(openai_api_key, 3)
    print("Scientific Facts:")
    for fact in facts:
        print(fact)

    keyword_images = {}  # Dictionary to store images for each keyword

    for index, fact in enumerate(facts):
        keywords = get_image_query(fact, num_keywords=2)
        if not keywords:
            print("Skipping fact due to insufficient valid keywords.")
            continue

        for keyword in keywords:
            keyword = clean_filename(keyword)
            print("Processing keyword:", keyword)
            image_filenames, image_count = get_images_from_pexels(keyword, pexels_api_key, image_dir, fact_id, image_count, required_images=3)

            # Check if images were properly retrieved
            if isinstance(image_filenames, list):
                keyword_images[keyword] = [os.path.basename(filename) for filename in image_filenames]
                if len(image_filenames) < 3:
                    # Not enough images, find alternatives
                    alternate_keyword = get_alternate_keyword(keyword, set(keyword_images.keys()))
                    if alternate_keyword:
                        alt_images, image_count = get_images_from_pexels(alternate_keyword, pexels_api_key, image_dir, fact_id, image_count, required_images=3-len(image_filenames))
                        keyword_images[alternate_keyword] = [os.path.basename(filename) for filename in alt_images]
                        image_filenames.extend(alt_images)  # Append new images to the original list

            else:
                print(f"Error retrieving images for keyword '{keyword}'.")
                continue  # Skip to next keyword if images are not correctly retrieved

            if len(image_filenames) >= 3:
                print(f"Successfully downloaded images for keyword '{keyword}':", image_filenames)
            else:
                print(f"Failed to download enough images for keyword '{keyword}'.")
        
        fact_id += 1  # Increment fact_id after processing each fact
        update_env_variable(env_path, 'FACT_ID', fact_id)
        update_env_variable(env_path, 'IMAGE_COUNTER', image_count)

        print(f"FACT_ID is now {fact_id}")
        print(f"IMAGE_COUNTER is now {image_count}")

    return keyword_images  # Optionally return the dictionary of downloaded images for each keyword
