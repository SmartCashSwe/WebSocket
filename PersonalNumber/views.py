from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import  Mobile_user
from .decorators import  mobile_is_authenticated
from KasaRegister.decorators import pc_is_authenticated
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from core.settings import ARGON_HASH_PARALLELISM, ARGON_HASH_ROUNDS, ARGON_HASH_SALT
from django.contrib.auth.hashers import  make_password
from KasaRegister.models import KasaUser, Licence
from django.http import HttpRequest
import json
from KasaRegister.src.auth.auth import requestHandler
# Create your views here.


def index(request):
    return render(request, "personalnumber/index.html")

@mobile_is_authenticated
def room(request:HttpRequest, room_name):
    session=request.session.session_key
    return render(request, "personalnumber/room.html", {"room_name": room_name,"session_key":session})


def get_kasa_list(prn):
    _all=KasaUser.objects.all()
    arr=[]
    k=[]

    for _user in _all:
        arr.append(_user.prn) 
    for item in arr:

        try:
            i:dict=json.loads(item)
            if prn in i.keys():
                u=KasaUser.objects.get(prn=item)
                cert=u.licence
                k.append({"username":u.username,"company_name":u.company_name, "org_nummer":u.org_num})
        except:
            pass
    return k
 

@csrf_exempt
def choose_kasa(request:HttpRequest):
    try:
        _pn=request.session["personal_number"]
        _user=Mobile_user.objects.get(personal_number=_pn)
    except:
        return HttpResponse(status=401)
    if request.method=="GET":
        try:
            kasa_list=get_kasa_list(prn=_pn)
            json_kasa_list={"kasalist":kasa_list}
            return render(request,"personalnumber/mobile_choose.html", context=json_kasa_list)
        except:
            return HttpResponse(500)
    elif request.method=="POST":
        try:
            data = json.loads(request.body)
            receiver = data.get('receivers')
        except Exception as e:
            return HttpResponse(status=400)
        try:
            json_receivers=json.loads(receiver)
        except:
            return HttpRequest(status=400)
        try:
            users=[]
            for item in json_receivers:
                print("kasa_userkasa_userkasa_userkasa_userkasa_userkasa_userkasa_user")
                print(item)
                kasa_user=KasaUser.objects.get(username=item)
                print("kasa_userkasa_userkasa_userkasa_userkasa_userkasa_userkasa_user")
                users.append(kasa_user.username)
            print("endendendendendendend")
            print(users)
            print("endendendendendendend")
        except Exception as e:
            return HttpResponse(status=403)
        request.session["receiver"]=json.dumps(users)
        request.session.save()
        return HttpResponse(status=200)


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
            # request.session["receiver"]=str( data.get('identifier'))
            request.session["personal_number"]=identifier.personal_number
            request.session.modified=True
            # request.session.save()
            return HttpResponse(status=200)
        except:
            return HttpResponse (status=400)
    elif request.method=="GET":
        return render(request, "personalnumber/mobile_login.html")


@csrf_exempt
@mobile_is_authenticated
def get_company(request):
    if request.method=="POST":
        req=requestHandler.extractRequest(request)
        _username=request.session["personal_number"]
        _password=request.session["password"]
        try:
            _user=Mobile_user.objects.get(personal_number=_username , password=_password)
        except:
            return HttpResponse(status=404)
        _orgnummer      = _user.org_num
        _adress         = json.loads(_user.adress)
        _company_name   = _user.company_name
        theObj = {"orgnummer":_orgnummer, "adress":_adress,"company_name":_company_name}
        return HttpResponse(json.dumps(theObj))


@csrf_exempt
@mobile_is_authenticated
def phone_getNotifications(request):

    if(request.method == "GET"):
        req=requestHandler.extractRequest(request)
        _username=request.session["personal_number"]
        _password=request.session["password"]
        try:
            the_user=Mobile_user.objects.get(personal_number=_username , password=_password)
        except:
            return HttpResponse(status=404)
        notiser=the_user.notifications
        the_user.notifications="[]"
        the_user.save()
        return HttpResponse(notiser.replace("'",'"').replace("[","{").replace("]","}"))
    return HttpResponse(403)


@csrf_exempt
@mobile_is_authenticated
def send_to_mobile(request:HttpRequest):

    if request.method =="POST":
        try:
            the_user=request.session["username"]
            p=request.session["password"]
            user=Mobile_user.objects.get(username=the_user, password=p)
        except:
            return HttpResponse(status=404)
        try:
            _kassor=json.loads(request.session["receiver"])
            kasa_list=KasaUser.objects.filter(username__in=_kassor)
            data=[]
            _user:KasaUser
            for _user in kasa_list:
                data.append(_user.all_products)
            _json=json.dumps(data)
            return HttpResponse( _json)
        except:
            return HttpResponse(500)


@csrf_exempt
@mobile_is_authenticated
def get_x_rapport(request):
    if request.method=="POST":
        try:
            the_user=request.session["username"]
            p=request.session["password"]
            user=Mobile_user.objects.get(username=the_user, password=p)
        except:
            return HttpResponse(status=404)
        try:
            _kassor=json.loads(request.session["receiver"])
            kasa_list=KasaUser.objects.filter(username__in=_kassor)
            data={}
            _user:KasaUser
            for _user in kasa_list:
                data[_user.username]=(_user.all_products)
            x_rapport=json.dumps(data)
            return HttpResponse(x_rapport)
        except:
            return HttpResponse(status=204)


@csrf_exempt
@mobile_is_authenticated
def get_z(request):
    if request.method=="POST":
        try:
            the_user=request.session["username"]
            p=request.session["password"]
            user=Mobile_user.objects.get(username=the_user, password=p)
        except:
            return HttpResponse(status=404)
        try:
            _kassor=json.loads(request.session["receiver"])
            kasa_list=KasaUser.objects.filter(username__in=_kassor)
        except:
            return HttpResponse(status=401)
        prn=request.session["prn"]
        data={}
        _user:KasaUser
        for _user in kasa_list:
            data[_user.username]=(_user.z_rapport)
        return HttpResponse(json.dumps(data))


@csrf_exempt
@mobile_is_authenticated
def update_huvudgrupp(request):
    if request.method=="POST":
        _req=requestHandler.extractRequest(request)
        new_item=_req["item"]
        old_item=_req["old_item"]
        # _list:list=_user.kassa_list["UppdateraHuvudgrupp"]
        # _list.index(old_item)
        _list:list=_user.kassa_list["UppdateraHuvudgrupp"]
        _list.append(new_item)
        _user.kasa_send=_list
        
        _huvudgrupper:list=_user.huvudgrupper
        _index=_huvudgrupper.index(old_item)
        _huvudgrupper[_index]=new_item
        _user.huvudgrupper=_huvudgrupper
        
        _user.save()
        return HttpResponse(status=200)
        

@csrf_exempt
@mobile_is_authenticated
def update_artikel(request):
    if request.method=="POST":
        _req=requestHandler.extractRequest(request)
        new_item=_req["item"]
        old_item=_req["old_item"]
        # _list:list=_user.kassa_list["UppdateraHuvudgrupp"]
        # _list.index(old_item)
        _list:list=_user.kassa_list["UppdateraArtikel"]
        _list.append(new_item)
        _user.kasa_send=_list
        
        artiklar:list=_user.all_products
        _index=artiklar.index(old_item)
        artiklar[_index]=new_item
        _user.all_products=artiklar
        _user.save()
        return HttpResponse(status=200)


@csrf_exempt
@mobile_is_authenticated
def laggTill_artikel(request):
    if request.method=="POST":
        _req=requestHandler.extractRequest(request)
        new_item=_req["item"]
        # _list:list=_user.kassa_list["UppdateraHuvudgrupp"]
        # _list.index(old_item)
        _list:list=_user.kassa_list["LäggTillArtikel"]
        _list.append(new_item)
        _user.kasa_send=_list
        
        artiklar:list=_user.all_products
        artiklar.append(new_item)
        _user.all_products=artiklar
        _user.save()
        return HttpResponse(status=200)


@csrf_exempt
@mobile_is_authenticated
def laggTill_huvudgrupp(request):
    if request.method=="POST":
        _req=requestHandler.extractRequest(request)
        new_item=_req["item"]
        # _list:list=_user.kassa_list["UppdateraHuvudgrupp"]
        # _list.index(old_item)
        _list:list=_user.kassa_list["LäggTillHuvudgrupp"]
        _list.append(new_item)
        _user.kasa_send=_list
        
        artiklar:list=_user.huvudgrupper
        artiklar.append(new_item)
        _user.huvudgrupper=artiklar
        _user.save()
        return HttpResponse(status=200)