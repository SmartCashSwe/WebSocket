
# from django.http import HttpResponse
# from security.src.controllers.requestTools.requestHandler import requestHandler
# from ast import literal_eval
# from django.core.exceptions import ObjectDoesNotExist
# from kasa.models import user 
# from PersonalNumber.models import Pc_user as user


# import json 
# from django.http import JsonResponse
# from django.utils import timezone
# from django.contrib.sessions.models import Session
# json_ready=json.dumps({
# 	"sales": [],
# 	"user": "ali@smartcash.se",
# 	"lastId": "0",
# 	"kvitto": []
# })
# def kasa_login(request):
#     if(request.method == "POST"):
#         req = requestHandler.extractRequest(request)
#         print(json.dumps( req))
#         u_name = req["name"]

            
#         u_pass = req["pass"]

#         query = user.objects.filter(email= u_name, password= u_pass)
#         if(len(query) != 0):
#             if("token" in req):
#                 user_sessions = []
#                 all_sessions  = Session.objects.filter(expire_date__gte=timezone.now())
#                 for session in Session.objects.all():
#                     print(session.get_decoded().get("user"))
#                     print("session user")

#                     if str(u_name) == session.get_decoded().get('user'):
#                         session.delete()
#                 _user = user.objects.get(email= u_name, password= u_pass)
#                 _user.fcm_token= req["token"]
#                 sales=json.loads(_user.sales)
#                 sales["lastId"]=req["lastId"][0]["kopId"]
#                 sales["sales"]=[]
#                 sales["kvitto"]=[]

#                 request.session.set_expiry(0)
#                 request.session.set_test_cookie()
#                 request.session["user"]=u_name
#                 print("start checking")
#                 print(request.session["user"])
#                 print("start loop")

#                 for key, value in request.session.items():
#                     print('{} => {}'.format(key, value))
            
#                 print("end for loop")                
#                 print("try")
#                 print(req["name"]) 
#                 request.session['user'] = req["name"]
#                 _user.sales=json.dumps(sales)
#                 _user.save()
#                 print("done")

#             print("after first line it")
            
#             print(query[0].fcm_token)
#             print("after second line")
            
#             print("login")
#             return HttpResponse(query[0].fcm_token)
#         print("failed login")
#         return HttpResponse(status=500)
#     return HttpResponse(403, "Unauthorized")

# def kasa_getSession(request):
#     print("start get session")
#     if(request.method == "GET"):
#         for key, value in request.session.items():
#             print('{} => {}'.format(key, value))
            
#         print("end for loop")
        
#         try:
#             if(request.session["user"] != ""):
#                 print(request.session)

#                 print(str( request.session.session_key))
#                 # _user=user.objects.get(email=request.session["user"])
#                 # _user.sales=json_ready
#                 # _user.save()
#                 print("________________________________________")
#                 session = {"email": request.session["user"]}
#                 print(session)
#                 jsonString = json.dumps(session, separators=(", ", ":"))
#                 print("end get session")
#                 return HttpResponse(jsonString)
#             else:
#                 return HttpResponse(500)
#         except:
#             return HttpResponse(500)
#     return HttpResponse(403)

# def kasa_clearSession(request):
#     if(request.method == "POST"):
#         for key, value in request.session.items():
#             print('{} => {}'.format(key, value))
#         request.session.flush()


#         return HttpResponse(status=200)
#     return HttpResponse(403)

# def kasa_signup(request):
#     if(request.method == "POST"):
#         req = requestHandler.extractRequest(request)

#         _username       = req["username"]
#         _email          = req["email"]
#         _password       = req["password"]
#         _phone_number   = req["phone_number"]
#         _orgnum         = req["org_num"]
#         _company_name   = req["company_name"]
#         _is_subscribed  = req["is_subscribed"]

#         new_user = user(
#                 username        = _username,
#                 email           = _email,
#                 password        = _password,
#                 phone_number    = _phone_number,
#                 org_num         = _orgnum,
#                 company_name    = _company_name,
#                 is_subscribed   = _is_subscribed
#         )
#         new_user.save()
#         return HttpResponse(200)

# def kasa_insertNotification(request):
#     if(request.method == "POST"):
#         req = requestHandler.extractRequest(request)

#         notification = req["notification"]
#         _user = user.objects.filter(email= req["email"])[0]
#         arr = literal_eval(_user.notifications)
#         '''
#         ['', '"{\\"title\\": \\"Korrigering\\", \\"month\\": \\"Mars\\", \\"year\\": \\"2022\\", \\"time\\": \\"16:42\\", \\"user\\": \\"kass\\\\u00f6r \\"}"']
#         '''
#         notification = json.dumps(req["notification"]).replace("'",'"')
#         print(notification)
#         #jsonObj = {"title": req["title"], "month": req["month"], "year": req["year"], "time": req["time"], "user": req["user"]}
#         arr.append(json.loads(notification))
#         print(json.loads(notification))

#         _user.notifications = json.dumps(arr)
#         _user.save()
#         print("______________________")
#         print(_user.notifications)

#         return HttpResponse(200)
#     return HttpResponse(403)

# def kasa_getNotifications(request):
#     print("Before getting a notifation")

#     if(request.method == "GET"):
#         print("getting notifications")

#         _user = user.objects.filter(email=request.session['user'])[0].notifications

#         the_user=user.objects.filter(email=request.session['user'])[0]
#         the_user.notifications="[]"
#         print(the_user.notifications)
#         the_user.save()
#         if(_user == None):
#             return HttpResponse("empty")
#         return HttpResponse(_user.replace("'",'"').replace("[","{").replace("]","}"))
#     return HttpResponse(403)



# #Johnnie's code
# #Sending 
# def get_artikel(request):
#     print("__________GET_ARTIKEL_START______________")
#     if request.method=="POST":
#         req = requestHandler.extractRequest(request)
#         the_user=request.session["user"]
#         print(req)
#         print("__________GET_ARTIKEL_END______________")
#         print(the_user)

#         jsonprod = json.dumps(req).replace("'",'"')
#         _user=user.objects.filter(email=the_user)[0]
#         _user.kasa_send=jsonprod
#         _user.save()
#         return HttpResponse(200)
#     else:
#         return HttpResponse(500)
#     return HttpResponse(400)

# def send_artikel(request):
#     print("sending file")
#     if request.method=="POST":
#         print(request)
#         print(requestHandler.extractRequest(request))
#         req = requestHandler.extractRequest(request)
#         name=req['user']
#         _user = user.objects.get(email=name)
#         if(_user == None):
#             return HttpResponse("empty")
#         product=_user.kasa_send
#         _user.kasa_send=""
#         _user.save()
#         print(product)
#         return JsonResponse(product, safe=False)


# #setting all produccs to yes to be able to send the articles with the next kasa request
# def set_access(request):
#    if request.method =="POST":
#         req = requestHandler.extractRequest(request)
#         the_user=request.session["user"]
#         try:
#             _user=user.objects.get(email=the_user)
#             _user.all_products="yes"
#         except:
#             return HttpResponse(500)
#         return HttpResponse(200)

# #checking if the all_products column has a yes and then return that yes to the kassa to know the the accsess is set to yes         
# def check_access(request):
#     if request.method=="POST":
#         req=requestHandler.extractRequest(request)
#         name=req["user"]
#         try:
#             the_user=user.objects.get(email=name)
#             data=the_user.all_products
#             print("data")
            
#             print(data)
#             if data=="yes" or data=="":
#                 print("hoahaohaohaohaohaohaohaohaohaoahohao")
#                 return JsonResponse("yes", safe=False)
#             return HttpResponse(400)
#         except ObjectDoesNotExist:
#             return HttpResponse(500)

 
# #sending all the articles here from the kassa if there is a yes in the that column
# def get_all_artiklar(request):
#     # try_get = False
#     if request.method =="POST":
#         # if try_get == True:
#         req = requestHandler.extractRequest(request)
#         name=req["user"]
#         print("hohohohohohohoho")
#         try:
#             _user=user.objects.get(email=name)
#         except:
#             return HttpResponse(404)
#         if _user.all_products =="yes" or _user.all_products=="":
#             # _user.all_products=req["artiklar"]
#             print(req)
#             _user.all_products=""
#             _user.save()
#             print("there is a yes")
#             _user.save()
#             print("________________________________")
#             string=""
#             try:
#                 string=json.dumps( req  )
#                 print(string)
#             except:
#                 pass
#             _user.all_products=string
#             _user.save()
#             print(_user.all_products)
#             return JsonResponse({"access":"yes"})
        
#         return HttpResponse(200)
        

# #sending the articles to the front end(mobile in this case)
# def send_to_mobile(request):
#     print("hhhjhjsdhjkasdhjaskhdsajkasdhjksdahsdjkhk")

#     if request.method =="POST":
#         req = requestHandler.extractRequest(request)
#         print(json.dumps(req))
#         print("_____________________________________________________")
#         the_user=request.session["user"]
#         print(the_user)
#         print("endendendendendendendendednen")
#         try:
#             _user=user.objects.get(email=the_user)

#             data=_user.all_products
#             _user.all_products=""
#             _user.save()

#             return HttpResponse( json.dumps(data))
#         except:
#             return HttpResponse(500)


# #getting the new sales from the kassa inot the sever database
# def get_sales(request):
#     if request.method=="POST":
#         req=requestHandler.extractRequest(request)
#         try:
#             the_user=req["user"]
#             _user=user.objects.get(email=the_user)
#         except ObjectDoesNotExist:
#             return HttpResponse(500)
#         all=json.loads(_user.sales)

#         try:
#             sales=json.loads(_user.sales)["sales"]
#             incoming_sales=req['sales']
#             print("1")
#             for x in incoming_sales:
#                 sales.append(x)
#             print("2")
#             kvittos=json.loads(_user.sales)["kvitto"]   
#             print("2.5") 
#             incoming_kvittos=req['kvitto']
#             print("3")
#             for x in incoming_kvittos:
#                 kvittos.append(x)
#             print("4")

#             all["sales"]=sales
#             all["lastId"]=req["lastId"]
#             all["kvitto"]=kvittos
#             print(json.dumps(req))
#             _user.sales=json.dumps(all)
#             _user.save()
#             return HttpResponse(200)
#         except:
#             return HttpResponse(500)
# #sending the new sales to the mobile phone
# def send_sales(request):
#     if request.method =="POST":
#         req = requestHandler.extractRequest(request)
#         print("the req",req)
#         print("hahahahahaha  "+json.dumps(req["lastId"][0]["kopId"]))
#         print("_________________________hahahahahahahaha____________________________")
#         the_user=request.session["user"]
#         print(the_user)
#         try:
#             _user=user.objects.get(email=the_user)
#             # print(json.loads(_user.sales))
            
#             data=json.loads(_user.sales)
#             saving_data=json.loads(_user.sales)
#             saving_data["sales"]=[]
#             saving_data["kvitto"]=[]
#             # saving_data["lastId"]=json.dumps(req["lastId"][0]["kopId"])
#             print(saving_data)
#             print("datadatadatadatadatadatadatadatadatadatadatadatadata")
#             print('data',json.dumps(data))
#             print('saving data',json.dumps(saving_data))

#             _user.sales=json.dumps(saving_data)
#             _user.save()
#             print("Not error")
#             return HttpResponse( json.dumps(data))
#         except:
#             print("error")
#             return HttpResponse(500)

# def check_sales(request):
#     if request.method=="POST":
#         req=requestHandler.extractRequest(request)
#         the_user=req["user"]
#         try:
#             _user=user.objects.get(email=the_user)
#             # _user.sales='{"sales" :[], "user": "ali@smartcash.se", "lastId": "0", "kvitto": []}'
#             # _user.save()
#         except ObjectDoesNotExist:
#             return HttpResponse(400)
#         try:
#             sales=json.loads(_user.sales)
#             print(sales["lastId"])
#             return(HttpResponse(json.dumps({"lastId":sales["lastId"]})))
#         except:
#             return (HttpResponse(json.dumps({"lastId":"0"})))
#         return HttpResponse(500)
    
    
    
    # ./apachectl start   