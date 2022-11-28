"""Кастомные исключения."""


class WrongValuesError(Exception):
    def __init__(self):
        self.__msg = 'Данные не валидны!'

    def __call__(self, *args, **kwargs):
        print(self.__msg)


class EmptyDBError(Exception):
    pass
