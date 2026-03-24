import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    return driver

def collect_user_ratings(user_login):
    """
    Собирает все оценки пользователя Letterboxd.
    
    Args:
        user_login (str): Логин пользователя Letterboxd
        
    Returns:
        list: Список словарей с ключами film_name, release_date, rating
    """
    driver = setup_driver()
    data = []
    page_num = 1
    
    try:
        while True:
            url = f"https://letterboxd.com/{user_login}/films/diary/page/{page_num}/"
            print(f"Загружаю {url}")
            
            driver.get(url)
            time.sleep(3)
            
            # Ждем загрузки таблицы
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "table.diary-table"))
                )
            except:
                pass
            
            rows = driver.find_elements(By.CSS_SELECTOR, "tr.diary-entry-row")
            
            if not rows:
                print("Записи не найдены, завершаем")
                break
            
            print(f"Найдено {len(rows)} записей на странице {page_num}")
            
            for row in rows:
                try:
                    # Название фильма
                    film_name = None
                    name_elem = row.find_elements(By.CSS_SELECTOR, ".film-title, a[href*='/film/']")
                    if name_elem:
                        film_name = name_elem[0].text.strip()
                    
                    # Год выпуска
                    release_date = None
                    year_elem = row.find_elements(By.CSS_SELECTOR, ".released, .td-released")
                    if year_elem:
                        release_date = year_elem[0].text.strip()
                    
                    # Оценка
                    rating = None
                    rating_elem = row.find_elements(By.CSS_SELECTOR, ".rating")
                    if rating_elem:
                        classes = rating_elem[0].get_attribute("class")
                        if classes and "rated-" in classes:
                            for cls in classes.split():
                                if cls.startswith("rated-"):
                                    rating = int(cls.split("-")[1])
                    
                    if film_name:
                        data.append({
                            'film_name': film_name,
                            'release_date': release_date,
                            'rating': rating
                        })
                        print(f"  ✅ {film_name} ({release_date}) - {rating if rating else 'нет оценки'}")
                    else:
                        print(f"  ⚠️ Пропущена запись без названия")
                    
                except Exception as e:
                    continue
            
            page_num += 1
            time.sleep(2)
            
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        driver.quit()
    
    return data

def save_to_excel(data, filename='user_ratings.xlsx'):
    """Сохраняет данные в Excel файл"""
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    print(f"Сохранено {len(data)} записей в {filename}")

def save_to_csv(data, filename='user_ratings.csv'):
    """Сохраняет данные в CSV файл"""
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding='utf-8')
    print(f"Сохранено {len(data)} записей в {filename}")

def save_to_json(data, filename='user_ratings.json'):
    """Сохраняет данные в JSON файл"""
    df = pd.DataFrame(data)
    df.to_json(filename, orient='records', force_ascii=False, indent=2)
    print(f"Сохранено {len(data)} записей в {filename}")

def main():
    print("=" * 50)
    print("Letterboxd User Ratings Parser")
    print("=" * 50)
    print("\nДанный парсер собирает информацию о фильмах из дневника пользователя Letterboxd:")
    print("- Название фильма")
    print("- Год выпуска")
    print("- Оценка пользователя (от 1 до 10)")
    print("\nРезультат может быть использован для построения рекомендательных систем,")
    print("анализа предпочтений или создания персональной базы просмотренных фильмов.\n")
    
    user_login = input("Введите логин пользователя Letterboxd: ").strip()
    if not user_login:
        print("Логин не может быть пустым")
        return
    
    print(f"\nСобираю оценки для пользователя '{user_login}'...")
    print("Сейчас откроется браузер, НЕ закрывайте его\n")
    
    ratings = collect_user_ratings(user_login)
    
    if not ratings:
        print("\n❌ Ничего не найдено. Проверьте:")
        print("1. Правильно ли введен логин")
        print("2. Есть ли у пользователя дневник с фильмами")
        print("3. Проверьте подключение к интернету")
        return
    
    print(f"\n✅ Собрано {len(ratings)} записей!")
    
    print("\nВыберите формат сохранения:")
    print("1. Excel (.xlsx)")
    print("2. CSV (.csv)")
    print("3. JSON (.json)")
    
    format_choice = input("Введите номер (1-3) [1]: ").strip()
    
    filename = input("\nИмя файла [user_ratings]: ").strip()
    if not filename:
        filename = "user_ratings"
    
    if format_choice == "2":
        save_to_csv(ratings, f"{filename}.csv")
    elif format_choice == "3":
        save_to_json(ratings, f"{filename}.json")
    else:
        save_to_excel(ratings, f"{filename}.xlsx")
    
    print("\n🎉 Готово!")

if __name__ == '__main__':
    main()
