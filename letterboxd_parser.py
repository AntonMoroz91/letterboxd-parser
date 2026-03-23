import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import sys
from typing import List, Dict

def collect_user_rates(user_login: str, delay: float = 2.0) -> List[Dict[str, str]]:
    """
    Парсит все страницы дневника пользователя Letterboxd.
    Извлекает название фильма, год выпуска и оценку.
    """
    page_num = 1
    data = []
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    print(f"Парсинг пользователя: {user_login}")
    
    while True:
        url = f'https://letterboxd.com/{user_login}/films/diary/page/{page_num}/'
        print(f"Страница {page_num}...")
        
        try:
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 403:
                print(f"Блокировка, жду 10 секунд...")
                time.sleep(10)
                continue
                
            if response.status_code != 200:
                print(f"Ошибка {response.status_code}")
                break
            
            soup = BeautifulSoup(response.text, 'lxml')
            rows = soup.find_all('tr', class_='diary-entry-row')
            
            if not rows:
                print(f"Достигнут конец (страница {page_num-1})")
                break
            
            page_films = 0
            for row in rows:
                if 'not-rated' in row.get('class', []):
                    continue
                
                td_film = row.find('td', class_='td-film-details')
                if not td_film:
                    continue
                film_name = td_film.find('a').text.strip()
                
                td_year = row.find('td', class_='td-released')
                release_year = td_year.text.strip() if td_year else ''
                
                td_rating = row.find('td', class_='td-rating')
                if not td_rating:
                    continue
                rating_span = td_rating.find('span', class_='rating')
                if not rating_span:
                    continue
                classes = rating_span.get('class', [])
                if len(classes) < 2:
                    continue
                rating = classes[1].split('-')[1]
                
                data.append({
                    'film_name': film_name,
                    'release_year': release_year,
                    'rating': rating
                })
                page_films += 1
            
            print(f"Найдено фильмов с оценками: {page_films}")
            page_num += 1
            time.sleep(delay)
            
        except Exception as e:
            print(f"Ошибка: {e}")
            break
    
    print(f"Всего собрано оценок: {len(data)}")
    return data

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
    df['rating'] = pd.to_numeric(df['rating'])
    
    print("\n" + "="*50)
    print("СТАТИСТИКА")
    print("="*50)
    print(f"Всего фильмов: {len(data)}")
    print(f"Средняя оценка: {df['rating'].mean():.2f}/10")
    print(f"Максимальная: {df['rating'].max()}/10")
    print(f"Минимальная: {df['rating'].min()}/10")
    
    print("\nПервые 10 записей:")
    for i, r in enumerate(data[:10]):
        print(f"{i+1}. {r['film_name']} ({r['release_year']}) — {r['rating']}/10")

if __name__ == "__main__":
    print("="*50)
    print("ПАРСЕР ОЦЕНОК LETTERBOXD")
    print("="*50)
    
    if len(sys.argv) > 1:
        USER_LOGIN = sys.argv[1]
    else:
        USER_LOGIN = "rfeldman9"
    
    ratings = collect_user_rates(USER_LOGIN)
    
    if ratings:
        save_to_csv(ratings, f"{USER_LOGIN}_rates.csv")
        save_to_excel(ratings, f"{USER_LOGIN}_rates.xlsx")
        print_stats(ratings)
    else:
        print(f"\nНе удалось получить данные для {USER_LOGIN}")
        print("Возможные причины:")
        print("  • Сайт временно блокирует запросы")
        print("  • У пользователя нет публичных оценок")
        print("\nПопробуйте другого пользователя:")
        print("   python letterboxd_parser.py dave")
