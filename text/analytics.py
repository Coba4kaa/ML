import pandas as pd
import matplotlib.pyplot as plt
from nltk.corpus import stopwords

data = pd.read_csv('cleaned_reviews.csv')
data = data[data['type'] != "Нейтральный"]

def word_count(text):
    return len(text.split())

data['word_count'] = data['review'].apply(word_count)

data = data[(data['word_count'] >= 50) & (data['word_count'] <= 500)]

def remove_stopwords(text, stop_words):
    words = text.split()
    filtered_words = [word for word in words if word.lower() not in stop_words]
    return ' '.join(filtered_words)

stop_words = set(stopwords.words('russian'))
data['review'] = data['review'].apply(lambda x: remove_stopwords(x, stop_words))

data = data[(data['word_count'] >= 10) & (data['word_count'] <= 400)]

data['word_count'] = data['review'].apply(word_count)

num_reviews = len(data)
print(f"Общее количество отзывов (после фильтрации): {num_reviews}")

class_counts = data['type'].value_counts()
print("Количество отзывов по классам:")
print(class_counts)

average_words = data['word_count'].mean()
min_words = data['word_count'].min()
max_words = data['word_count'].max()

print(f"Среднее количество слов в отзыве: {average_words:.2f}")
print(f"Минимальное количество слов в отзыве: {min_words}")
print(f"Максимальное количество слов в отзыве: {max_words}")

plt.figure(figsize=(10, 6))
plt.hist(data['word_count'], bins=30, edgecolor='k', alpha=0.7)
plt.title("Распределение количества слов в отзывах")
plt.xlabel("Количество слов")
plt.ylabel("Количество отзывов")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

def word_lengths(text):
    return [len(word) for word in text.split()]

all_word_lengths = [length for review in data['review'] for length in word_lengths(review)]

all_words = ' '.join(data['review']).split()
unique_words = set(all_words)

print(f"Общее количество уникальных слов: {len(unique_words)}")
