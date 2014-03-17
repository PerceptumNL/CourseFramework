from django.conf.urls import patterns, url, include
from frontend import views

urlpatterns = \
    patterns('',
             url(r'^$',
                 views.interface, name='interface'),
    )
