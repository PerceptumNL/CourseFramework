from django.conf.urls import patterns, url, include
from frontend import views
from frontend import api

urlpatterns = patterns('',\
    url(r'^$',
        views.landing, name='landing'),
    url(r'^course/(?P<course_id>\d+)/?$', views.course, name='course'),
    url(r'^course/(?P<course_id>\d+)/lessons/?$', views.lessons,
        name='lessons'),
    url(r'^resource/(?P<course_id>\d+)/(?P<lesson_id>\d+)/(?P<resource_id>\d+)/?$',
        views.resource, name='resource'),
    url(r'admin/test/(?P<test_id>\d+)/?^$',
        api.process_test_submission, name='admin_test_submission'),
)
