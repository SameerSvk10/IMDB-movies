"""
views.py
This script includes all the views of the app
"""
from .models import Movie

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from .serializers import MovieSerializer

from decimal import Decimal


class StandardResultsSetPagination(PageNumberPagination):
    """
    Adding the pagination style, number of results per page
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 120


class MovieViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Movie instances.
    This ViewSet will handle list, create, retrieve, update, destroy, partial_update actions
    list, retrieve is accessible to all the users
    All other actions requires admin credentials
    """
    queryset = Movie.objects.all().order_by('imdb_score')
    serializer_class = MovieSerializer
    authentication_classes = [BasicAuthentication]
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['retrieve', "list"]:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]


class FindMovieView(APIView):
    """
    API endpoint that allows users to find movies by query.
    This API search for the query term in title, director, genre
    """
    serializer_class = MovieSerializer

    def get(self, request):
        offset = request.query_params.get('offset', 0)
        count = request.query_params.get('count', 20)
        queryset = Movie.objects.all()
        query = request.query_params.get('q', None)
        query_type = request.query_params.get('query_type', None)
        if query:
            if query_type is None:
                name_queryset = queryset.filter(name__icontains=query)[offset:count]
                director_queryset = queryset.filter(director__icontains=query)[offset:count]
                genre_queryset = queryset.filter(genre__name__icontains=query)[offset:count]

                response = {"titles": self.serializer_class(name_queryset, many=True).data,
                            "directors": self.serializer_class(director_queryset, many=True).data,
                            "genres": self.serializer_class(genre_queryset, many=True).data}
                return Response(response)
            else:
                filter_mapping = {"titles": "name__icontains",
                                  "directors": "director__icontains",
                                  "genres": "genre__name__icontains"}
                queryset = queryset.filter(**{filter_mapping[query_type]: query})
        movies_serializer = self.serializer_class(queryset[offset:count], many=True)
        return Response(movies_serializer.data)


class AdvancedSearchView(APIView):
    """
    API endpoint that allows users to search for movies using filters such as genre, imdb score, popularity
    and search for title and director
    """
    serializer_class = MovieSerializer

    def get(self, request):
        offset = request.query_params.get('offset', 0)
        count = request.query_params.get('count', 20)
        title = request.query_params.get('title')
        director = request.query_params.get("director")
        genres = request.query_params.get('genres')
        imdb_score = request.query_params.get("imdb_score")
        popularity = request.query_params.get("popularity")

        queryset = Movie.objects.all()

        if title:
            queryset = queryset.filter(name__icontains=title)

        if director:
            queryset = queryset.filter(director__icontains=director)

        if genres:
            genres = genres.split(",")
            queryset = queryset.filter(genre__name__in=genres)

        if imdb_score:
            min_score, max_score = imdb_score.split(",")
            queryset = queryset.filter(imdb_score__gte=Decimal(min_score), imdb_score__lte=Decimal(max_score))

        if popularity:
            min_popularity, max_popularity = popularity.split(",")
            queryset = queryset.filter(popularity__gte=Decimal(min_popularity), popularity__lte=Decimal(max_popularity))

        movies_serializer = self.serializer_class(queryset[offset:count], many=True)
        return Response(movies_serializer.data)
