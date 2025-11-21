from django.contrib import admin
from .models import movie,favoriteList
# Register your models here.
admin.site.register((movie,favoriteList))