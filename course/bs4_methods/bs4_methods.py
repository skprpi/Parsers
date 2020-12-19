import re

from bs4 import BeautifulSoup


def find_some(soup):
    """Удобно использовать словарь для поиска чего-либо"""
    data = soup.find_all('div', {'data-set': 'salary'})
    row = soup.find_all('div', {'class': 'row'})
    print(data)
    print()
    print(row)


def find_parent_elements(soup):
    """parent - даёт  доступ к родительскому элементу"""
    alena = soup.find('div', text='Alena')
    print(alena.parent)
    print(end='\n\n\n')
    print(alena.parent.parent)


def find_specific_parent(soup):
    """find_parent - поиск конкретного родителя"""
    alena = soup.find('div', text='Alena')
    print(alena.find_parent(class_='row'))


def find_sibling(soup):
    """find_next_sibling, find_previous_sibling - поиск на одном уровне"""
    kate_p = soup.find('div', text='Kate').find_parent(class_='row')
    print(kate_p.find_next_sibling(class_='row'), end='\n\n\n')
    print(kate_p.find_previous_sibling(class_='row'))


def get_copywriter(tag):
    whois = tag.find('div', id='whois').text.strip()
    if 'Copywriter' in whois:
        return tag
    return None


def find_copywriters(soup):
    """Пример фильтрующей функции"""
    copywriters = []
    persons = soup.find_all('div', class_='row')
    for person in persons:
        cw = get_copywriter(person)
        if cw:
            copywriters.append(cw)
    print(copywriters)
    print(len(copywriters))


def get_salary(text):
    """Так же для поиска можно использовать search + group
    ^ - начало строки
    $ - конец строки
    . - любой символ
    + - неограниченное кол-во вхождений
    \d - цифры
    \w - буквы,  цыфры, _
    
    """
    pattern = r'\d{1,9}'  # ищем число длинной от 1 до 9 символов
    salary = re.findall(pattern, text)  # re.findall(что искать, где искать)
    return salary


def find_salary(soup):
    """Сложность в том, что описание текста зарплат везде разное и мы
    не знаем на каком месте в строке написана зарплата
    https://pythex.org/ - сервис валидации регулярных выражений
    """
    salary = soup.find_all('div', {'data-set': 'salary'})
    for el in salary:
        text = el.text.strip()
        rez = get_salary(text)
        print(f'До обработки: {text}\nПосле: {rez}')


def main():
    file = open('index.html').read()
    soup = BeautifulSoup(file, 'lxml')

    find_salary(soup)


if __name__ == '__main__':
    main()
