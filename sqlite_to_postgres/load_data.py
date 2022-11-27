import sqlite3

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from config.database import dsl
from loaders import PostgresSaver, SQLiteExtractor


def load_from_sqlite(
        connection: sqlite3.Connection,
        pg_conn: _connection
):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_extractor = SQLiteExtractor(connection)

    datas = sqlite_extractor.extract_movies()
    for data in datas:
        postgres_saver.save_all_data(data)


if __name__ == '__main__':

    with sqlite3.connect(dsl['sqlite']['dbname']) as sqlite_conn,\
            psycopg2.connect(**dsl['postgres'], cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
