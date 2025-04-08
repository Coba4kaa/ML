import requests
import csv

# Базовый URL для API
url = "https://api.kinopoisk.dev/v1.4/review"
headers = {
    "accept": "application/json",
    "X-API-KEY": "463PAFC-HP0MYV7-H7E1YQE-VPJ80WW"
}

# Открываем файл для записи данных
with open('reviews.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=[
        "id", "movieId", "title", "type", "review", "date", "author",
        "userRating", "authorId", "reviewLikes", "reviewDislikes",
        "createdAt", "updatedAt"
    ])
    writer.writeheader()  # Записать заголовки в файл

    # Цикл для запросов к нескольким страницам
    for page in range(1, 101):  # Для примера от 1 до 15 страницы
        params = {
            "page": page,
            "limit": 250
        }

        # Отправка запроса
        response = requests.get(url, headers=headers, params=params)

        # Проверка успешности запроса
        if response.status_code == 200:
            data = response.json()  # Ответ от API в формате JSON

            # Для каждого отзыва на текущей странице
            for review in data.get('docs', []):
                writer.writerow({
                    "id": review.get("id"),
                    "movieId": review.get("movieId"),
                    "title": review.get("title"),
                    "type": review.get("type"),
                    "review": review.get("review"),
                    "date": review.get("date"),
                    "author": review.get("author"),
                    "userRating": review.get("userRating"),
                    "authorId": review.get("authorId"),
                    "reviewLikes": review.get("reviewLikes"),
                    "reviewDislikes": review.get("reviewDislikes"),
                    "createdAt": review.get("createdAt"),
                    "updatedAt": review.get("updatedAt")
                })
            print(f"Данные с страницы {page} успешно сохранены.")
        else:
            print(f"Ошибка запроса на страницу {page}: {response.status_code}")

print("Все данные успешно сохранены в файл reviews.csv.")
