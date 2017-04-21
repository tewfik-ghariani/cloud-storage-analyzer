from django.shortcuts import render
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.


def register(request):
    form = RegisterForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data['username']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        pwd = form.cleaned_data['pwd']
        mail = form.cleaned_data['mail']

        registered = True

        try:
            user = User.objects.create_user(username=username,
                                            first_name=first_name,
                                            last_name=last_name,
                                            password=pwd,
                                            email=mail)
        except:
            messages.error(request, 'This account is already registered!')
        #profile = Account(user=user)
        #profile.save()

    return render(request, 'profil/register.html', locals())


@login_required
def profile(request):
    usr = request.user
    is_disabled = "disabled"
    if request.method == 'POST':
        is_disabled = ""

    return render(request, 'profil/account.html', {'usr': usr,
                                                   'is_disabled': is_disabled,
                                                  })