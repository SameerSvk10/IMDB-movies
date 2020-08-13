"""
serializers.py
This script provides way to serialize complex models into python datatypes that can be rendered to JSON objects for REST
API response
"""

from .models import Movie, Genre
from rest_framework import serializers


class GenreSerializer(serializers.ModelSerializer):
    """Serializer for Genre Model class"""

    class Meta:
        model = Genre
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    """Serializer for Movie Model class"""

    genre = GenreSerializer(many=True)

    class Meta:
        model = Movie
        fields = ('id', 'name', 'director', 'genre', 'imdb_score', 'popularity')

    def create(self, validated_data):
        """
        Nested serializers don't support create and update
        This method will handle saving multiple genres objects and mapping them to movie object
        :param validated_data: input data from API
        :return: Movie model object
        """
        new_movie = Movie(name=validated_data['name'],
                          imdb_score=validated_data['imdb_score'],
                          director=validated_data['director'],
                          popularity=validated_data['popularity'])
        new_movie.save()
        # add genres to the movie
        for genre in validated_data['genre']:
            genre_object, created = Genre.objects.get_or_create(name=genre["name"])
            new_movie.genre.add(genre_object)
        return new_movie

    def update(self, instance, validated_data):
        """
        Nested serializers don't support create and update
        This method will handle updating multiple genres objects and mapping them to movie object
        :param instance: instance of the previous Movie object
        :param validated_data: new data from API
        :return: updated instance of the Movie object
        """
        instance.name = validated_data.get('name', instance.name)
        instance.imdb_score = validated_data.get('imdb_score', instance.imdb_score)
        instance.popularity = validated_data.get('popularity', instance.popularity)
        instance.director = validated_data.get('director', instance.director)
        nested_genres = validated_data.pop('genre')
        # update genres to the movie
        instance.genre.set([])
        for genre in nested_genres:
            genre_object, created = Genre.objects.get_or_create(name=genre['name'])
            instance.genre.add(genre_object)
        instance.save()
        return instance
