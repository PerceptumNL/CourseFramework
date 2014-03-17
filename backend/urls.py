from django.conf.urls import patterns, url, include
from backend import views

urlpatterns = \
    patterns('',
             url(r'^$',
                 views.interface, name='interface'),
    )
