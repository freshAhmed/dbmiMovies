from django.urls import path
from .views import (addMovieFavoriteList,removeMovieFavoriteList,movieDetails)
urlpatterns=[
 path('add/',addMovieFavoriteList),
 path('remove/',removeMovieFavoriteList),
 path('<str:Title>/',movieDetails)
 ]
