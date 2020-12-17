import requests
from bs4 import BeautifulSoup
import csv


def write_csv(data):
    with open('statistic.csv', 'a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow([data['name'], data['url'], data['price']])


def get_html(url):
    response = requests.get(url)
    return response.text


def normalize_price(string):
    price = string.replace(',', '')
    price = float(price)
    return price


def get_page_data(html, start_url):
    soup = BeautifulSoup(html, 'lxml')
    tr_list = soup.find('table').find('tbody').find_all('tr')
    for tr in tr_list[:10]:
        td_list = tr.find_all('td')
        if len(td_list) >= 2:
            name = td_list[2].find('p').text
            url = f"{start_url}{td_list[2].find('a').get('href')}"
            price_str = td_list[3].find('a', class_='cmc-link').text
            price = normalize_price(price_str[1:])
            data = {'name': name, 'price': price, 'url': url}
            write_csv(data)

    return len(tr_list)


def main():
    url = 'https://coinmarketcap.com/'
    print(get_page_data(get_html(url), url))


if __name__ == '__main__':
    main()
