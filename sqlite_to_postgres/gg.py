import sqlite3

import psycopg2
from psycopg2.extras import DictCursor
from psycopg2.extensions import connection as _connection

from sqlite_to_postgres.config.database import dsl


class Tests:

    def __init__(self, sqlite_connection: sqlite3.Connection, pg_connection: _connection):
        self.sqlite_cur = sqlite_connection.cursor()
        self.pg_cur = pg_connection.cursor()

    def check_count(self, table):
        stmt = '''
        SELECT count(*) AS cnt FROM {0};
        '''.format(table)
        sqlite_row = self.sqlite_cur.execute(stmt).fetchone()
        sqlite_count = dict(sqlite_row)
        pg_stmt = '''
        SELECT count(*) FROM content.{0}
        '''.format(table)
        self.pg_cur.execute(pg_stmt)
        pg_count = dict(self.pg_cur.fetchone())
        assert sqlite_count['cnt'] == pg_count['count']

    def check_values(self, table):
        sqlite_stmt = "select * from {0};".format(table)
        sqlite_select = self.sqlite_cur.execute(sqlite_stmt)
        for row in sqlite_select:
            sql_dict = dict(row)
            sql_dict.pop('created_at', None)
            sql_dict.pop('updated_at', None)
            pg_stmt = "select * from content.{0} where id='{1}'".format(table, row['id'])
            self.pg_cur.execute(pg_stmt)
            pg_row = self.pg_cur.fetchone()
            pg_dict = dict(pg_row)
            pg_dict.pop('created_at', None)
            pg_dict.pop('updated_at', None)
            assert sql_dict == pg_dict

    def __call__(self, *args, **kwargs):
        for i in ('genre', 'film_work', 'person', 'person_film_work', 'genre_film_work'):
            self.check_count(i)
            self.check_values(i)


if __name__ == '__main__':

    with sqlite3.connect(dsl['sqlite']['test']) as sqlite_conn,\
            psycopg2.connect(**dsl['postgres'], cursor_factory=DictCursor) as pg_conn:
        sqlite_conn.row_factory = sqlite3.Row
        obj = Tests(sqlite_conn, pg_conn)
        obj()
