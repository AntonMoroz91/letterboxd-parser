import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from typing import List, Dict

def collect_user_rates_rss(user_login: str) -> List[Dict[str, str]]:
    """
    Парсит RSS-ленту пользователя Letterboxd (не блокируется).
    """
    url = f'https://letterboxd.com/{user_login}/rss/'
    data = []
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    print(f"Парсинг RSS пользователя: {user_login}")
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code != 200:
            print(f"Ошибка {response.status_code}")
            return []
        
        soup = BeautifulSoup(response.text, 'xml')
        items = soup.find_all('item')
        
        print(f"Найдено записей в RSS: {len(items)}")
        
        for item in items:
            # Название фильма
            title = item.find('title')
            if not title or not title.text:
                continue
            film_name = title.text.strip()
            
            # Извлекаем год из названия или описания
            year = ""
            description = item.find('description')
            if description and description.text:
                import re
                match = re.search(r'\b(19|20)\d{2}\b', description.text)
                if match:
                    year = match.group()
            
            # Извлекаем оценку из описания (звезды)
            rating = None
            if description and description.text:
                stars = description.text.count('★')
                if stars > 0:
                    rating = str(stars)
                elif '½' in description.text:
                    rating = '0.5'
            
            if rating:
                data.append({
                    'film_name': film_name,
                    'release_year': year,
                    'rating': rating
                })
        
        return data
        
    except Exception as e:
        print(f"Ошибка: {e}")
        return []

def save_to_csv(data: List[Dict[str, str]], filename: str) -> None:
    if data:
        pd.DataFrame(data).to_csv(filename, index=False, encoding='utf-8')
        print(f"✅ Сохранено в {filename}")
    else:
        print("Нет данных для сохранения")

def save_to_excel(data: List[Dict[str, str]], filename: str) -> None:
    if data:
        pd.DataFrame(data).to_excel(filename, index=False)
        print(f"✅ Сохранено в {filename}")
    else:
        print("Нет данных для сохранения")

if __name__ == "__main__":
    print("="*50)
    print("ПАРСЕР LETTERBOXD (RSS - не блокируется)")
    print("="*50)
    
    USER_LOGIN = "rfeldman9"
    
    ratings = collect_user_rates_rss(USER_LOGIN)
    
    if ratings:
        save_to_csv(ratings, f"{USER_LOGIN}_rates.csv")
        save_to_excel(ratings, f"{USER_LOGIN}_rates.xlsx")
        
        print(f"\n📊 Всего оценок: {len(ratings)}")
        print("\n📋 Первые 5 записей:")
        for i, r in enumerate(ratings[:5]):
            print(f"{i+1}. {r['film_name']} ({r['release_year']}) — {r['rating']}/10")
        
        # Статистика
        if len(ratings) > 0:
            df = pd.DataFrame(ratings)
            df['rating'] = pd.to_numeric(df['rating'])
            print(f"\n📈 Средняя оценка: {df['rating'].mean():.2f}/10")
    else:
        print("\n❌ Не удалось получить данные.")
        print("Попробуйте другого пользователя, например:")
        print("   python letterboxd_parser.py dave")
