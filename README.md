# Letterboxd User Ratings Parser

## Постановка задачи
Разработать парсер для сайта Letterboxd, который по логину пользователя собирает информацию о всех фильмах, добавленных в дневник: название, год выпуска и оценку. Результат сохраняется в формате Excel, CSV или JSON.

## Инструкция по сборке и запуску

1. Клонирование репозитория:
git clone https://github.com/AntonMoroz91/letterboxd-parser.git
cd letterboxd-parser

2. Установка зависимостей:
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

3. Запуск парсера:
python letterboxd_parser.py

4. Введите логин пользователя, выберите формат сохранения и имя файла.

## Пример результатов работы парсера

Для пользователя rfeldman9 собрано 782 записи:

Train Dreams (2025) - 9
Frankenstein (2025) - 8
28 Years Later: The Bone Temple (2025) - 9
Bugonia (2025) - 9
People We Meet on Vacation (2025) - 8

## Структура проекта
letterboxd-parser/
.gitignore
README.md
requirements.txt
letterboxd_parser.py
rfeldman9.xlsx

## Используемые технологии
- Python 3.11+
- Selenium
- Pandas
- WebDriver Manager

## Примечание
При первом запуске автоматически скачается ChromeDriver. Убедитесь, что установлен браузер Google Chrome.
