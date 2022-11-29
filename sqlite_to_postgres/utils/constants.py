"""Константные значения."""


PAGE_SIZE = 500
DB_SIZE = 5
TABLES = (
    'film_work',
    'genre',
    'person',
    'genre_film_work',
    'person_film_work',
)

LOGS_FORMAT = "|\t%(asctime)s – [%(levelname)s]: %(message)s. " \
              "Исполняемый файл – '%(filename)s': " \
              "функция – '%(funcName)s'(%(lineno)d)"
