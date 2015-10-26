from django.conf.urls import patterns, url, include
from main import json_views

urlpatterns = [
    url(r'status_reports/$', json_views.status_collection,
        name='status_reports_collection'),

    url(r'status_reports/(?P<id>[0-9]+)$', json_views.status_collection,
        name='status_reports_collection'),
]
