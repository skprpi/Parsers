import csv
from datetime import datetime
from multiprocessing import Pool
from time import sleep

import requests


def get_html(url):
    """sleep - замедляет парсинг sleep(1) - на 1 секунду"""
    # sleep(1)
    response = requests.get(url)
    return response.text


def write_csv(data):
    with open('websites.csv', 'a', newline='') as file:
        order = ['name', 'url', 'description', 'traffic', 'persent']
        writer = csv.DictWriter(file, fieldnames=order, delimiter=';')
        writer.writerow(data)


def do_dict_from_column(columns):
    return {
        'name': columns[0],
        'url': columns[1],
        'description': columns[2],
        'traffic': columns[3],
        'persent': columns[4],
    }


def normalize_data(data_l):
    for row in data_l:
        try:
            columns = row.strip().split('\t')
            data_dict = do_dict_from_column(columns)
            write_csv(data_dict)
        except:
            continue


def parse_one_page(url):
    html = get_html(url)
    data = html.strip().split('\n')[1:]
    normalize_data(data)


def find_count_pages():
    url = f'https://www.liveinternet.ru/rating/ru//today.tsv?page={1}'
    html = get_html(url)
    count_pages = int((int(html.strip().split('\n')[0].split()[1]) + 29) / 30)
    return count_pages


def main():
    """
    pool.map(find_count_pages, urls) - каждый элемент списка передаёт
    в функцию
    """
    start = datetime.now()
    count_pages = find_count_pages()
    url = 'https://www.liveinternet.ru/rating/ru//today.tsv?page={}'
    urls = [url.format(str(i)) for i in range(1, count_pages + 1)]
    with Pool(10) as pool:
        try:
            pool.map(parse_one_page, urls)
        except:
            print('OOps')
    print(datetime.now() - start)


if __name__ == '__main__':
    main()
