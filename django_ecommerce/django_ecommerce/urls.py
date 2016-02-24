"""django_ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from payments import views
import main.views
import main.urls

import contact.views

import djangular_polls.urls

api_patterns = main.urls.urlpatterns + djangular_polls.urls.urlpatterns

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', main.views.index, name='home'),
    url(r'^pages/', include('django.contrib.flatpages.urls')),
    url(r'^contact/', contact.views.contact, name='contact'),

    # user registration
    url(r'^sign_in$', views.sign_in, name='sign_in'),
    url(r'^sign_out$', views.sign_out, name='sign_out'),
    url(r'^register$', views.register, name='register'),
    url(r'^edit$', views.edit, name='edit'),
    url(r'^report$', main.views.report, name='report'),

    # api
    url(r'^api/v1/', include(api_patterns)),

    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]
