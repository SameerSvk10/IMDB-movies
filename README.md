# IMDB-movies

REST APIs for movies.

Users can search for movies based on title, genres, IMDB rating, director, popularity.


Follow the instructions to run project on local machine:
  - clone the repository to your machine
    - git clone https://github.com/SameerSvk10/IMDB-movies.git
  - pip install requirements.txt
  - python manage.py makemigrations
  - python manage.py migrate
  - python manage.py import_movies
  - python manage.py runserver
  
  open the link in your browser - http://127.0.0.1:8000/movies/
