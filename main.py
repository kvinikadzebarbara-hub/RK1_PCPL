from operator import itemgetter


class Database:
    """База данных"""
    def __init__(self, id, name):
        self.id = id
        self.name = name


class DataTable:
    """Таблица данных"""
    def __init__(self, id, name, rows, db_id):
        self.id = id
        self.name = name
        self.rows = rows      # количественный признак: число записей
        self.db_id = db_id


class TableDatabase:
    """Связь 'таблицы базы данных' (многие-ко-многим)"""
    def __init__(self, db_id, table_id):
        self.db_id = db_id
        self.table_id = table_id


# Базы данных
dbs = [
    Database(1, 'Аналитическая БД'),
    Database(2, 'Архивная БД'),
    Database(3, 'Оперативная БД'),
    Database(11, 'Аналитическая (резервная) БД'),
    Database(22, 'Архивная (резервная) БД'),
    Database(33, 'Оперативная (резервная) БД'),
]

# Таблицы данных
tables = [
    DataTable(1, 'Аккаунты', 1200, 1),
    DataTable(2, 'Архив_заказов', 5400, 2),
    DataTable(3, 'Клиенты', 800, 3),
    DataTable(4, 'Аналитика_продаж', 350, 3),
    DataTable(5, 'Аудит_операций', 2100, 3),
]

# Связь многие-ко-многим
tables_dbs = [
    TableDatabase(1, 1),
    TableDatabase(2, 2),
    TableDatabase(3, 3),
    TableDatabase(3, 4),
    TableDatabase(3, 5),
    TableDatabase(11, 1),
    TableDatabase(22, 2),
    TableDatabase(33, 3),
    TableDatabase(33, 4),
    TableDatabase(33, 5),
]


def main():
    # Соединение один-ко-многим: (таблица, число записей, БД)
    one_to_many = [(t.name, t.rows, d.name)
                   for d in dbs
                   for t in tables
                   if t.db_id == d.id]

    # Соединение многие-ко-многим
    many_to_many_temp = [(d.name, td.db_id, td.table_id)
                         for d in dbs
                         for td in tables_dbs
                         if d.id == td.db_id]

    many_to_many = [(t.name, t.rows, db_name)
                    for db_name, db_id, table_id in many_to_many_temp
                    for t in tables if t.id == table_id]

    # ---------- Задание В1 ----------
    print('Задание В1')
    res_1 = [(name, db) for name, _, db in one_to_many
             if name.startswith('А')]
    for name, db in res_1:
        print(f'  таблица «{name}» — БД «{db}»')

    # ---------- Задание В2 ----------
    print('\nЗадание В2')
    res_2_unsorted = []
    for d in dbs:
        d_tables = list(filter(lambda i: i[2] == d.name, one_to_many))
        if d_tables:
            d_rows = [rows for _, rows, _ in d_tables]
            d_min = min(d_rows)
            res_2_unsorted.append((d.name, d_min))
    res_2 = sorted(res_2_unsorted, key=itemgetter(1))
    for name, mn in res_2:
        print(f'  БД «{name}»: минимальное число записей = {mn}')

    # ---------- Задание В3 ----------
    print('\nЗадание В3')
    res_3 = sorted(many_to_many, key=itemgetter(0))
    for name, _, db in res_3:
        print(f'  таблица «{name}» — БД «{db}»')


if __name__ == '__main__':
    main()