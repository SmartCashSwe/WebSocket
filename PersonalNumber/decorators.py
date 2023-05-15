import functools
from django.shortcuts import redirect
from django.contrib import messages
from .models import Pc_user,Mobile_user
from django.contrib.sessions.models import Session


def pc_is_authenticated(view_func, redirect_url="prn:pc_login"):
    """
        this decorator ensures that a pc user is logged in,
        if a pc user is logged in, the user will get redirected to 
        the url whose view name was passed to the redirect_url parameter
    """
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
          user=Session.objects.get(session_key=request.session.session_key)
          post_username=request.session["username"]
          
          pc=Pc_user.objects.get(username=post_username)
          return view_func(request,*args, **kwargs)
        except:
          messages.info(request, "You need to be logged in")
          return redirect(redirect_url)
    return wrapper

    
def mobile_is_authenticated(view_func, redirect_url="prn:mobile_login"):
    """
        this decorator ensures that a pc user is logged in,
        if a pc user is logged in, the user will get redirected to 
        the url whose view name was passed to the redirect_url parameter
    """
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
          print("request.session")
          print(request.session)
          print("request.session")
          user=Session.objects.get(session_key=request.session.session_key)
          post_mobileIdentifier=request.session["personal_number"]
          
          pc=Mobile_user.objects.get(personal_number=post_mobileIdentifier)
          return view_func(request,*args, **kwargs)
        except:
          messages.info(request, "You need to be logged in")
          return redirect(redirect_url)
    return wrapper