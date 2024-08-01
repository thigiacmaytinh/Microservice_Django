from django.conf.urls import url

from . import views
from api.main import OnReady

#OnReady()

urlpatterns = [
    url(r'^yolo/detect$', views.DetectYOLO),
]