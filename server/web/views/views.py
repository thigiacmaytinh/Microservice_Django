import json
import mimetypes
import os
from django.shortcuts import render, redirect
from django.http import HttpResponse, StreamingHttpResponse
from rest_framework.decorators import api_view
from api.models import Currency, LoginSession, Person, PersonGroup, User
import datetime, time
from django.conf import settings
from api import auth
from api.apps import printt, utcnow



def activity(request):
    permissions = ["Root", "Admin"]
    return CheckToken(request, 'activity.html', permissions)

def attendance(request):
    args = {'fullscreen' : True}
    permissions = ["Root", "Admin", "Gate", "Supporter"]
    return CheckToken(request, 'attendance.html', permissions, args)

def appear(request):
    args = {}
    jwt = GetLoginSession(request)
    if(jwt == None):
        return redirect("/login")

    # happy birthday
    nday = 1
    today = utcnow() + datetime.timedelta(hours=7)
    today = today.replace(hour=0, minute=0, second=0)
    
    birthdayPerson = []
    if(today.month != 2 and today.day != 29):
        persons = Person.objects(birthday__ne=None, isDeleted=False)
        for person in persons:   
            birthday = person.birthday + datetime.timedelta(hours=7)        
            then = today.replace(year=birthday.year) + datetime.timedelta(days=nday)
            if(birthday < then):
                diff = birthday - today.replace(year=birthday.year)
                if(diff.days >= 0 and diff.days <= nday):
                    obj = json.loads(person.to_json())
                    obj["days"] = diff.days
                    birthdayPerson.append(obj)

    args["birthday"] = json.dumps(birthdayPerson) 

    personGroups = PersonGroup.objects(owner=jwt["owner"], isDeleted=False)
    args["personGroups"] = personGroups.to_json()
    permissions = ["Root", "Admin", "Gate"]
    args["THRESHOLD"] = settings.THRESHOLD
    return CheckToken(request, 'appear.html', permissions, args)

def changepassword(request):
    permissions = ["all"]
    return CheckToken(request, 'changepassword.html', permissions)

def dashboard(request):
    permissions = ["Root", "Admin", "Gate"]
    return CheckToken(request, 'dashboard.html', permissions)

def database(request):
    permissions = ["Root"]
    return CheckToken(request, 'database.html', permissions)

def download(request, filepath):
    jwt = GetLoginSession(request)
    if(jwt == None):
        return render(request, "404.html")
    if(jwt["email"] not in ["admin", "root"]):
        return render(request, "404.html")
    
    try:
        fileName = GetFileName(filepath)
        filepathAbs = os.path.join(settings.MEDIA_ROOT.replace("media", "download"), filepath)
        fsock = open(filepathAbs, "rb")
        mime_type_guess = mimetypes.guess_type(filepath)
        if mime_type_guess is not None:
            response = HttpResponse(fsock, content_type=mime_type_guess[0])
        response['Content-Disposition'] = 'attachment; filename=' + fileName
        return response
    except Exception as e:
        printt(str(e))
        return render(request, "404.html")

def person(request):
    jwt = GetLoginSession(request)
    args = {}
    args["THRESHOLD"] = settings.THRESHOLD

    if(jwt != None and jwt["level"] == "Root"):
        owners = User.objects(level="Admin", isDeleted=False).order_by("email")
        args["owners"] = owners.to_json()
    else:
        args["owners"] = "[]"
    permissions = ["Root", "Admin", "Gate", "Supporter"]
    return CheckToken(request, 'person.html', permissions, args)

def exchange(request):
    permissions = ["Root", "Admin"]
    args = {}
    currencies = Currency.objects(isDeleted=False)
    args["currencies"] = currencies.to_json()
    return CheckToken(request, 'exchange.html', permissions, args)


def exchange_history(request):
    permissions = ["Root", "Admin"]
    return CheckToken(request, 'exchange_history.html', permissions)

def notification(request):
    permissions = ["Root", "Admin", "Gate", "Partner"]
    return CheckToken(request, 'notification.html', permissions)

def option(request):
    permissions = ["Root", "Admin"]
    return CheckToken(request, "option.html", permissions)

def persongroup(request):
    permissions = ["Root", "Admin", "Gate", "Supporter"]
    return CheckToken(request, 'persongroup.html', permissions)

def phone(request):
    permissions = ["Root", "Admin"]
    return CheckToken(request, 'phone.html', permissions)

def shift(request):
    permissions = ["Root", "Admin"]
    return CheckToken(request, 'shift.html', permissions)

def usergroup(request):
    permissions = ["Root", "Admin"]
    return CheckToken(request, 'usergroup.html', permissions)

@api_view(["POST", "GET"])
def login(request):
    permissions = ["Root", "Admin", "Gate", "Supporter"]
    return CheckToken(request, 'dashboard.html', permissions)

def logout(request):
    try:        
        _token = request.COOKIES.get('token')
        jwt = LoginSession.objects.get(token=_token, isDeleted = False)
        jwt.isDeleted = True
        jwt.save()        
    except Exception as e:
        print(str(e))

    res = redirect('login')
    res.delete_cookie('token')
    res.delete_cookie('email')
    return res

def index(request):
    _token = request.COOKIES.get('token')
    if(_token == None or _token == ""):
        return redirect("/login")
    else:
        if(IsValidToken(request)):
            return redirect("/dashboard")
        else:
            return redirect("/login")
                
        

def register(request):
    _token = request.COOKIES.get('token')
    if(_token == None or _token == ""):
        args = {'authorized': False}
        return render(request, 'register.html', args)
    else:
        return redirect("/dashboard")

def profile(request):
    permissions = ["Root", "Admin", "Gate"]
    return CheckToken(request, 'profile.html', permissions)

def user(request):
    permissions = ["Root", "Admin"]
    return CheckToken(request, 'user.html', permissions)

def client(request):
    permissions = ["Root", "Admin"]
    return CheckToken(request, 'client.html', permissions)

def config(request):
    permissions = ["Root", "Admin"]
    return CheckToken(request, 'config.html', permissions)

def detect(request):
    args = {'fullscreen' : True}
    permissions = ["Root", "Admin", "Gate", "Supporter"]
    return CheckToken(request, 'detect.html', permissions, args)

def log(request):
    permissions = ["Root"]
    return CheckToken(request, 'log.html', permissions)

def GateAccount(request):
    permissions = ["Root", "Admin"]
    return CheckToken(request, 'gateaccount.html', permissions)

def Supporter(request):
    permissions = ["Root"]
    return CheckToken(request, 'supporter.html', permissions)

def systeminfo(request):
    args = GetSystemInfo()
    permissions = ["Root", "Admin"]
    return CheckToken(request, 'systeminfo.html', permissions, args)

    
def Redirect(request):
        args = {
            'authorized': False,
            'version' : settings.VERSION,
            }
        return render(request, 'redirect.html' , args)
    
def CheckToken(request, redirect_page, permissions, args=None):
    isValidToken = False
    
    if(args == None):
        args = {}

    args['debug'] = settings.DEBUG
    args['authorized'] = False
    args['version'] = settings.VERSION
    args['numGateAccountAdded'] = 0

    if("all" in permissions):
        isValidToken = True

    if(not isValidToken):
        jwt = GetLoginSession(request)
        if jwt != None:
            args['email'] = jwt["email"]
            args['level'] = jwt["level"]

            for p in permissions:
                if(p == jwt["level"]):
                    isValidToken = True
                    break

    if(isValidToken):
        args['authorized'] = True
        if("fullscreen" not in args):
            args['fullscreen'] = False
        return render(request, redirect_page , args)
    # else:        
    #     args['fullscreen'] = True
    #     response = render(request, 'login.html', args)
    #     response.delete_cookie('token')
    #     response.delete_cookie('email')
    #     return response


def IsValidToken(request):
    try:
        _token = request.COOKIES.get('token')
        if(_token == None or _token == ""):
            _token = request.GET.get('token')
        if(_token == None or _token == ""):
            return False

        auth.decode(_token)
        return True
    except Exception as e:
        print(str(e))

        return False



def GetLoginSession(request):
    try:
        _token = request.COOKIES.get('token')
        if(_token == None or _token == ""):
            _token = request.GET.get('token')
        if(_token == None or _token == ""):
            return None

        jwt = auth.decode(_token)
        return jwt
    except Exception as e:
        printt(str(e))

    return None


