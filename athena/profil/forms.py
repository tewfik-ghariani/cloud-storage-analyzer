from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100)
    pwd = forms.CharField(widget=forms.PasswordInput())
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    mail = forms.EmailField(label="Mail", help_text="@mail")
