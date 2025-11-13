from django.shortcuts import render ,redirect
from django.contrib.auth import login ,authenticate,logout
import logging

log=logging.getLogger(__name__)
# Create your views here.

def login_view(request,*args,**kwargs):
  
    if request.method=="POST":
     username=request.POST.get('username')
     password=request.POST.get('password')
     user=authenticate(username=username,password=password)
     
     if user is not None:
        login(request,user)
        return redirect('/favoriteList/')
     else:
        log.info('account is not authenticate')

    return render(request,'accounts/login.html',{})
    

def logout_view(request,*args,**kwargs):
    log.info(request.user.is_authenticated)
    if request.user is not None:
     logout(request)
     return render(request,'accounts/login.html',{})

def register_view(request,*args,**kwargs):
    return render(request,'accounts/register.html',{})