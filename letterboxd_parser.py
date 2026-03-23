import pandas as pd
from imdb import Cinemagoer

def get_top_250_movies():
    """Получает топ-250 фильмов через IMDb API."""
    ia = Cinemagoer()
    
    print("Получение топ-250 фильмов IMDb...")
    
    try:
        top250 = ia.get_top250_movies()
        
        data = []
        for i, movie in enumerate(top250[:100], 1):
            data.append({
                'rank': i,
                'title': movie['title'],
                'year': movie.get('year', ''),
                'rating': movie.get('rating', 'N/A')
            })
            print(f"  {i}. {movie['title']} ({movie.get('year', '')}) — {movie.get('rating', 'N/A')}")
        
        print(f"\nВсего собрано фильмов: {len(data)}")
        return data
        
    except Exception as e:
        print(f"Ошибка: {e}")
        return []

def save_results(data, login):
    if not data:
        print("Нет данных")
        return
    
    df = pd.DataFrame(data)
    df.to_csv(f"{login}_rates.csv", index=False, encoding='utf-8')
    df.to_excel(f"{login}_rates.xlsx", index=False)
    print(f"Сохранено в {login}_rates.csv и {login}_rates.xlsx ({len(data)} записей)")
    
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    print("\n" + "="*50)
    print("СТАТИСТИКА")
    print("="*50)
    print(f"Всего фильмов: {len(data)}")
    
    ratings = df[df['rating'].notna()]['rating']
    if len(ratings) > 0:
        print(f"Средний рейтинг: {ratings.mean():.2f}/10")
        print(f"Максимальный: {ratings.max()}/10")
        print(f"Минимальный: {ratings.min()}/10")
    
    print("\nПервые 10 записей:")
    for i, r in enumerate(data[:10]):
        print(f"{i+1}. {r['title']} ({r['year']}) — {r['rating']}/10")

if __name__ == "__main__":
    print("="*50)
    print("ПАРСЕР IMDb TOP 250")
    print("="*50)
    
    movies = get_top_250_movies()
    
    if movies:
        save_results(movies, "imdb_top250")
    else:
        print("Не удалось получить данные")
