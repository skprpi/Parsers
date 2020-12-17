import requests
from bs4 import BeautifulSoup


def get_html(url):
    response = requests.get(url)
    return response.text


def get_data(html):
    soup = BeautifulSoup(html, 'lxml')
    header = soup.find('div', id='home-welcome').find('header')
    h1_text = header.find('h1').text
    p_text = header.find('p').text
    title = f'{h1_text}\n{p_text}'
    return title


def main():
    url = 'https://wordpress.org/'
    print(get_data(get_html(url)))


if __name__ == '__main__':
    main()

