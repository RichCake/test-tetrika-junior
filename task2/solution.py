import requests
from bs4 import BeautifulSoup
import csv
from collections import defaultdict
import time


BASE_URL = "https://ru.wikipedia.org"
START_PATH = "/wiki/Категория:Животные_по_алфавиту"
OUTPUT_FILENAME = "beasts.csv"
HEADERS = {
    'User-Agent': 'AnimalCounterBot (arsenijkarpov@ya.ru)'
}


def fetch_animal_counts():
    # Выполняется около 5 минут
    animal_counts = defaultdict(int)
    current_path = START_PATH
    page_num = 1

    while current_path:
        url = BASE_URL + current_path
        print(f"Обработка страницы {page_num}: {url}")

        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        mw_pages_div = soup.find('div', id='mw-pages')

        list_items_container = mw_pages_div.find('div', class_='mw-category-columns')

        all_li_elements = list_items_container.find_all('li')

        for item in all_li_elements:
            link = item.find('a')
            if link and link.text:
                name = link.text.strip()
                if name:
                    first_letter = name[0].upper()
                    animal_counts[first_letter] += 1

        next_page_link_tag = mw_pages_div.find('a', string='Следующая страница')

        if next_page_link_tag and next_page_link_tag.get('href'):
            current_path = next_page_link_tag.get('href')
        else:
            current_path = None

        page_num += 1
        time.sleep(1)
    print("Обработка закончена")

    return animal_counts


def save_to_csv(counts, filename=OUTPUT_FILENAME):
    sorted_counts = sorted(counts.items(), key=lambda item: item[0])

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(sorted_counts)


if __name__ == '__main__':
    collected_counts = fetch_animal_counts()
    save_to_csv(collected_counts)
