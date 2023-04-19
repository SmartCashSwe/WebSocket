from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Pc_user, Mobile_user
from .decorators import pc_is_authenticated
# Create your views here.
import json
# Create your views here.
def index(request):
    return render(request, "personalnumber/index.html")

def room(request, room_name):
    return render(request, "personalnumber/room.html", {"room_name": room_name})

@pc_is_authenticated
def pcRoom(request, room_name):
    return render(request, "personalnumber/pcRoom.html", {"room_name": room_name})
@csrf_exempt
def log_in_pc(request):
    if request.method=="POST":
        print("hahahahah")
        try:
            # print(request.POST)
            data = json.loads(request.body)
            post_identifier = data.get('identifier')
    
            print(2)
            identifier=Pc_user.objects.get(pcIdentifier=post_identifier)
            print(3)
        except:
            print(4)
            return HttpResponse(status=404)
        try:
            print(5)
            request.session["pcIdentifier"]=identifier.pcIdentifier
            print(6)
            request.session["mobile_users"]=identifier.mobile_users
            request.session.modified=True
            request.session.save()
            print(request.session.__dict__)
            return HttpResponse(status=200)
        except:
            return HttpResponse (status=400)
    elif request.method=="GET":
        return render(request, "personalnumber/pc_login.html")