from django.conf.urls import patterns, url, include
from frontend import views
from frontend import api

urlpatterns = \
    patterns('',
             url(r'^$',
                 views.interface, name='interface'),
             url(r'admin/test/(?P<test_id>\d+)/?^$',
                 api.process_test_submission, name='admin_test_submission'),
    )
