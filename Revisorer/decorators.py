import functools
from django.shortcuts import redirect, HttpResponse
from django.contrib import messages
from .models import Revisor
from django.contrib.sessions.models import Session


def revisor_is_authenticated(view_func, redirect_url="kasa:pc_login"):
    """
        this decorator ensures that a pc user is logged in,
        if a pc user is logged in, the user will get redirected to 
        the url whose view name was passed to the redirect_url parameter
    """
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:

          user=Session.objects.get(session_key=request.session.session_key)
          post_username=request.session["email"]
          post_password=request.session["password"]

          pc=Revisor.objects.get(email=post_username, password=post_password)
          return view_func(request,*args, **kwargs)
        except:
          messages.info(request, "You need to be logged in")
          return HttpResponse(status=401)
    return wrapper