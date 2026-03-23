import pandas as pd
from imdb import Cinemagoer

ia = Cinemagoer()

print("Загрузка топ-250 фильмов IMDb...")

movies = ia.get_top250_movies()

data = []
for i, m in enumerate(movies[:50], 1):
    data.append({
        'rank': i,
        'title': m['title'],
        'year': m.get('year', ''),
        'rating': m.get('rating', '')
    })
    print(f"{i}. {m['title']} ({m.get('year', '')}) — {m.get('rating', '')}")

df = pd.DataFrame(data)
df.to_csv('imdb_top250.csv', index=False, encoding='utf-8')
df.to_excel('imdb_top250.xlsx', index=False)

print(f"\nСохранено {len(data)} фильмов в imdb_top250.csv и imdb_top250.xlsx")
