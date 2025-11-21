from django.shortcuts import render ,redirect
from django.contrib.auth import login ,authenticate,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import logging
from movie.models import favoriteList
log=logging.getLogger(__name__)
# Create your views here.

def login_view(request,*args,**kwargs):
    context={}
    if request.method=="POST":
     username=request.POST.get('username')
     password=request.POST.get('password')
     user=authenticate(username=username,password=password)
     if user is not None:
        login(request,user)
        return redirect('/favoriteList/')
     else:
        context['message']='error the username and password invalid try agin'
    return render(request,'accounts/login.html',{})
    

def logout_view(request,*args,**kwargs):

 if request.user is not None:
  logout(request)
  if 'next'in request.GET:
   next_url=request.GET.get('next')
   return redirect(next_url)
  
 return render(request,'accounts/login.html',{})
    

def register_view(request,*args,**kwargs):
    form =UserCreationForm(request.POST or None)
    context={
      'form':form
    } 
    if form.is_valid():
      data=form.clean()
      form.save()
      user=User.objects.filter(username=data['username'])
      favlist=favoriteList(author=user[0])
      favlist.save()
      context['form']=UserCreationForm()
      return redirect('/login/')
    return render(request,'accounts/register.html',context)