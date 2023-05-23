
from django.shortcuts import render,HttpResponse
from ast import literal_eval
from .models import KasaUser
import json
from django.http import JsonResponse, HttpRequest
import os
from core.settings import ARGON_HASH_SALT
import json
from django.contrib.auth.hashers import  make_password
from django.views.decorators.csrf import csrf_exempt
from .decorators import pc_is_authenticated
from .src.auth.auth import requestHandler
import secrets

json_ready=json.dumps({
	"sales": [],
	"user": "ali@smartcash.se",
	"lastId": "0",
	"kvitto": []
})


def kasa_signup(request):
    if(request.method == "POST"):
        req = requestHandler.extractRequest(request)
        cheker= False
        s=secrets.token_hex(32)
        all_kassaytr=KasaUser.objects.all()
        _username       = make_password( salt = ARGON_HASH_SALT, password=s)
        _orgnum         = req["org_num"]
        _adress         = req["adress"]
        _postnummer     = req["postnummer"]
        _company_name   = req["company_name"]

        try:
            new_user = KasaUser.objects.create(
                    username        = _username,
                    org_num         = _orgnum,
                    company_name    = _company_name,
                    adress          = json.dumps({"adress":_adress,"postnummer":_postnummer})
            )
            new_user.save()
        except:
            return HttpResponse(status=500)

        return JsonResponse({"username":s})

@csrf_exempt
def log_in_pc(request):
    if request.method=="POST":
        print("hahahahahahah")
        try:
            print(1)
            # data = json.loads(request.body)
            print(2)
            post_identifier = request.POST['identifier']
            print(3)
            encrypted_username=requestHandler.encrypt(post_identifier)
            print(encrypted_username)
            identifier=KasaUser.objects.get(username=encrypted_username)
            
            print(identifier.licence)
        except:
            return HttpResponse(status=404)
        try:
            request.session.set_expiry(0)
            request.session.set_test_cookie()
            request.session["username"]=str( post_identifier)
            request.session.modified=True
            print(request.session.keys())
            request.session.save()
            return HttpResponse(status=200)
        except:
            request.session.flush()
            return HttpResponse (status=400)
    elif request.method=="GET":
        return render(request, "personalnumber/pc_login.html")

@csrf_exempt
@pc_is_authenticated
def get_company(request:HttpRequest):
    if request.method=="POST":
        req=requestHandler.extractRequest(request)
        _username       = requestHandler.encrypt(request.session["username"])
        try:
            user=KasaUser.objects.get(username=_username)
        except:
            return HttpResponse(status=404)
        _orgnum         = req["org_num"]
        _adress         = req["adress"]
        _postnummer     = req["postnummer"]
        _company_name   = req["company_name"]
        user.org_num        = _orgnum,
        user.company_name   = _company_name,
        user.adress         = json.dumps({"adress":_adress,"postnummer":_postnummer})
        user.save()
        return HttpResponse(status=200)
        

@csrf_exempt
@pc_is_authenticated
def kasa_insertNotification(request):
    if(request.method == "POST"):
        req = requestHandler.extractRequest(request)
        notification = req["notification"]
        _username=request.session["username"]
        encrypted_username=requestHandler.encrypt(_username)
        try:
            _user = KasaUser.objects.get(username=encrypted_username)
        except:
            return HttpResponse(status=404)
        arr = literal_eval(_user.notifications)
        '''
        ['', '"{\\"title\\": \\"Korrigering\\", \\"month\\": \\"Mars\\", \\"year\\": \\"2022\\", \\"time\\": \\"16:42\\", \\"user\\": \\"kass\\\\u00f6r \\"}"']
        '''
        notification = json.dumps(req["notification"]).replace("'",'"')
        #jsonObj = {"title": req["title"], "month": req["month"], "year": req["year"], "time": req["time"], "user": req["user"]}
        arr.append(json.loads(notification))
        _user.notifications = json.dumps(arr)
        _user.save()

        return HttpResponse(200)
    return HttpResponse(403)

#kasa
#sending all the articles here from the kassa if there is a yes in the that column
@csrf_exempt
@pc_is_authenticated
def get_all_artiklar(request):
    if request.method =="POST":
        print("haaaaaaaaaaaaaaaaahaaaaaaaaaaaaaaaaahaaaaaaaaaaaaaaaa")
        req = requestHandler.extractRequest(request)
        _username=request.session["username"]
        encrypted_username=requestHandler.encrypt(_username)
        try:
            _user = KasaUser.objects.get(username=encrypted_username)
        except:
            return HttpResponse(status=404)
        _user.all_products=req ["artiklar"]
        print("hdjsakhdjkashjkdsahjdkashjkdashjk")
        _user.save()
        return JsonResponse({"access":"yes"})        


#kasa
@csrf_exempt
@pc_is_authenticated
def backup(request):
    if request.method=="POST":
        if "file" in request.FILES:
            # req=requestHandler.extractRequest(request)
            _username=request.POST["username"]
            encrypted_username=requestHandler.encrypt(_username)
            try:
                
                _user = KasaUser.objects.get(username=encrypted_username)
            except:
                return HttpResponse(status=404)
            last=_user.backup
            if _user.backup3 !=None and _user.backup3!="":
                if os.path.isfile(_user.backup3.path):
                    os.remove(_user.backup3.path)
            _user.backup3=_user.backup2
            _user.backup2=last
            _user.backup=request.FILES["file"]
            _user.save()
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400) 

#kasa
@csrf_exempt
@pc_is_authenticated
def check_backup(request):

    if request.method=="POST":
        req=requestHandler.extractRequest(request)

        _username=request.session["username"]
        encrypted_username=requestHandler.encrypt(_username)
        try:
            _user = KasaUser.objects.get(username=encrypted_username)
        except:
            return HttpResponse(status=404)
        obj={"last_backup":_user.backup_name()}
        return HttpResponse(json.dumps(obj))
    

#phone



#kasa
@csrf_exempt
@pc_is_authenticated
def sync_pn(request):
    if request.method=="POST":
        req=requestHandler.extractRequest(request)
        _username=request.session["username"]        
        _encrypted=requestHandler.encrypt(_username)
        try:
            _user=KasaUser.objects.get(username=_encrypted)
        except:
            return HttpResponse(status=404)
        try:
            pns:dict=json.loads(_user.prn)
        except:
            pns={}
        print(pns)
        pns_keys=pns.keys()
        _kasa_pn=req["pn"]
        if _kasa_pn not in pns_keys:
            pns[_kasa_pn]=""
        _user.prn=json.dumps(pns)
        _user.save()
        return HttpResponse(status=200)

@csrf_exempt
@pc_is_authenticated
def get_x(request):
    if request.method=="POST":
        req=requestHandler.extractRequest(request)
        username=request.session["username"]
        _encrypted=requestHandler.encrypt(username)
        try:
            _user=KasaUser.objects.get(username=_encrypted)
        except:
            return HttpResponse(status=404)
        _user.xRapport=req["x_rapport"]
        _user.save()
        return HttpResponse(status=200)

@csrf_exempt
@pc_is_authenticated
def check_z(request):
    if request.method=="POST":
        req=requestHandler.extractRequest(request)
        _username=request.session["username"]
        encrypted_username=requestHandler.encrypt(_username)
        try:
            _user = KasaUser.objects.get(username=encrypted_username)
        except:
            return HttpResponse(status=404)
        z=_user.z_rapport
        z_r=z
        if req["pn"] in z_r:
        
            z_p=z_r[req["pn"]]
            return(HttpResponse(json.dumps({"last_id":z_p["last_id"]})))
        else:
            return(HttpResponse(json.dumps({"last_id":0})))

@csrf_exempt
@pc_is_authenticated
def send_z(request):
    if request.method=="POST":
        req=requestHandler.extractRequest(request)
        _username=request.session["username"]
        encrypted_username=requestHandler.encrypt(_username)
        try:
            _user = KasaUser.objects.get(username=encrypted_username)
        except:
            return HttpResponse(status=404)
        _z=req["z_rapport"]
        pn=req["pn"]
        s_z=_user.z_rapport
        if pn not in s_z:

            s_z[pn]=_z
            _user.z_rapport=s_z
            _user.save()
        else:
            k_z=_z
            for item in k_z["items"]:
                s_z[pn]["items"].append(item)
            for item in k_z["vaxel"]:
                s_z[pn]["vaxel"].append(item)
            s_z[pn]["last_id"]=k_z["last_id"]
            _user.z_rapport=s_z
            _user.save()
        return(HttpResponse(status=200))    



@csrf_exempt
@pc_is_authenticated
def get_update(request):
    if request.method=="POST":
        req=requestHandler.extractRequest(request)
        _username=request.session["username"]
        _encrypted=requestHandler.encrypt(_username)
        try:
            _user=KasaUser.objects.get(username=_encrypted)
        except:
            return(HttpResponse(status=404))
        data=_user.kassa_list
        _user.kassa_list={"LäggTillArtikel":[], "UppdateraArtikel":[], "LäggTillHuvudgrupp":[],"UppdateraHuvudgrupp":[]}
        _user.save()
        return HttpResponse(json.dumps(data))


@csrf_exempt
@pc_is_authenticated
def send_huvudgrupper(request):
    if request.method=="POST":
        req=requestHandler.extractRequest(request)
        _username=request.session["username"]
        _encrypted=requestHandler.encrypt(_username)
        try:
            _user=KasaUser.objects.get(username=_encrypted)
        except:
            return(HttpResponse(status=404))
        _data=req["data"]
        _user.huvudgrupper=json.loads(_data)
        _user.save()
        return HttpResponse(status=200)