# Letterboxd User Ratings Parser

## Постановка задачи
Разработать парсер для сайта Letterboxd, который по логину пользователя собирает информацию о всех фильмах, добавленных в дневник (Diary): название, год выпуска и оценку (от 1 до 10). Результат сохраняется в формате Excel или CSV для дальнейшего анализа.

## Инструкция по сборке и запуску

### 1. Клонирование репозитория
git clone https://github.com/AntonMoroz91/letterboxd-parser.git
cd letterboxd-parser

### 2. Установка зависимостей
python -m venv venv
source venv/bin/activate   # для Linux/macOS
venv\Scripts\activate      # для Windows
pip install -r requirements.txt

### 3. Запуск парсера
python letterboxd_parser.py
Скрипт предложит ввести логин и имя выходного файла.

### 4. Результат
Будет создан Excel-файл с колонками:
- film_name – название фильма
- release_date – год выпуска
- rating – оценка (от 1 до 10) или None, если оценка не проставлена

## Пример результатов работы парсера
Для пользователя rfeldman9:

| film_name | release_date | rating |
|-----------|--------------|--------|
| The Nice Guys | 2016 | 9 |
| Last Action Hero | 1993 | 7 |
| Tokyo Godfathers | 2003 | 10 |
| Perfect Blue | 1997 | 10 |
| Paprika | 2006 | 9 |

Всего собрано 629 записей (включая фильмы без оценки).
