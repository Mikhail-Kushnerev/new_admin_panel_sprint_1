from sqlite3 import Connection
from collections import deque

from sqlite_to_postgres.models import TABLES


class SQLiteExtractor:

    def __init__(
            self,
            conn: Connection,
            deque=deque()
    ):
        self.__cur = conn.cursor()
        self.__deque = deque

    def extract_movies(self):
        self.check_tables()
        return self.send_datas()

    def check_tables(self):
        self.__cur.execute(
            '''
            SELECT name
            FROM sqlite_master
            WHERE type='table';
            '''
        )
        datas = self.__cur.fetchall()
        if not self.size_datas(datas):
            raise
        for table_name in datas:
            self.__deque.append(table_name[0])

    def send_datas(self):
        while self.__deque:
            table_name = self.__deque.popleft()
            if self.validate_name(table_name):
                self.__cur.execute('''SELECT * FROM {0}'''.format(table_name))
                datas = self.__cur.fetchmany(500)
                if not self.size_datas(datas):
                    break
                yield table_name, datas

    @staticmethod
    def validate_name(table_name):
        return TABLES[table_name] if table_name in TABLES else False

    @staticmethod
    def size_datas(datas):
        return len(datas)
