"""
urls.py
This script navigates the request to the View depending on the route requested
"""
from . import views
from django.urls import path, re_path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter

admin.autodiscover()
# set up rest router, urls for CRUD operations
router = DefaultRouter()
router.register(r'', views.MovieViewSet, basename='movies')

urlpatterns = [
    path('', include(router.urls)),
    re_path(r'^find', views.FindMovieView.as_view(), name='find'),
    re_path(r'^search', views.AdvancedSearchView.as_view(), name='search')
]
