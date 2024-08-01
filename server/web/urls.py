from django.conf.urls import url

from . import views
from django.contrib.sitemaps.views import sitemap
from yolo.sitemaps import StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap
}

urlpatterns = [
    url(r'^$', views.abnormal, name='index'),
    url(r'^404/$', views.notfound, name='notfound'),
    url(r'^systeminfo/$', views.systeminfo, name='systeminfo'),
    
]
handler404 = views.notfound
