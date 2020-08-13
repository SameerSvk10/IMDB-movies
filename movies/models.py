"""
models.py
This script defines our data models
"""
from django.db import models
from django.core.validators import MaxValueValidator, DecimalValidator, MinValueValidator
from decimal import Decimal


class Genre(models.Model):
    """
    Model for Genres
    fields :
        name - varchar
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    """
    Model for Movie
    fields :
        name - varchar
        imdb_score - Decimal 0 to 10
        director - varchar
        popularity - Decimal 0 to 99
        genre - List of Genre Object - Many to Many field
    """
    name = models.CharField(max_length=200)
    imdb_score = models.DecimalField(max_digits=3, decimal_places=1,
                                     validators=[MaxValueValidator(10), DecimalValidator(3, 1),
                                                 MinValueValidator(Decimal('0.0'))])
    director = models.CharField(max_length=200)
    popularity = models.DecimalField(max_digits=3, decimal_places=1,
                                     validators=[MaxValueValidator(99), DecimalValidator(3, 1),
                                                 MinValueValidator(Decimal('0.0'))])
    genre = models.ManyToManyField(Genre)

    def __str__(self):
        return self.name
