"""
admin.py
This script register database models to Django admin dashboard
"""
from django.contrib import admin
from .models import Movie, Genre


class MovieAdmin(admin.ModelAdmin):
    """Ordering by imdb_score, filter by genre and search by name and director"""
    ordering = ["imdb_score"]
    list_display = ("name", "imdb_score")
    list_filter = ("genre",)
    search_fields = ["name", "director"]


admin.site.register(Movie, MovieAdmin)
admin.site.register(Genre)
