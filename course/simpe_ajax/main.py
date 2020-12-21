import requests
import csv


def get_html(url):
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
            # print(columns)
        except:
            continue


def parse_one_page(num_page):
    url = f'https://www.liveinternet.ru/rating/ru//today.tsv?page={num_page}'
    html = get_html(url)
    data = html.strip().split('\n')[1:]
    normalize_data(data)


def find_count_pages():
    url = f'https://www.liveinternet.ru/rating/ru//today.tsv?page={1}'
    html = get_html(url)
    count_pages = int((int(html.strip().split('\n')[0].split()[1]) + 29) / 30)
    return count_pages


def main():
    count_pages = find_count_pages()
    for i in range(1, count_pages + 1):
        parse_one_page(i)
        print(f'Done {i} / {count_pages}')


if __name__ == '__main__':
    main()
