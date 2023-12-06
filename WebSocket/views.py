from django.shortcuts import render
from .models import KasaSoftware
from django.http import HttpRequest, HttpResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
import json
@csrf_exempt
def get_latest_software(request:HttpRequest):
    if request.method=="POST":
      last=KasaSoftware.objects.latest("id")
      return HttpResponse(json.dumps({"pk":last.pk}))
    elif request.method=="GET":
       return HttpResponse(200)

@csrf_exempt
def get_enox(request:HttpRequest):
   if request.method=="GET":
      last=KasaSoftware.objects.latest("id")
      the_file=last.file
      return FileResponse(the_file)
# Create your views here.
