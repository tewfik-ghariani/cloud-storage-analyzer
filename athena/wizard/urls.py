from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.base, name="wizard"),
    url(r'^console$', views.console, name="console"),
    url(r'^external$', views.external, name="external"),
    url(r'^database$', views.database, name="database"),
]