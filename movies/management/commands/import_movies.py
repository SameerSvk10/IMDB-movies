"""
import_movies.py
This script provides a way to execute custom admin commands - import movies from a json dump
This custom command will fill up Movie database table with data from imdb.json file
To run :
    python manage.py import_movies
"""
from ...models import Movie, Genre
from django.core.management.base import BaseCommand, CommandError

from pathlib import Path
import json

parent_directory = str(Path().resolve().parent)


class Command(BaseCommand):
    help = 'Imports Movies from json dump into Movie table'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        input_file = 'movies/data/imdb.json'
        with open(input_file, 'r') as f:
            raw_data = f.read()
            movies = json.loads(raw_data)
            for each_movie in movies:
                try:
                    movie, created = Movie.objects.get_or_create(name=each_movie.get('name'),
                                                                 imdb_score=each_movie.get('imdb_score'),
                                                                 director=each_movie.get('director'),
                                                                 popularity=each_movie.get('99popularity'))
                    genre_list = each_movie.get('genre')
                    genre_objects = []
                    for name in genre_list:
                        name = name.strip()
                        genre, created = Genre.objects.get_or_create(name=name)
                        genre_objects.append(genre)
                    movie.genre.add(*genre_objects)
                    movie.save()
                except Exception as e:
                    raise CommandError(
                        'Movie {} cannot be added because of the following error {}'.format(each_movie.get('name'),
                                                                                            str(e)))
