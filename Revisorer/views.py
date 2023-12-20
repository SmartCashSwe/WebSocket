from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, FileResponse, JsonResponse
from .decorators import revisor_is_authenticated
from .models import Revisor
from KasaRegister.models import KasaUser
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.
def log_in_admin(request:HttpRequest):

    return HttpResponse(status=200)

def log_out_admin(request:HttpRequest):

    return HttpResponse(status=200)


@csrf_exempt
def log_in_revisor(request:HttpRequest):
    try:
        print(request.POST)
        _email=request.POST["email"]
        print(_email)
        _password=request.POST["password"]
        print(_password)
        
    except:
        return HttpResponse(status=401)
    try:
        _revisor=Revisor.objects.get(email=_email, password=_password)
    except:
        return HttpResponse(status=401)
    try:
        _kassa_list=_revisor.kasa_system.all()
    except Exception as e:
        return HttpResponse(204)
    try:
        user_1=_kassa_list[0].username
    except:
        return HttpResponse(204)
    request.session["email"]=_email
    request.session["password"]=_password    
    request.session["KassaSystem"]=  user_1
    request.session.save()
    return HttpResponse(status=200)


@revisor_is_authenticated    
def log_out_revisor(request:HttpRequest):
    request.session.flush()
    return HttpResponse(status=200)


@revisor_is_authenticated    
@csrf_exempt
def choose_kassasystem(request:HttpRequest):
    if request.method=="GET":
        try:
            _email=request.session["email"]
            _password=request.session["password"]
        
        except:
            return HttpResponse(status=401)
        try:
            _revisor=Revisor.objects.get(email=_email, password=_password)
        except:
            return HttpResponse(status=401)
        try:
            _kassa_list=_revisor.kasa_system.all()
        except Exception as e:
            return HttpResponse(204)
        kassa_list_obj={}
        for item in _kassa_list:
            obj={"org_num":item.org_num, "company_name":item.company_name}
            kassa_list_obj[item.org_num]=obj
        try:
            return JsonResponse({"kassa_list":kassa_list_obj})
        except Exception as e:
            return HttpResponse(status=500)
    elif request.method=="POST":
        try:
            _email=request.session["email"]
            _password=request.session["password"]
        except:
            return HttpResponse(status=401)
        try:
            _revisor=Revisor.objects.get(email=_email, password=_password)
        except:
            return HttpResponse(status=401)
        try:
            _org_num=request.POST["org_num"]
            _kassa=request.POST["num"]
            _kassa=KasaUser.objects.get(id=_kassa, org_num=_org_num)
        except Exception as e:
            return HttpResponse(status=404)
        request.session["KassaSystem"]=_kassa.username
        request.session.save()
        return HttpResponse(status=200)




@revisor_is_authenticated    
def z_rapport_list(request:HttpRequest):
    if request.method=="GET":
        try:
            _email=request.session["email"]
            _password=request.session["password"]
            _revisor=Revisor.objects.get(email=_email, password=_password)
        except:
            return HttpResponse(status=401)
        try:
            _kassa_username=request.session["KassaSystem"]
            _kassa=KasaUser.objects.get(username=_kassa_username)
        except:
            return HttpResponse(status=404)
        z_list=_kassa.z_rapport

        return JsonResponse(z_list)


@revisor_is_authenticated    
def z_rapport_sie4(request:HttpRequest):

    return HttpResponse(status=200)


@revisor_is_authenticated    
def z_rapport_pdf(request:HttpRequest):

    return HttpResponse(status=200)


@revisor_is_authenticated    
def bokforing(request:HttpRequest):

    return HttpResponse(status=200)



