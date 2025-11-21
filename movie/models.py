from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class favoriteList(models.Model):
  author=models.OneToOneField(
    User,
    on_delete=models.CASCADE
  )

  def get_movies(self): 
   return movie.objects.filter(favoritelist=self)


class movie(models.Model):
  Title=models.TextField()
  Poster=models.TextField()
  Plot=models.TextField()
  Released=models.TextField()
  Writer=models.TextField()
  Genre=models.TextField()
  Type=models.CharField()
  Year=models.CharField()
  favoritelist=models.ManyToManyField(favoriteList) 
  def get_data(self):
   return{
     'Title':self.Title,
     'Poster':self.Poster,
     'Plot':self.Plot,
     'Released':self.Released,
     'Writer':self.Writer,
     'Genre':self.Genre,
     'Type':self.Type,
     'Year':self.Year,
   }
