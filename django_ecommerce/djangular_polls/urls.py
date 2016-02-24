from django.conf.urls import url

from . import json_views

urlpatterns = [
    url(r'^polls/$', json_views.PollCollection.as_view(),
        name='polls_collection'),

    url(r'^polls/(?P<pk>[0-9]+)$', json_views.PollMember.as_view()),

    url(r'^poll_items/$', json_views.PollItemCollection.as_view(),
        name='poll_item_collection'),

    url(r'^poll_items/(?P<pk>[0-9]+)$', json_views.PollItemMember.as_view()),
]
