from django.shortcuts import render,redirect
import logging
import os
import requests
import pprint
from .models import movie
from django.db.models import Q
import json
log=logging.getLogger(__name__)

def make_request(url=os.environ.get("END_POINT"),params={'r':'json','t':'','page':1}):
 API_KEY= os.environ.get('Omdb_API_KEY')
 END_POINT=url.format(API_KEY)
 response=requests.get(END_POINT,params)
 return response.json() 

def search_view(request,*args,**kwargs):
 context={'data':None}
 title=request.GET.get('query')
 log.info(len(title))
 if len(title)>0:
  data=make_request(os.environ.get('END_POINT'),
                   {'r':'json',
                    't':title,
                    'page':50})
#   log.info((data,True))
  context['jsondata']=json.dumps(data) if data.get('Response')=='True' else None
  if data.get('Response')=='True':   
   context['is_in_favoriteList']=True if (len(movie.objects.filter(Q(Title=str(data.get('Title')))
                                                           |Q(Title=str(data.get('Title')).lower())
                                                           |Q(Title=str(data.get('Title')).upper())))==1) else False
 
  return render(request,'movie_detaile.html',context)
 return favoriteList_view(request)
def addMovieFavoriteList(request,*args,**kwargs):
 context={}

 if request.method=='POST':
  data=eval(request.POST.get('data'))
  context['jsondata']=json.dumps(data)
 
  if len(movie.objects.filter(Q(Title=str(data.get("Title")))
                            |Q(Title=str(data.get('Title')).lower())
                            |Q(Title=str(data.get('Title')).upper())))==0:
   obj=movie.objects.create(Title=data.get('Title'),
                           Type=data.get('Type'),
                           Released=data.get('Released'),
                           Poster=data.get('Poster'),
                           Genre=data.get('Genre'),
                           Year=data.get('Year'),
                           Plot=data.get('Plot'),
                           Writer=data.get('Writer')) 
   context['is_in_favoriteList']=True 

   obj.save()

   return render(request,'response_api/remove_btn_favoriteList.html',context)
  
 else :
  return redirect('/')

def removeMovieFavoriteList(request,*args,**kwargs):
 context={}
 if request.method=='POST':
  data=eval(request.POST.get('data'))
  obj=movie.objects.filter(
                          Q(Title=data.get('Title'))
                         |Q(Title=data.get("Title").lower())
                         |Q(Title=data.get("Title").upper()))
  obj.delete()
  context['is_in_favoriteList']=False
  context['jsondata']=None 
 return favoriteList_view(request)

def home_view(request,*args,**kwargs):
 context={}  
 return render(request,'base.html',context)

def favoriteList_view(request,*args,**kwargs):
 favoriteList=movie.objects.all()
 return render(request,'favoriteList.html',{'favoriteList':favoriteList})

def movieDetails(request,Title,*args,**kwargs):
 context={}
 movies=movie.objects.filter(Q(Title=Title)|
                          Q(Title=str(Title).lower()) |
                          Q(Title=str(Title).upper()))
 context['jsondata']=json.dumps(movies[0].get_data())
 context['is_in_favoriteList']=True if len(movies)>0 else False
 return render(request,'movie_detaile.html',context)
