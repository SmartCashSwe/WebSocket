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
def check_logged_in(request:HttpRequest):
    try:
        print(1)
        _email=request.session["email"]
        print(2)
        _password=request.session["password"]    
        print(3)
        
        
    except:
        return HttpResponse(status=401)
    try:
        print(4)
        _revisor=Revisor.objects.get(email=_email, password=_password)
        print(5)
    except:
        return HttpResponse(status=401)
    try:
        print(6)
        _kassa_list=_revisor.kasa_system.all()
    except Exception as e:
        return HttpResponse(204)
    try:
        print(7)
        user_1=_kassa_list[0].username
    except:
        return HttpResponse(204)
    try:
        print(8)
        session_kassa=request.session["KassaSystem"]
        print(9)
        if session_kassa =="":
            print(10)
            request.session["KassaSystem"]=  user_1
            print(11)
    except:
            request.session["KassaSystem"]=  user_1
    print(12)
    request.session.save()
    
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
        print(1)
        _revisor=Revisor.objects.get(email=_email, password=_password)
        print(2)
    except:
        return HttpResponse(status=401)
    try:
        print(3)
        _kassa_list=_revisor.kasa_system.all()
        print(4)
    except Exception as e:
        return HttpResponse(204)
    try:
        print(5)
        user_1=_kassa_list[0].username
        print(6)
    except:
        return HttpResponse(204)
    request.session["email"]=_email
    request.session["password"]=_password
    request.session["KassaSystem"]=  user_1
    print(8)
    request.session.save()
    print(9)
    
    return HttpResponse(status=200)


# @revisor_is_authenticated    
@csrf_exempt
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
        _chosen_kassa_id:str=None
        try:
            session_kassa=request.session["KassaSystem"]    
            _kassa_user=KasaUser.objects.get(username=session_kassa)
            _chosen_kassa_id=_kassa_user.pk
        except:
            None
        for item in _kassa_list:
            obj={"org_num":item.org_num, "company_name":item.company_name, "chosen":False}
            kassa_list_obj[item.org_num]=obj
            if (_chosen_kassa_id == item.pk):
                obj["chosen"]=True
        try:
            return JsonResponse({"kassa_list":kassa_list_obj,"mail":_revisor.email})
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
@csrf_exempt
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
            
        z_list=_kassa.z_rapport["items"]
        return JsonResponse({"items":z_list+ z_list+z_list+z_list+z_list+z_list+z_list+z_list+z_list+z_list+z_list+z_list})


@revisor_is_authenticated    
def z_rapport_sie4(request:HttpRequest):

    return HttpResponse(status=200)


@revisor_is_authenticated    
def z_rapport_pdf(request:HttpRequest):

    return HttpResponse(status=200)

@csrf_exempt
@revisor_is_authenticated    
def bokforing(request:HttpRequest):
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
        bokforing=_kassa.bokforing
        return JsonResponse(bokforing)
    elif request.method =="POST":
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
        _kassa_list=_kassa.kassa_list
        _kassa_bokforing=_kassa.bokforing
        _to_be_updated=[]
        _sent_bokforing=json.loads( request.POST["bokforing"])
        for item, val in _sent_bokforing.items():
            if _kassa_bokforing[item]!=val:
                _to_be_updated.append({item:val})
        print(_to_be_updated)
        if (len(_to_be_updated)>0):
            _kassa.bokforing=_sent_bokforing
        _kassa_list["UppdateraBokforing"]=_to_be_updated
        _kassa.kassa_list=_kassa_list
        _kassa.save()
        return HttpResponse(status=200)



@csrf_exempt
@revisor_is_authenticated    
def download_file(request:HttpRequest):
    if request.method =="POST":
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
        file=_kassa.download
        # _kassa.download.delete()
        # _kassa.save()
        return FileResponse(file)




