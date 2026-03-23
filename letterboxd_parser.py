import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from typing import List, Dict

def collect_user_rates_rss(user_login: str) -> List[Dict[str, str]]:
    """
    Парсит RSS-ленту пользователя Letterboxd.
    """
    url = f'https://letterboxd.com/{user_login}/rss/'
    data = []
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    print(f"📡 Парсинг RSS пользователя: {user_login}")
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code != 200:
            print(f"❌ Ошибка {response.status_code}")
            return []
        
        soup = BeautifulSoup(response.text, 'xml')
        items = soup.find_all('item')
        
        print(f"📄 Найдено записей в RSS: {len(items)}")
        
        for item in items:
            # Название фильма
            title = item.find('title')
            if not title or not title.text:
                continue
            film_name = title.text.strip()
            
            # Извлекаем год из названия
            year = ""
            year_match = re.search(r'\((\d{4})\)', film_name)
            if year_match:
                year = year_match.group(1)
                # Убираем год из названия
                film_name = re.sub(r'\s*\(\d{4}\)', '', film_name)
            
            # Извлекаем оценку из description (ищем звезды)
            description = item.find('description')
            rating = None
            
            if description and description.text:
                desc_text = description.text
                # Ищем звезды (★)
                stars = desc_text.count('★')
                if stars > 0:
                    rating = str(stars)
                # Проверяем половину звезды
                elif '½' in desc_text:
                    rating = '0.5'
                # Если звезд нет, ищем число после "Rated "
                else:
                    rated_match = re.search(r'Rated\s+(\d+)/?', desc_text, re.IGNORECASE)
                    if rated_match:
                        rating = rated_match.group(1)
            
            # Добавляем только записи с оценкой
            if rating:
                data.append({
                    'film_name': film_name,
                    'release_year': year,
                    'rating': rating
                })
                print(f"   ✅ {film_name} ({year}) — {rating}/10")
            else:
                print(f"   ⚠️ {film_name} — без оценки")
        
        return data
        
    except Exception as e:
        print(f"⚠️ Ошибка: {e}")
        return []

def save_to_csv(data: List[Dict[str, str]], filename: str) -> None:
    if data:
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"\n💾 Сохранено в {filename}")
        print(f"   Всего записей: {len(data)}")
    else:
        print("Нет данных для сохранения")

def save_to_excel(data: List[Dict[str, str]], filename: str) -> None:
    if data:
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)
        print(f"💾 Сохранено в {filename}")

if __name__ == "__main__":
    print("="*50)
    print("🎬 ПАРСЕР ОЦЕНОК LETTERBOXD (RSS)")
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
        df = pd.DataFrame(ratings)
        df['rating'] = pd.to_numeric(df['rating'])
        print(f"\n📈 Средняя оценка: {df['rating'].mean():.2f}/10")
        print(f"🏆 Максимальная: {df['rating'].max()}/10")
        print(f"📉 Минимальная: {df['rating'].min()}/10")
    else:
        print("\n❌ Не удалось получить данные с оценками.")
        print("Попробуйте другого пользователя, например:")
        print("   python letterboxd_parser.py dave")
