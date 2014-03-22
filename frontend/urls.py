from django.conf.urls import patterns, url, include
from frontend import views
from frontend import api

urlpatterns = patterns('',\
    url(r'^$',
        views.landing, name='landing'),
    url(r'^course/(?P<course_id>\d+)/?$', views.course, name='course'),
    url(r'^course/(?P<course_id>\d+)/lessons/?$', views.lessons,
        name='lessons'),
    url(r'^item/(?P<course_id>\d+)/(?P<lesson_id>\d+)/(?P<item_index>\d+)/?$',
        views.item, name='item'),
    url(r'^item/(?P<course_id>\d+)/(?P<lesson_id>\d+)/(?P<parent_id>\d+)/related/(?P<related_id>\d+)/?$',
        views.related, name='related'),
    url(r'api/test/(?P<test_id>\d+)/?$',
        api.process_test_submission, name='api_test_submission'),
)
