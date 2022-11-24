from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedMixin, UUIDMixin


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Filmwork(UUIDMixin, TimeStampedMixin):

    class Type(models.TextChoices):
        MOVIE = 'Film', "movie"
        TV_SHOW = "Serial", "q"

    title = models.TextField(max_length=255)
    description = models.TextField(max_length=255)
    creation_date = models.DateField(auto_created=True)
    rating = models.FloatField(
        blank=True,
        validators=(
            MinValueValidator(0),
            MaxValueValidator(100)
        ),
        verbose_name="рейтинг"
    )
    type = models.CharField(
        max_length=255,
        choices=Type.choices
    )
    genres = models.ManyToManyField(
        Genre,
        through="GenreFilmwork"
    )
    persons = models.ManyToManyField(
        'Person',
        through='PersonFilmwork'
    )

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey(
        Filmwork,
        on_delete=models.CASCADE,
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"


class Person(UUIDMixin, TimeStampedMixin):

    full_name = models.CharField(max_length=255)

    class Meta:
        db_table = "content\".\"person"


class PersonFilmwork(UUIDMixin):

    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE
    )
    film_work = models.ForeignKey(
        Filmwork,
        on_delete=models.CASCADE
    )
    role = models.CharField(
        max_length=255,
    )
    created = models.DateTimeField(auto_now_add=True,)

    class Meta:
        db_table = "content\".\"person_film_work"
