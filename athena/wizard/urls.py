from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.base, name="wizard"),
    url(r'^console$', views.console, name="console"),
    url(r'^new$', views.add_table, name="add_table"),
    url(r'^api/athena$', views.create_query, name="create"),
    url(r'^external$', views.external, name="external"),
]