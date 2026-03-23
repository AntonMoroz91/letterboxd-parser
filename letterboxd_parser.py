import pandas as pd
from imdb import Cinemagoer

def get_top_250_movies():
    """Получает топ-250 фильмов через IMDb API."""
    ia = Cinemagoer()
    
    print("Получение топ-250 фильмов IMDb...")
    
    # Получаем топ-250
    top250 = ia.get_top250_movies()
    
    data = []
    for i, movie in enumerate(top250[:100], 1):  # Берём первые 100 для примера
        data.append({
            'rank': i,
            'title': movie['title'],
            'year': movie.get('year', ''),
            'rating': movie.get('rating', 'N/A')
        })
        print(f"  {i}. {movie['title']} ({movie.get('year', '')}) — {movie.get('rating', 'N/A')}")
    
    print(f"\nВсего собрано фильмов: {len(data)}")
    return data

def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding='utf-8')
    print(f"Сохранено в {filename} ({len(data)} записей)")

def save_to_excel(data, filename):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    print(f"Сохранено в {filename}")

if __name__ == "__main__":
    print("="*50)
    print("ПАРСЕР IMDb TOP 250")
    print("="*50)
    
    movies = get_top_250_movies()
    
    if movies:
        save_to_csv(movies, "imdb_top250.csv")
        save_to_excel(movies, "imdb_top250.xlsx")
        
        df = pd.DataFrame(movies)
        print("\n" + "="*50)
        print("СТАТИСТИКА")
        print("="*50)
        print(f"Всего фильмов: {len(movies)}")
        
        ratings = df[df['rating'] != 'N/A']['rating']
        if len(ratings) > 0:
            print(f"Средний рейтинг: {ratings.mean():.2f}/10")
            print(f"Максимальный: {ratings.max()}/10")
            print(f"Минимальный: {ratings.min()}/10")
        
        print("\nПервые 10 записей:")
        for i, r in enumerate(movies[:10]):
            print(f"{i+1}. {r['title']} ({r['year']}) — {r['rating']}/10")
    else:
        print("Не удалось получить данные")
