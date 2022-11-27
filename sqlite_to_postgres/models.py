import attr
import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Id:
    id: uuid


@dataclass
class Time(Id):
    created_at: datetime
    updated_at: datetime


@dataclass
class Movie(Time):
    title: str
    description: str
    creation_date: datetime
    file_path: str
    rating: float
    type: str


@dataclass(kw_only=True)
class Genre(Time):
    name: str
    description: Optional[str] = None


@dataclass
class GenreFilmwork(Id):
    film_work: uuid
    genre: uuid
    created_at: datetime


@dataclass
class Person(Time):
    full_name: str


@dataclass
class PersonFilmwork(Id):
    film_work: uuid
    person: uuid
    role: str
    created_at: datetime


TABLES = {
    'film_work': Movie,
    'genre': Genre,
    'genre_film_work': GenreFilmwork,
    'person': Person,
    'person_film_work': PersonFilmwork
}
