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
        
        # Находим блоки с фильмами
        films = soup.find_all('li', class_='ipc-metadata-list-summary-item')
        if not films:
            films = soup.find_all('td', class_='titleColumn')
        
        data = []
        for i, film in enumerate(films[:250], 1):
            try:
                if film.name == 'td' and 'titleColumn' in film.get('class', []):
                    title_link = film.find('a')
                    title = title_link.text.strip()
                    year_text = film.find('span', class_='secondaryInfo')
                    year = year_text.text.strip('()') if year_text else ""
                    rating_cell = film.find_next_sibling('td', class_='ratingColumn')
                    rating = rating_cell.text.strip() if rating_cell else "N/A"
                else:
                    title_elem = film.find('h3', class_='ipc-title__text')
                    if not title_elem:
                        title_elem = film.find('a', class_='ipc-title-link-wrapper')
                    title = title_elem.text.strip() if title_elem else "Unknown"
                    if '.' in title:
                        title = title.split('.', 1)[1].strip()
                    year_elem = film.find('span', class_='cli-title-metadata-item')
                    year = year_elem.text.strip() if year_elem else ""
                    rating_elem = film.find('span', class_='ipc-rating-star')
                    rating = rating_elem.text.split()[0] if rating_elem else "N/A"
                
                data.append({'rank': i, 'title': title, 'year': year, 'rating': rating})
                print(f"  {i}. {title} ({year}) — {rating}")
            except Exception as e:
                print(f"  Ошибка при обработке фильма {i}: {e}")
                continue
        
        print(f"\nВсего собрано фильмов: {len(data)}")
        return data
    except Exception as e:
        print(f"Ошибка: {e}")
        return []

def save_to_csv(data: List[Dict[str, str]], filename: str) -> None:
    if data:
        pd.DataFrame(data).to_csv(filename, index=False, encoding='utf-8')
        print(f"Сохранено в {filename} ({len(data)} записей)")

def save_to_excel(data: List[Dict[str, str]], filename: str) -> None:
    if data:
        pd.DataFrame(data).to_excel(filename, index=False)
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
