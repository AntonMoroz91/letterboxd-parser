import cloudscraper
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from typing import List, Dict

def collect_user_rates(user_login: str = "rfeldman9") -> List[Dict[str, str]]:
    scraper = cloudscraper.create_scraper(
        interpreter='javascript',
        delay=15,
        browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True}
    )
    
    scraper.headers.update({
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
    })
    
    page = 1
    data = []
    print(f"Парсинг пользователя: {user_login}")

    while True:
        url = f'https://letterboxd.com/{user_login}/films/diary/page/{page}/'
        print(f"Страница {page}...")

        try:
            time.sleep(random.uniform(1, 2))
            response = scraper.get(url, timeout=30)
            
            if response.status_code == 403:
                print("Блокировка, жду 5 секунд...")
                time.sleep(5)
                continue
            if response.status_code != 200:
                break

            soup = BeautifulSoup(response.text, 'lxml')
            rows = soup.find_all('tr', class_='diary-entry-row')
            if not rows:
                break

            for row in rows:
                if 'not-rated' in row.get('class', []):
                    continue

                title_td = row.find('td', class_='td-film-details')
                if not title_td:
                    continue
                title = title_td.find('a').text.strip()

                year_td = row.find('td', class_='td-released')
                year = year_td.text.strip() if year_td else ''

                rating_td = row.find('td', class_='td-rating')
                if not rating_td:
                    continue
                rating_span = rating_td.find('span', class_='rating')
                if not rating_span:
                    continue
                classes = rating_span.get('class', [])
                if len(classes) < 2:
                    continue
                rating = classes[1].split('-')[1]

                data.append({
                    'film_name': title,
                    'release_year': year,
                    'rating': rating
                })

            page += 1

        except Exception as e:
            print(f"Ошибка: {e}")
            break

    print(f"Всего оценок: {len(data)}")
    return data

def save_to_csv(data: List[Dict[str, str]], filename: str) -> None:
    if data:
        pd.DataFrame(data).to_csv(filename, index=False, encoding='utf-8')
        print(f"Сохранено в {filename}")

def save_to_excel(data: List[Dict[str, str]], filename: str) -> None:
    if data:
        pd.DataFrame(data).to_excel(filename, index=False)
        print(f"Сохранено в {filename}")

if __name__ == "__main__":
    print("="*50)
    print("ПАРСЕР LETTERBOXD")
    print("="*50)
    
    ratings = collect_user_rates("rfeldman9")
    
    if ratings:
        save_to_csv(ratings, "rfeldman9_rates.csv")
        save_to_excel(ratings, "rfeldman9_rates.xlsx")
        
        print("\nПервые 5 записей:")
        for i, r in enumerate(ratings[:5]):
            print(f"{i+1}. {r['film_name']} ({r['release_year']}) — {r['rating']}/10")
    else:
        print("Не удалось получить данные")
