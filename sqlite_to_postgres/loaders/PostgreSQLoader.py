from dataclasses import asdict

from psycopg2.extensions import connection

from sqlite_to_postgres.models import TABLES
from sqlite_to_postgres.utils import WrongValuesError


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
                if not obj:
                    raise WrongValuesError()
            except WrongValuesError as err:
                err()
                continue
            else:
                self.create_columns(table_name, obj)

    def create_columns(self, table_name, data):
        keys = asdict(data).keys()
        values = asdict(data).values()
        columns = ', '.join(keys)
        args = '%s, ' * len(keys)
        self.__cur.execute(
            f"""
            INSERT INTO content.{table_name} ({columns})
            VALUES ({args[:-2]});
            """, tuple(values),
        )
