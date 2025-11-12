from django.db import models

# Create your models here.



class movie(models.Model):
  Title=models.TextField()
  Poster=models.TextField()
  Plot=models.TextField()
  Released=models.TextField()
  Writer=models.TextField()
  Genre=models.TextField()
  Type=models.CharField()
  Year=models.CharField()
 
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
