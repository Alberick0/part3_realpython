from django.conf.urls import patterns, url, include
from main import json_views

urlpatterns = [
    # as view provides a function like interface into the class
    url(r'status_reports/$', json_views.StatusCollection.as_view(),
        name='status_reports_collection'),

    # using pk instead of if since is a drf requirement
    url(r'status_reports/(?P<pk>[0-9]+)$', json_views.StatusMember.as_view(),
        name='status_reports_collection'),

    url(r'badges/$', json_views.BadgeCollection.as_view(),
        name='badges_collection'),

    url(r'badges/(?P<pk>[0-9]+)$', json_views.BadgeMember.as_view(),
        name='badges_member')

]
