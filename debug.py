from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = "https://letterboxd.com/rfeldman9/films/diary/page/1/"
driver.get(url)
import time

time.sleep(3)

# Находим первую строку
rows = driver.find_elements(By.CSS_SELECTOR, "tr.diary-entry-row")
print(f"Найдено строк: {len(rows)}")

if rows:
    first_row = rows[0]
    print("\nВся HTML первой строки:")
    print(first_row.get_attribute("outerHTML"))

    print("\n\nИщем все ссылки:")
    links = first_row.find_elements(By.TAG_NAME, "a")
    for i, link in enumerate(links):
        print(f"  {i + 1}. Текст: '{link.text}', href: {link.get_attribute('href')}")

driver.quit()