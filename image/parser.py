import os
import requests

API_KEY = "47630560-aa1c509935ac71b6d88f53537"
BASE_URL = "https://pixabay.com/api/"
QUERY = "flamingo"
IMAGE_TYPE = "photo"
MIN_WIDTH = 800
MIN_HEIGHT = 600
TARGET_FOLDER = "flamingo_images"
PER_PAGE = 200
TOTAL_IMAGES = 300

if not os.path.exists(TARGET_FOLDER):
    os.makedirs(TARGET_FOLDER)

def download_image(url, filename):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(filename, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
    except Exception as e:
        print(f"Ошибка при загрузке {url}: {e}")

images_downloaded = 0
page = 1

while images_downloaded < TOTAL_IMAGES:
    params = {
        "key": API_KEY,
        "q": QUERY,
        "image_type": IMAGE_TYPE,
        "min_width": MIN_WIDTH,
        "min_height": MIN_HEIGHT,
        "per_page": PER_PAGE,
        "page": page,
        "pretty": "true",
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        hits = data.get("hits", [])

        if not hits:
            print("Больше изображений не найдено.")
            break

        for hit in hits:
            if images_downloaded >= TOTAL_IMAGES:
                break

            image_url = hit.get("largeImageURL")
            if image_url:
                image_id = hit.get("id")
                filename = os.path.join(TARGET_FOLDER, f"flamingo_{image_id}.jpg")
                download_image(image_url, filename)
                images_downloaded += 1
                print(f"Скачано изображение {images_downloaded}: {filename}")

    else:
        print(f"Ошибка API: {response.status_code}")
        break

    page += 1

print(f"Всего скачано изображений: {images_downloaded}")
