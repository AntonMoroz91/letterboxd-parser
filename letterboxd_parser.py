
---

### **letterboxd_parser.py**
```python
"""
Letterboxd User Ratings Parser
Collects film ratings from a Letterboxd user's diary.
"""

import time
import requests
from bs4 import BeautifulSoup
import pandas as pd

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


def get_soup(url):
    """Fetch a URL and return a BeautifulSoup object."""
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'lxml')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def extract_rating(entry):
    """Extract rating from a diary entry row."""
    # Find the td with class containing 'td-rating'
    td_rating = entry.find('td', class_='td-rating')
    if not td_rating:
        return None

    rating_span = td_rating.find('span', class_='rating')
    if not rating_span:
        return None

    # Look for a class like 'rated-9'
    for cls in rating_span.get('class', []):
        if cls.startswith('rated-'):
            try:
                return int(cls.split('-')[1])
            except (IndexError, ValueError):
                return None
    return None


def collect_user_ratings(user_login):
    """
    Parse all pages of a user's diary and return a list of dictionaries
    with film name, release year, and rating.
    """
    page_num = 1
    data = []

    while True:
        url = f'https://letterboxd.com/{user_login}/films/diary/page/{page_num}/'
        print(f"Fetching {url}")
        soup = get_soup(url)
        if not soup:
            break

        entries = soup.find_all('tr', class_='diary-entry-row viewing-poster-container')
        if not entries:
            # No more entries – end of pages
            break

        for entry in entries:
            # Film name
            td_details = entry.find('td', class_='td-film-details')
            if td_details:
                name_tag = td_details.find('a')
                film_name = name_tag.text.strip() if name_tag else None
            else:
                film_name = None

            # Release year
            td_released = entry.find('td', class_='td-released center')
            release_date = td_released.text.strip() if td_released else None

            # Rating
            rating = extract_rating(entry)

            if film_name:
                data.append({
                    'film_name': film_name,
                    'release_date': release_date,
                    'rating': rating
                })

        page_num += 1
        # Small delay to avoid overwhelming the server
        time.sleep(1)

    return data


def save_to_excel(data, filename='user_ratings.xlsx'):
    """Save data to an Excel file."""
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    print(f"Saved {len(data)} records to {filename}")


def save_to_csv(data, filename='user_ratings.csv'):
    """Save data to a CSV file."""
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding='utf-8')
    print(f"Saved {len(data)} records to {filename}")


def main():
    print("Letterboxd User Ratings Parser")
    user_login = input("Enter Letterboxd username: ").strip()
    if not user_login:
        print("Username cannot be empty.")
        return

    print(f"Collecting ratings for user '{user_login}'...")
    ratings = collect_user_ratings(user_login)

    if not ratings:
        print("No ratings found. Check username or network.")
        return

    print(f"Collected {len(ratings)} entries.")
    save_format = input("Save as (excel/csv): ").strip().lower()
    filename = input("Output filename (without extension): ").strip() or "user_ratings"

    if save_format == 'csv':
        save_to_csv(ratings, f"{filename}.csv")
    else:
        save_to_excel(ratings, f"{filename}.xlsx")


if __name__ == '__main__':
    main()
