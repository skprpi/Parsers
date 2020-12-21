import csv
from datetime import datetime

from peewee import *

db = SqliteDatabase('test.sqlite')


def timer(func):
    """Чтобы не потерять имя функции и документации
    или же можно воспользоваться декоратором wraps
    from functools import wraps
    """

    def inner(*args, **kwargs):
        start = datetime.now()
        func(*args, **kwargs)
        return datetime.now() - start

    inner.__name__ = func.__name__
    inner.__doc__ = func.__doc__
    return inner


class Coin(Model):
    name = CharField(max_length=50)
    salary = CharField(max_length=50)

    class Meta:
        database = db


@timer
def way_to_write_db1(reader, order):
    for row in reader:
        coin = Coin(name=row[order[0]], salary=row[order[1]])
        coin.save()
        print(row)


@timer
def way_to_write_db2(coins):
    with db.atomic():
        for row in coins:
            Coin.create(**row)


def read_csv(file_name):
    """
    Не забудь установить библиотеки
    pip install peewee
    pip install psycopg2
    pip install psycopg2.binary
    """
    with open(file_name, 'r') as file:
        order = ('name', 'salary')
        reader = csv.DictReader(file, delimiter=';', fieldnames=order)
        coins = list(reader)

        # этот способ получиля быстрее
        print(way_to_write_db1(reader, order))

        # этот способ медленее
        print(way_to_write_db2(coins))


def main():
    db.connect()
    db.create_tables([Coin])
    read_csv('text.csv')


if __name__ == '__main__':
    main()
