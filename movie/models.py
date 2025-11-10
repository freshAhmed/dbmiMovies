from django.db import models

# Create your models here.



class movie(models.Model):
  title=models.TextField()
  poster=models.TextField()
  plot=models.TextField()
  released=models.TextField()
  writer=models.TextField()
  genre=models.TextField()
  type=models.CharField()
  year=models.CharField()