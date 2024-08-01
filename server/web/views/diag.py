from api.models import User
from web.views.views import CheckToken, GetLoginSession
from django.conf import settings

def compare(request):
    permissions = ["Root"]
    return CheckToken(request, 'compare.html', permissions)

def draw_landmark(request):
    permissions = ["Root"]
    return CheckToken(request, 'draw_landmark.html', permissions)

def checkmedia(request):
    permissions = ["Root"]
    return CheckToken(request, 'checkmedia.html', permissions)

def face_direction(request):
    permissions = ["Root"]
    return CheckToken(request, 'face_direction.html', permissions)

def brightness(request):
    permissions = ["Root"]
    return CheckToken(request, 'brightness.html', permissions)

def abnormal(request):
    permissions = ["all"]
    # jwt = GetLoginSession(request)
    args = {}
    args["THRESHOLD"] = settings.THRESHOLD

    # if(jwt != None and jwt["level"] == "Root"):
    #     owners = User.objects(level="Admin", isDeleted=False).order_by("email")
    #     args["owners"] = owners.to_json()
    # else:
    #     args["owners"] = "[]"

    return CheckToken(request, 'abnormal.html', permissions, args)