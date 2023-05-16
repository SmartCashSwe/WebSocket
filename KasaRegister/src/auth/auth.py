
import json
from core.settings import ARGON_HASH_SALT
import json
from django.contrib.auth.hashers import  make_password


class requestHandler:
    
    def extractRequest(request):
        return json.loads(request.body.decode('utf-8'))

    def encrypt(_x):


        return make_password( salt = ARGON_HASH_SALT, password=_x)

