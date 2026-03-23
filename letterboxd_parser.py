import requests
from bs4 import BeautifulSoup
import pandas as pd
from typing import List, Dict

def parse_imdb_top250() -> List[Dict[str, str]]:
    """Парсит топ-250 фильмов IMDb. Данные получаются напрямую с сайта."""
    url = "https://www.imdb.com/chart/top/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    print("Парсинг IMDb Top 250...")
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Находим все строки таблицы с фильмами
        films = soup.find_all('tr')
        
        data = []
        for film in films:
            try:
                # Ищем ячейку с названием
                title_cell = film.find('td', class_='titleColumn')
                if not title_cell:
                    continue
                
                # Название и ссылка
                a_tag = title_cell.find('a')
                title = a_tag.text.strip() if a_tag else "Unknown"
                
                # Год
                year_span = title_cell.find('span', class_='secondaryInfo')
                year = year_span.text.strip('()') if year_span else ""
                
                # Рейтинг
                rating_cell = film.find('td', class_='ratingColumn')
                rating = rating_cell.text.strip() if rating_cell else "N/A"
                
                data.append({
                    'title': title,
                    'year': year,
                    'rating': rating
                })
                
            except Exception:
                continue
        
        # Добавляем rank
        for i, item in enumerate(data, 1):
            item['rank'] = i
        
        print(f"  Найдено фильмов: {len(data)}")
        for i, f in enumerate(data[:10], 1):
            print(f"  {i}. {f['title']} ({f['year']}) — {f['rating']}")
        
        return data
        
    except Exception as e:
        print(f"Ошибка: {e}")
        return []

def save_to_csv(data: List[Dict[str, str]], filename: str) -> None:
    if data:
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"Сохранено в {filename} ({len(data)} записей)")

def save_to_excel(data: List[Dict[str, str]], filename: str) -> None:
    if data:
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)
        print(f"Сохранено в {filename}")

def print_stats(data: List[Dict[str, str]]) -> None:
    if not data:
        return
    df = pd.DataFrame(data)
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    print("\n" + "="*50)
    print("СТАТИСТИКА")
    print("="*50)
    print(f"Всего фильмов: {len(data)}")
    print(f"Средний рейтинг: {df['rating'].mean():.2f}/10")
    print(f"Максимальный: {df['rating'].max()}/10")
    print(f"Минимальный: {df['rating'].min()}/10")
    print("\nПервые 10 записей:")
    for i, r in enumerate(data[:10]):
        print(f"{i+1}. {r['title']} ({r['year']}) — {r['rating']}/10")

if __name__ == "__main__":
    print("="*50)
    print("ПАРСЕР IMDb TOP 250")
    print("="*50)
    films = parse_imdb_top250()
    if films:
        save_to_csv(films, "imdb_top250.csv")
        save_to_excel(films, "imdb_top250.xlsx")
        print_stats(films)
    else:
        print("Не удалось получить данные с IMDb")
