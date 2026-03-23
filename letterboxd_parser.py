import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from typing import List, Dict

def parse_imdb_top250() -> List[Dict[str, str]]:
    """
    Парсит топ-250 фильмов IMDb.
    Извлекает: место, название, год, рейтинг.
    Данные получаются напрямую с сайта.
    """
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
        rows = soup.find_all('tr', class_='ipc-metadata-list__item')
        
        if not rows:
            # Альтернативный селектор для IMDb
            rows = soup.find_all('li', class_='ipc-metadata-list-summary-item')
        
        if not rows:
            print("Не удалось найти фильмы, пробуем другой селектор...")
            # Простой поиск по ячейкам таблицы
            rows = soup.find_all('td', class_='titleColumn')
        
        data = []
        
        for i, row in enumerate(rows[:50], 1):  # Берем первые 50 фильмов
            try:
                # Извлекаем название и год
                if row.name == 'td' and 'titleColumn' in row.get('class', []):
                    title_link = row.find('a')
                    title = title_link.text.strip() if title_link else "Unknown"
                    year_text = row.find('span', class_='secondaryInfo')
                    year = year_text.text.strip('()') if year_text else ""
                    rating_cell = row.find_next_sibling('td', class_='ratingColumn')
                    rating = rating_cell.text.strip() if rating_cell else "N/A"
                else:
                    # Альтернативный парсинг
                    title_elem = row.find('h3') or row.find('a')
                    title = title_elem.text.strip() if title_elem else "Unknown"
                    
                    # Извлекаем год
                    year_match = re.search(r'\((\d{4})\)', str(row))
                    year = year_match.group(1) if year_match else ""
                    
                    # Извлекаем рейтинг
                    rating_elem = row.find('span', class_='ipc-rating-star')
                    if rating_elem:
                        rating = rating_elem.text.split()[0]
                    else:
                        rating = "N/A"
                
                data.append({
                    'rank': i,
                    'title': title,
                    'year': year,
                    'rating': rating
                })
                print(f"  {i}. {title} ({year}) — {rating}")
                
            except Exception as e:
                print(f"  Ошибка при обработке фильма {i}: {e}")
                continue
        
        print(f"\nВсего собрано фильмов: {len(data)}")
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return []
    except Exception as e:
        print(f"Ошибка парсинга: {e}")
        return []

def parse_user_reviews(username: str) -> List[Dict[str, str]]:
    """
    Парсит рецензии пользователя IMDb (если нужно).
    """
    url = f"https://www.imdb.com/user/{username}/reviews"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    print(f"Парсинг рецензий пользователя: {username}")
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        reviews = soup.find_all('div', class_='lister-item-content')
        
        data = []
        for i, review in enumerate(reviews[:20], 1):
            title_elem = review.find('a', class_='title')
            title = title_elem.text.strip() if title_elem else "Unknown"
            
            rating_elem = review.find('span', class_='rating-other-user-rating')
            rating = rating_elem.text.strip() if rating_elem else "N/A"
            
            data.append({
                'rank': i,
                'film': title,
                'rating': rating
            })
            print(f"  {i}. {title} — {rating}")
        
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
    if 'rating' in df.columns and 'rating' not in ['N/A']:
        df['rating_num'] = pd.to_numeric(df['rating'], errors='coerce')
        ratings = df['rating_num'].dropna()
        if len(ratings) > 0:
            print("\n" + "="*50)
            print("СТАТИСТИКА")
            print("="*50)
            print(f"Всего записей: {len(data)}")
            print(f"Средний рейтинг: {ratings.mean():.2f}/10")
            print(f"Максимальный: {ratings.max()}/10")
            print(f"Минимальный: {ratings.min()}/10")
    
    print("\nПервые 10 записей:")
    for i, r in enumerate(data[:10]):
        rating = r.get('rating', 'N/A')
        title = r.get('title', r.get('film', 'Unknown'))
        year = r.get('year', '')
        print(f"{i+1}. {title} {year} — {rating}")

if __name__ == "__main__":
    print("="*50)
    print("ПАРСЕР IMDb TOP 250")
    print("="*50)
    
    # Парсим топ-250 фильмов IMDb
    films = parse_imdb_top250()
    
    if films:
        save_to_csv(films, "imdb_top250.csv")
        save_to_excel(films, "imdb_top250.xlsx")
        print_stats(films)
    else:
        print("Не удалось получить данные с IMDb")
