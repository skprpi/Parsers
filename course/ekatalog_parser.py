import requests
from bs4 import BeautifulSoup
import csv


def get_html(url):
    response = requests.get(url)
    if response.ok:
        return response.text
    raise ConnectionError('Что-то пошло не так!')


def get_next_page(html, url):
    soup = BeautifulSoup(html, 'lxml')
    next_page = url + soup.find(
        'div', class_='list-pager-div'
    ).find('a', id='pager_next').get('href')
    return next_page


def normalize_num(string):
    rez = ''
    for el in string:
        if el.isdigit():
            rez += el
    return rez


def write_csv(data):
    with open('data.csv', 'a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(data)


def get_info(start_url, addition_url):
    html = get_html(start_url)
    while True:
        soup = BeautifulSoup(html, 'lxml')
        all_devise = soup.find(
            'form', id='list_form1'
        ).find_all(
            'div', class_=r"model-short-div"
        )
        for device in all_devise:

            try:
                name = device.find('a').find('span', class_='u').text
                price = device.find(
                    'div', class_='model-price-range'
                ).find_all('span')
            except:
                continue
            start_price = normalize_num(price[0].text)
            end_price = normalize_num(price[1].text)
            if end_price == '':
                end_price = start_price
            url = addition_url + device.find('a').get('href')
            write_csv((name, start_price, end_price, url))
            # print(name, start_price, end_price, url)
        try:
            next_page_url = get_next_page(html, addition_url)
            print(next_page_url)
            html = get_html(next_page_url)
        except:
            break


def main():
    url = 'https://www.e-katalog.ru/list/170/'
    get_info(url, 'https://www.e-katalog.ru')


if __name__ == '__main__':
    main()
