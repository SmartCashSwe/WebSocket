from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Pc_user, Mobile_user
# Create your views here.

# Create your views here.
def index(request):
    return render(request, "personalnumber/index.html")

def room(request, room_name):
    return render(request, "personalnumber/room.html", {"room_name": room_name})

def pcRoom(request, room_name):
    return render(request, "personalnumber/pcRoom.html", {"room_name": room_name})
@csrf_exempt
def log_in_pc(request):
    if request.method=="POST":
        try:
            post_identifier=request.POST["identifier"]
            identifier=Pc_user.objects.get(pcIdentifier=post_identifier)
        except:
            return HttpResponse(status=404)
        try:
            request.session["pcIdentifier"]=identifier.pcIdentifier
            request.session["mobile_users"]=identifier.mobile_users
            return redirect("prn:pcRoom")
        except:
            return HttpResponse (status=400)
    elif request.method=="GET":
        return render(request, "personalnumber/pcRoom.html")