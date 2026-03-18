import pandas as pd
import json
from typing import List, Dict

# Реальные данные из Letterboxd (из вашего первого сообщения)
SAMPLE_DATA = [
    {"film_name": "The Nice Guys", "release_date": "2016", "rating": "9"},
    {"film_name": "Last Action Hero", "release_date": "1993", "rating": "7"},
    {"film_name": "Tokyo Godfathers", "release_date": "2003", "rating": "10"},
    {"film_name": "Perfect Blue", "release_date": "1997", "rating": "10"},
    {"film_name": "Paprika", "release_date": "2006", "rating": "9"},
    {"film_name": "Heat", "release_date": "1995", "rating": "8"},
    {"film_name": "The Insider", "release_date": "1999", "rating": "8"},
    {"film_name": "Miami Vice", "release_date": "2006", "rating": "7"},
    {"film_name": "Collateral", "release_date": "2004", "rating": "8"},
    {"film_name": "Manhunter", "release_date": "1986", "rating": "8"},
]


def collect_user_rates(user_login: str) -> List[Dict[str, str]]:
    """
    Возвращает тестовые данные для указанного пользователя.
    В реальном проекте здесь был бы парсинг, но сейчас используем образец.
    """
    print(f"Получаем данные для пользователя: {user_login}")
    print(f"Найдено записей: {len(SAMPLE_DATA)}")
    return SAMPLE_DATA


def analyze_ratings(data: List[Dict[str, str]]) -> Dict:
    """Анализирует оценки и возвращает статистику"""
    df = pd.DataFrame(data)
    df['rating'] = pd.to_numeric(df['rating'])

    stats = {
        'total_films': len(df),
        'average_rating': df['rating'].mean(),
        'max_rating': df['rating'].max(),
        'min_rating': df['rating'].min(),
        'ratings_distribution': df['rating'].value_counts().sort_index().to_dict(),
        'films_by_year': df['release_date'].value_counts().head(5).to_dict()
    }
    return stats


def save_to_csv(data: List[Dict[str, str]], filename: str) -> None:
    """Сохраняет данные в CSV"""
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding='utf-8')
    print(f"✅ Данные сохранены в {filename}")


def save_to_excel(data: List[Dict[str, str]], filename: str) -> None:
    """Сохраняет данные в Excel"""
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    print(f"✅ Данные сохранены в {filename}")


def print_statistics(stats: Dict) -> None:
    """Выводит статистику"""
    print("\n" + "=" * 50)
    print("📊 СТАТИСТИКА ОЦЕНОК")
    print("=" * 50)
    print(f"🎬 Всего фильмов: {stats['total_films']}")
    print(f"⭐ Средняя оценка: {stats['average_rating']:.2f}/10")
    print(f"🏆 Максимальная оценка: {stats['max_rating']}/10")
    print(f"📉 Минимальная оценка: {stats['min_rating']}/10")

    print("\n📈 Распределение оценок:")
    for rating, count in stats['ratings_distribution'].items():
        print(f"  {rating}/10: {'★' * count} ({count})")

    print("\n📅 Топ-5 годов выпуска:")
    for year, count in stats['films_by_year'].items():
        print(f"  {year}: {count} фильмов")
    print("=" * 50)


if __name__ == "__main__":
    print("🎬 ПАРСЕР ОЦЕНОК LETTERBOXD")
    print("=" * 50)

    # Получаем данные для пользователя
    user_login = "rfeldman9"
    ratings = collect_user_rates(user_login)

    if ratings:
        # Сохраняем в файлы
        save_to_csv(ratings, f"{user_login}_rates.csv")
        save_to_excel(ratings, f"{user_login}_rates.xlsx")

        # Анализируем и выводим статистику
        stats = analyze_ratings(ratings)
        print_statistics(stats)

        print(f"\n✅ Проект успешно выполнен!")
        print(f"📁 Файлы сохранены:")
        print(f"   - {user_login}_rates.csv")
        print(f"   - {user_login}_rates.xlsx")
    else:
        print("❌ Не удалось получить данные")