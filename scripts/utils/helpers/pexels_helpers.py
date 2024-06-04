
import requests
import os
import time

def get_images_from_pexels(query, api_key, image_dir, fact_id, image_count, required_images=3, retries=3):
    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": api_key}
    params = {"query": query, "per_page": required_images}
    attempt = 0
    total_images_downloaded = 0
    
    while attempt < retries and total_images_downloaded < required_images:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            images = response.json().get('photos', [])
            if images:
                for i, image in enumerate(images):
                    if total_images_downloaded >= required_images:
                        break
                    img_url = image['src']['original']
                    img_data = requests.get(img_url).content
                    filename = f"fact{fact_id}_{query}_image_{image_count}.jpg"
                    image_path = os.path.join(image_dir, filename)
                    with open(image_path, 'wb') as handler:
                        handler.write(img_data)
                    print(f"Descargada {img_url} como {filename}")
                    image_count += 1
                    total_images_downloaded += 1
                return total_images_downloaded, image_count  # Return if successful
            else:
                print(f"No images found for query '{query}'.")
        else:
            print(f"Failed to fetch images from Pexels. Status code: {response.status_code}")
        
        attempt += 1
        time.sleep(2)  # Wait before retrying

    print(f"Failed to download required images for query '{query}' after {retries} attempts.")
    return total_images_downloaded, image_count
