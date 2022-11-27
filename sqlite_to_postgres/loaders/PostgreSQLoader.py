from dataclasses import asdict

from psycopg2.extensions import connection

from sqlite_to_postgres.models import TABLES


class PostgresSaver:

    def __init__(self, conn: connection):
        self.__cur = conn.cursor()

    def save_all_data(self, datas):
        table_name = datas[0]
        data_array = datas[1]
        for i in data_array:
            try:
                data = TABLES[table_name](*i)
            except:
                continue
            else:
                self.create_columns(table_name, data)

    def create_columns(self, table_name, data):
        columns = asdict(data).keys()
        print(columns)
