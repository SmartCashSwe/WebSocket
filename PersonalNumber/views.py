from django.shortcuts import render

# Create your views here.

# Create your views here.
def index(request):
    return render(request, "personalnumber/index.html")

def room(request, room_name):
    return render(request, "personalnumber/room.html", {"room_name": room_name})

def pcRoom(request, room_name):
    return render(request, "personalnumber/pcRoom.html", {"room_name": room_name})
