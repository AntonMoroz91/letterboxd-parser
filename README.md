# Парсер оценок Letterboxd

## Постановка задачи
Сбор всех оценок пользователя Letterboxd. Парсер обходит защиту Cloudflare, парсит дневник пользователя и извлекает название фильма, год выпуска и оценку. Результаты сохраняются в CSV и Excel.

## Установка и запуск

1. Установите библиотеки:
   pip install -r requirements.txt

2. Запустите:
   python letterboxd_parser.py

## Результат
- rfeldman9_rates.csv
- rfeldman9_rates.xlsx

## Пример вывода
Первые 5 записей:
1. The Nice Guys (2016) — 9/10
2. Last Action Hero (1993) — 7/10
3. Tokyo Godfathers (2003) — 10/10
4. Perfect Blue (1997) — 10/10
5. Paprika (2006) — 9/10
