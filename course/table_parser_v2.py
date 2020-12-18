import csv

import requests
from bs4 import BeautifulSoup


def get_html(url):
    response = requests.get(url)
    if response.ok:
        return response.text
    raise ConnectionError('Something wrong')


def write_csv(data):
    with open('data.csv', 'a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(data)


def normalize_price(text):
    return text[1:].replace(',', '').replace('.', ',')


def get_data(html):
    soup = BeautifulSoup(html, 'lxml')
    data_arr = soup.find('tbody').find_all('tr')
    for data in data_arr:
        try:
            td_arr = data.find_all('td')
        except:
            continue
        try:
            name = td_arr[2].find('p').text
            url = 'https://coinmarketcap.com' + td_arr[2].find('a').get('href')
            price = normalize_price(
                td_arr[3].find('a', class_='cmc-link').text
            )
            print(name, url, price)
        except:
            continue
        write_csv((name, url, price))


def main():
    url = 'https://coinmarketcap.com/'
    url_new = url
    page_index = 1
    while True:
        try:
            html = get_html(url_new)
            get_data(html)
            url_new = f'{url}{page_index}/'
            page_index += 1
        except:
            break


if __name__ == '__main__':
    main()
