from django.shortcuts import render
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.


def register(request):
    form = RegisterForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data["username"]
        first_name = form.cleaned_data["first_name"]
        last_name = form.cleaned_data["last_name"]
        pwd = form.cleaned_data["pwd"]
        mail = form.cleaned_data["mail"]

        registered = True

        if User.objects.filter(email__iexact=mail).exists():
            messages.error(request, "This email is already used ")
        else:
            try:
                user = User.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    password=pwd,
                    email=mail,
                )
            except:
                messages.error(request, "This account is already registered!")

    return render(request, "profil/register.html", locals())


@login_required
def profile(request):
    the_user = request.user
    is_disabled = "disabled"
    if request.method == "POST":
        if request.POST.get("edit"):
            is_disabled = ""
        elif request.POST.get("save"):
            new_username = request.POST.get("username")
            new_first_name = request.POST.get("first_name")
            new_last_name = request.POST.get("last_name")
            new_email = request.POST.get("email")
            if (
                not new_email
                or not new_first_name
                or not new_username
                or not new_last_name
            ):
                messages.error(request, "No empty credentials  ")

            elif (
                User.objects.filter(email__iexact=new_email)
                .exclude(username=the_user.username)
                .exists()
            ):
                messages.error(request, "This email is already used ")

            elif (
                User.objects.filter(first_name__iexact=new_first_name)
                .exclude(username=the_user.username)
                .exists()
            ):
                messages.error(request, "The first name is already used")

            elif (
                User.objects.filter(last_name__iexact=new_last_name)
                .exclude(username=the_user.username)
                .exists()
            ):
                messages.error(request, "The last name  is already used")

            elif (
                User.objects.filter(username__iexact=new_username)
                .exclude(username=the_user.username)
                .exists()
            ):
                messages.error(request, "This user name  is already used")
            else:
                the_user.username = new_username
                the_user.last_name = new_last_name
                the_user.email = new_email
                the_user.first_name = new_first_name
                the_user.save()
                messages.success(request, "Credentials updated successfully ")

    return render(
        request, "profil/account.html", {"usr": the_user, "is_disabled": is_disabled,}
    )
