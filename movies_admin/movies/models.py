"""Django модели"""

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedMixin, UUIDMixin


class Genre(TimeStampedMixin):
    name = models.CharField(max_length=255)
    description = models.TextField(
        # blank=True,
        null=True,
    )

    class Meta:
        db_table = 'content\".\"genre'
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')


class Filmwork(TimeStampedMixin):

    class Type(models.TextChoices):
        MOVIE = 'Movie', _('movie')
        TV_SHOW = 'TV Show', _('tv show')

    title = models.TextField(
        verbose_name=_('title'),
        max_length=255,
    )
    description = models.TextField(
        verbose_name=_('description'),
        max_length=255,
        null=True,
    )
    creation_date = models.DateField(
        verbose_name=_('creation_date'),
        null=True,
        auto_created=True,
    )
    file_path = models.FileField(
        verbose_name=_('image'),
        upload_to='movies/',
        blank=True,
        null=True,
    )
    rating = models.FloatField(
        verbose_name=_('rating'),
        blank=True,
        null=True,
        validators=(
            MinValueValidator(0),
            MaxValueValidator(100),
        ),
    )
    type = models.CharField(
        verbose_name=_('type'),
        max_length=255,
        choices=Type.choices,
    )
    genres = models.ManyToManyField(
        Genre,
        through='GenreFilmwork',
    )
    persons = models.ManyToManyField(
        'Person',
        through='PersonFilmwork',
    )

    class Meta:
        db_table = 'content\".\"film_work'
        verbose_name = _('Filmwork')
        verbose_name_plural = _('Filmworks')


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey(
        Filmwork,
        on_delete=models.CASCADE,
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content\".\"genre_film_work'


class Person(TimeStampedMixin):

    full_name = models.CharField(
        verbose_name=_('full name'),
        max_length=255,
    )

    class Meta:
        db_table = 'content\".\"person'
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')


class PersonFilmwork(UUIDMixin):

    class Role(models.TextChoices):
        ACTOR = 'actor', _('actor')
        PRODUCER = 'producer', _('producer')
        DIRECTOR = 'director', _('director')

    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
    )
    film_work = models.ForeignKey(
        Filmwork,
        on_delete=models.CASCADE,
    )
    role = models.CharField(
        max_length=255,
        choices=Role.choices,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content\".\"person_film_work'
        constraints = [
            models.UniqueConstraint(
                fields=('person', 'film_work', 'role'),
                name=_('Actor with this Role was added to this Filmwork'),
            ),
        ]
