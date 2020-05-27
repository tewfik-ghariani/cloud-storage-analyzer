from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^$", views.wizard, name="wizard"),
    url(r"^console$", views.console, name="console"),
    url(r"^external$", views.external, name="external"),
    url(r"^metadata", views.metadata, name="metadata"),
]
