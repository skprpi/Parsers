import csv

import requests
from bs4 import BeautifulSoup


def get_html(url):
    response = requests.get(url)
    return response.text


def normalize_number(string):
    first_el = string.split()[0]
    result = first_el.replace(',', '')
    return result


def write_csv(data):
    with open('plugins.csv', 'a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow((data['name'],
                         data['url'],
                         data['reviews']))


def get_data(html):
    soup = BeautifulSoup(html, 'lxml')
    popular = soup.find_all('section')[1]
    plugins = popular.find_all('article')

    for plugin in plugins:
        name = plugin.find('h3').text
        url = plugin.find('h3').find('a').get('href')
        reviews = plugin.find('span', class_='rating-count').find('a').text
        data = {'name': name, 'url': url, 'reviews': normalize_number(reviews)}
        write_csv(data)


def main():
    url = 'https://wordpress.org/plugins/'
    get_data(get_html(url))


if __name__ == '__main__':
    main()
