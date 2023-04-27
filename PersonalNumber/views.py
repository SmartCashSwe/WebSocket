from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Pc_user, Mobile_user
from .decorators import pc_is_authenticated, mobile_is_authenticated
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from core.settings import ARGON_HASH_PARALLELISM, ARGON_HASH_ROUNDS, ARGON_HASH_SALT
from django.contrib.auth.hashers import  make_password

# Create your views here.
import json
# Create your views here.
def index(request):
    return render(request, "personalnumber/index.html")

@mobile_is_authenticated
def room(request, room_name):

    return render(request, "personalnumber/room.html", {"room_name": room_name})

@pc_is_authenticated
def pcRoom(request, room_name):
    mobile_users=json.loads(request.session["mobile_users"])
    print("mobile_users")
    print(mobile_users)
    print("mobile_users")
    return render(request, "personalnumber/pcRoom.html", {"room_name": room_name, "mobile_users":mobile_users })


@csrf_exempt
def log_in_pc(request):
    if request.method=="POST":
        try:
            print(1)
            # data = json.loads(request.body)
            print(2)
            post_identifier = request.POST['identifier']
            print(3)
    
            identifier=Pc_user.objects.get(pcIdentifier=post_identifier)
            print(4)
        except:
            return HttpResponse(status=404)
        try:
            request.session.set_expiry(0)
            request.session.set_test_cookie()
            request.session["pcIdentifier"]=str( identifier.pcIdentifier)
            request.session["mobile_users"]=json.dumps(identifier.mobile_users)
            request.session.modified=True
            json_string=json.dumps({"pcIdentifier":identifier.pcIdentifier, "mobile_users":identifier.mobile_users})
            print("hahahahahahahahahahah")
            json_token=make_password(password= json_string, salt=ARGON_HASH_SALT)
            print(json_token)
            # request.session.save()
            return HttpResponse(json_token)
        except Exception as e:
            print(e)
            return HttpResponse (status=400)
    elif request.method=="GET":
        return render(request, "personalnumber/pc_login.html")

def log_out_pc(request):
    if request.method=="POST":
        request.session.flush()
        return redirect("prn:pc_login")

@csrf_exempt
def log_in_mobile(request):
    if request.method=="POST":
        try:
        
            data = json.loads(request.body)
            post_identifier = data.get('personal_number')
    
            identifier=Mobile_user.objects.get(personal_number=post_identifier)
        except:
            return HttpResponse(status=404)
        try:
            request.session.set_expiry(0)
            request.session.set_test_cookie()
            request.session["reciever"]=str( data.get('identifier'))
            request.session["personal_number"]=identifier.personal_number
            request.session.modified=True
            # request.session.save()
            return HttpResponse(status=200)
        except:
            return HttpResponse (status=400)
    elif request.method=="GET":
        return render(request, "personalnumber/mobile_login.html")