import sqlite3, dataclasses

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
                data = dict(i)
                obj = TABLES[table_name](**data)
            except Exception as err:
                continue
            else:
                self.create_columns(table_name, obj)

    def create_columns(self, table_name, data):
        print(data)
        columns = ', '.join(asdict(data).keys())
        args = '%s, ' * len(asdict(data).keys())
        self.__cur.execute(
            f"""
            INSERT INTO content.{table_name} ({columns})
            VALUES ({args[:-2]})
            ON CONFLICT (id) DO NOTHING;
            """, tuple(asdict(data).values())
        )
