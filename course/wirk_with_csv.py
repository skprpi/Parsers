import csv


def write_csv(data):
    with open('data.csv', 'a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(data)


def write_csv2(data):
    with open('data2.csv', 'a', newline='') as file:
        order = ['message', 'sex']
        writer = csv.DictWriter(file, fieldnames=order, delimiter=';')
        writer.writerow(data)


def open_csv(filename):
    with open(filename) as file:
        order = ['message', 'sex']
        reader = csv.DictReader(file, fieldnames=order, delimiter=';')
        for row in reader:
            print(row)


def main():
    tup = [('Hello', 'Man'), ('Hello', 'Woman')]
    d = [{'message': 'Hello', 'sex': 'Male'},
         {'message': 'Hello', 'sex': 'Female'}]
    for el in tup:
        write_csv(el)
    for el in d:
        write_csv2(el)
    open_csv('data2.csv')


if __name__ == '__main__':
    main()
