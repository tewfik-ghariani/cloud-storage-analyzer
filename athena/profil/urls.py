from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(
        r"^login$",
        auth_views.login,
        {"template_name": "profil/login.html"},
        name="login",
    ),
    url(
        r"^logout$",
        auth_views.logout,
        {"template_name": "profil/logged_out.html"},
        name="logout",
    ),
    url(r"^register$", views.register, name="register"),
    ## ------------- Password Reset -----------------------------
    url(
        r"^pwd/reset$",
        auth_views.password_reset,
        {
            "template_name": "profil/password_reset_form.html",
            "email_template_name": "profil/password_reset_email.html",
        },
        name="password_reset_form",
    ),
    url(
        r"^pwd/done$",
        auth_views.password_reset_done,
        {"template_name": "profil/password_reset_done.html"},
        name="password_reset_done",
    ),
    url(
        r"^pwd/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        auth_views.password_reset_confirm,
        {"template_name": "profil/password_reset_confirm.html"},
        name="password_reset_confirm",
    ),
    url(
        r"^pwd/complete$",
        auth_views.password_reset_complete,
        {"template_name": "profil/password_reset_complete.html"},
        name="password_reset_complete",
    ),
    url(r"^profile$", views.profile, name="profile"),
    ## ------------- Password Change -----------------------------
    url(
        r"^pwd/change$",
        auth_views.password_change,
        {"template_name": "profil/password_change_form.html"},
        name="password_change",
    ),
    url(
        r"^pwd/changed$",
        auth_views.password_change_done,
        {"template_name": "profil/password_change_done.html"},
        name="password_change_done",
    ),
]
