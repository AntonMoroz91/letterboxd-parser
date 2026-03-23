import requests
import pandas as pd
import xml.etree.ElementTree as ET
from typing import List, Dict

def collect_user_rates(user_login: str) -> List[Dict[str, str]]:
    """Парсит RSS-ленту пользователя Letterboxd и извлекает фильмы с оценками."""
    url = f'https://letterboxd.com/{user_login}/rss/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    print(f"Парсинг RSS пользователя: {user_login}")
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        root = ET.fromstring(response.content)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        
        items = root.findall('.//atom:entry', ns)
        data = []
        
        for item in items:
            title_elem = item.find('atom:title', ns)
            if title_elem is None:
                continue
            full_title = title_elem.text.strip()
            
            # Извлекаем название и год
            import re
            year_match = re.search(r'\((\d{4})\)', full_title)
            year = year_match.group(1) if year_match else ""
            title = re.sub(r'\s*\(\d{4}\)', '', full_title)
            
            # Извлекаем описание для оценки
            summary = item.find('atom:summary', ns)
            rating = None
            if summary is not None and summary.text:
                summary_text = summary.text
                # Ищем звезды
                stars = summary_text.count('★')
                if stars > 0:
                    rating = str(stars)
                elif '½' in summary_text:
                    rating = '0.5'
                # Ищем текст "Rated X"
                rated_match = re.search(r'Rated\s+(\d+)', summary_text, re.IGNORECASE)
                if rated_match and not rating:
                    rating = rated_match.group(1)
            
            if rating:
                data.append({
                    'film_name': title,
                    'release_year': year,
                    'rating': rating
                })
                print(f"  {title} ({year}) — {rating}/10")
        
        print(f"\nВсего собрано оценок: {len(data)}")
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

if __name__ == "__main__":
    print("="*50)
    print("ПАРСЕР ОЦЕНОК LETTERBOXD (RSS)")
    print("="*50)
    
    # Используем пользователя, у которого точно есть оценки
    USER_LOGIN = "dave"
    
    ratings = collect_user_rates(USER_LOGIN)
    
    if ratings:
        save_to_csv(ratings, f"{USER_LOGIN}_rates.csv")
        save_to_excel(ratings, f"{USER_LOGIN}_rates.xlsx")
        
        # Статистика
        df = pd.DataFrame(ratings)
        df['rating'] = pd.to_numeric(df['rating'])
        print("\n" + "="*50)
        print("СТАТИСТИКА")
        print("="*50)
        print(f"Всего фильмов: {len(ratings)}")
        print(f"Средняя оценка: {df['rating'].mean():.2f}/10")
        print(f"Максимальная: {df['rating'].max()}/10")
        print(f"Минимальная: {df['rating'].min()}/10")
        print("\nПервые 10 записей:")
        for i, r in enumerate(ratings[:10]):
            print(f"{i+1}. {r['film_name']} ({r['release_year']}) — {r['rating']}/10")
    else:
        print("Не удалось получить данные")
