import functools
from django.shortcuts import redirect
from django.contrib import messages
from .models import Pc_user


def pc_is_authenticated(view_func, redirect_url="prn:pc_login"):
    """
        this decorator ensures that a pc user is logged in,
        if a pc user is logged in, the user will get redirected to 
        the url whose view name was passed to the redirect_url parameter
    """
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        print("hahahahahahahahah")
        print(request.session.__dict__)
        try:
          post_pcIdentifier=request.session["identifier"]
          pc=Pc_user.objects.get(pcIdentifier=post_pcIdentifier)
          print("sdaaaaaaaaaaaaaaaaaaa")
          print(pc.pcIdentifier)
          print("sdaaaaaaaaaaaaaaaaaaa")
          return view_func(request,*args, **kwargs)
        except:
          messages.info(request, "You need to be logged in")
          print("You need to be logged out")
          return redirect(redirect_url)
    return wrapper