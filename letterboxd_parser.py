import requests
import pandas as pd
import xml.etree.ElementTree as ET
import re
from typing import List, Dict

def collect_user_rates(user_login: str) -> List[Dict[str, str]]:
    """Парсит RSS-ленту пользователя Letterboxd."""
    url = f'https://letterboxd.com/{user_login}/rss/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    print(f"Парсинг пользователя: {user_login}")
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        root = ET.fromstring(response.content)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        entries = root.findall('.//atom:entry', ns)
        
        data = []
        for entry in entries:
            title_elem = entry.find('atom:title', ns)
            if title_elem is None:
                continue
            full_title = title_elem.text
            
            year_match = re.search(r'\((\d{4})\)', full_title)
            year = year_match.group(1) if year_match else ""
            title = re.sub(r'\s*\(\d{4}\)', '', full_title)
            
            summary = entry.find('atom:summary', ns)
            rating = None
            if summary is not None and summary.text:
                star_count = summary.text.count('★')
                if star_count > 0:
                    rating = str(star_count)
                elif '½' in summary.text:
                    rating = '0.5'
            
            if rating:
                data.append({'film_name': title, 'year': year, 'rating': rating})
                print(f"  {title} ({year}) — {rating}/10")
        
        print(f"\nВсего оценок: {len(data)}")
        return data
    except Exception as e:
        print(f"Ошибка: {e}")
        return []

def save_results(data: List[Dict[str, str]], login: str):
    if not data:
        print("Нет данных")
        return
    
    df = pd.DataFrame(data)
    df.to_csv(f"{login}_rates.csv", index=False, encoding='utf-8')
    df.to_excel(f"{login}_rates.xlsx", index=False)
    print(f"Сохранено в {login}_rates.csv и {login}_rates.xlsx ({len(data)} записей)")
    
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
        print(f"{i+1}. {r['film_name']} ({r['year']}) — {r['rating']}/10")

if __name__ == "__main__":
    print("="*50)
    print("ПАРСЕР ОЦЕНОК LETTERBOXD")
    print("="*50)
    
    USER = "dave"
    ratings = collect_user_rates(USER)
    
    if ratings:
        save_results(ratings, USER)
    else:
        print(f"Не удалось получить данные для {USER}")
