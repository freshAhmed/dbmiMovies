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
#  log.info(title)
 if title:
  data=make_request(os.environ.get('END_POINT'),
                   {'r':'json',
                    't':title,
                    'page':50})
  context['jsondata']=json.dumps(data) if data.get('Response')=='True' else None

 if data.get('Response')=='True':   
  context['favoriteList']=True if (len(movie.objects.filter(Q(title=str(data.get('Title')).lower())
                                                           |Q(title=str(data.get('Title').upper()))))==1) else False

 return render(request,'movie_detaile.html',context)

def add_movie_favorite_list(request,*args,**kwargs):
 context={}


 data=eval(request.POST.get('data'))
 context['jsondata']=json.dumps(data)
 
 if len(movie.objects.filter(Q(title=str(data.get('Title')).lower())|
                                                           Q(title=str(data.get('Title').upper()))))==0:
  obj=movie.objects.create(title=data.get('Title'),
                           type=data.get('Type'),
                           released=data.get('Released'),
                           poster=data.get('Poster'),
                           genre=data.get('Genre'),
                           year=data.get('Year'),
                           plot=data.get('Plot'),
                           writer=data.get('Writer')) 
  context['favoriteList']=True 

  obj.save()

 return render(request,'response_api/remove_btn_favoriteList.html',context)
  



def remove_movie_favorite_list(request,*args,**kwargs):
 context={}
 if request.method=='POST':
  data=eval(request.POST.get('data'))
  obj=movie.objects.filter(Q(title=data.get("Title").lower())| Q(title=data.get("Title").upper()))
  obj.delete()
  context['favoriteList']=False
  context['jsondata']=None 
 return render(request,'movie_detaile.html',context)


def home_view(request,*args,**kwargs):
 context={}  
 return render(request,'base.html',context)
 

def movie_detaile_view(request,*args,**kwargs):
 
 render(request,'movie_detaile.html',{})