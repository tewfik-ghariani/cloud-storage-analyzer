"""schemas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^$", views.base, name="welcome"),
    url(r"^second$", views.second, name="second"),
    url(r"^index$", views.index, name="index"),
    url(r"^list/$", views.list, name="list"),
    url(r"^config/$", views.config, name="config"),
    url(r"^details/$", views.details, name="details"),
    url(r"^FDV/$", views.FDV, name="FDV"),
]
