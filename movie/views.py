from django.shortcuts import render,redirect
import logging
import os
import requests
import pprint
from .models import movie as movie_model ,favoriteList
from django.db.models import Q
from django.contrib.auth.decorators import login_required
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
#  log.info(favoriteList)
 if len(title)>0:
  data=make_request(os.environ.get('END_POINT'),
                   {'r':'json',
                    't':title,
                    'page':50})
  
  context['jsondata']=json.dumps(data) if data.get('Response')=='True' else None
  if data.get('Response')=='True':   
   user=request.user if request.user.is_authenticated else None
   favlist=favoriteList.objects.filter(author=user)
   favlist= favlist[0] if len(favlist)>0 else None
   movielist=movie_model.objects.filter((Q(Title=str(data.get('Title')))
                                        |Q(Title=str(data.get('Title')).lower())
                                        |Q(Title=str(data.get('Title')).upper()))
                                        &(Q(favoritelist=favlist)))
   log.info(movielist)
   movie=movielist[0] if len(movielist) >0 else None
   
   context['is_in_favoriteList']=True if movie else False
 
  return render(request,'movie_detaile.html',context)
 return favoriteList_view(request)

@login_required
def addMovieFavoriteList(request,*args,**kwargs):
 context={}

 if request.method=='POST':
  data=eval(request.POST.get('data'))
  context['jsondata']=json.dumps(data)
  movies=movie_model.objects.filter((Q(Title=str(data.get("Title")))
                            |Q(Title=str(data.get('Title')).lower())
                            |Q(Title=str(data.get('Title')).upper())))
  favlist=favoriteList.objects.filter(Q(author=request.user))[0] 
  obj=movies[0] if len(movies)>0 else None
  if len(movies)==0:
   obj=movie_model.objects.create(Title=data.get('Title'),
                           Type=data.get('Type'),
                           Released=data.get('Released'),
                           Poster=data.get('Poster'),
                           Genre=data.get('Genre'),
                           Year=data.get('Year'),
                           Plot=data.get('Plot'),
                           Writer=data.get('Writer')) 
   obj.save()
  obj.favoritelist.add(favlist) if favlist in obj.favoritelist.all() else None
  context['is_in_favoriteList']=True 
  return render(request,'response_api/remove_btn_favoriteList.html',context)
 else :
  return redirect('/favoriteList/')
 

@login_required
def removeMovieFavoriteList(request,*args,**kwargs):
 context={}
 if request.method=='POST':
  data=eval(request.POST.get('data'))
  user=request.user if request.user.is_authenticated else None
  favlist=favoriteList.objects.filter(Q(author=user))[0] 
  movie=movie_model.objects.filter(
                          Q(Title=data.get('Title'))
                         |Q(Title=data.get("Title").lower())
                         |Q(Title=data.get("Title").upper()))
  movie=movie.filter(Q(favoritelist=favlist))
  if len(movie)>0:
   movie=movie[0]
   if movie.favoritelist.count()>0:
    movie.favoritelist.remove(favlist)
   else :
    movie.delete()
  context['is_in_favoriteList']=False
  context['jsondata']=None 
 return favoriteList_view(request)

def home_view(request,*args,**kwargs):
 context={}  
 return render(request,'base.html',context)
@login_required
def favoriteList_view(request,*args,**kwargs):
 user=request.user if request.user.is_authenticated else None
 favoritelist=favoriteList.objects.filter(author=user)[0] 
 movies= movie_model.objects.filter(Q(favoritelist=favoritelist))
 return render(request,'favoriteList.html',{'favoriteList':list(movies)})


def movieDetails(request,Title,*args,**kwargs):
 context={}
 movies=movie_model.objects.filter(Q(Title=Title)|
                          Q(Title=str(Title).lower()) |
                          Q(Title=str(Title).upper()))
 context['jsondata']=json.dumps(movies[0].get_data())
 context['is_in_favoriteList']=True if len(movies)>0 else False
 return render(request,'movie_detaile.html',context)
