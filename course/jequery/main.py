import requests
from bs4 import BeautifulSoup
import csv


def get_html(url):
    """
    Словарь может иметь и другие параметры, к каждому сайту нужно их подбирать
    """
    user_agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                       AppleWebKit/537.36 (KHTML, like Gecko)\
                        Chrome/87.0.4280.88 Safari/537.36'
    }
    response = requests.get(url, headers=user_agent)
    if response.ok:
        return response.text
    raise ConnectionError('Something wrong!')


def write_csv(data: dict):
    with open('data.csv', 'a', newline='') as file:
        order = ['year', 'phone', 'email']
        writer = csv.DictWriter(file, fieldnames=order, delimiter=';')
        writer.writerow(data)


def get_info(html):
    soup = BeautifulSoup(html, 'lxml')
    years = soup.find_all('p', class_='traxer-since')
    for year in years:
        try:
            email = year.find_next_sibling(
                'ul', class_='testimonial-meta'
            ).find('li', class_='email').text.strip()
        except:
            email = ''
        try:
            tel = year.find_next_sibling(
                'ul', class_='testimonial-meta'
            ).find('li', class_='tel').text.strip().replace('-', '')
        except:
           tel = ''
        data = {'email': email, 'phone': tel, 'year': year.text.split()[-1]}
        write_csv(data)
    if not years:
        return False
    return True


def main():
    url = 'https://catertrax.com/why-catertrax/traxers/page/{}/?' \
          'themify_builder_infinite_scroll=yes'
    val = True
    page = 1
    while val:
        val = get_info(get_html(url.format(page)))
        page += 1
    print(page)


if __name__ == '__main__':
    main()
