from django import forms
from user.models import User
from user.constants import Constants
from django.contrib.auth.models import User as auth_user
from django.contrib.auth import authenticate, login
from django.contrib.auth import login as auth_login


class LoginForm(forms.Form):
    email = forms.CharField(label='email', max_length=100)
    password = forms.CharField(label='password', max_length=100,widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(LoginForm,self).clean()

        my_email = cleaned_data.get("email")
        my_password = cleaned_data.get("password")

        user = authenticate(email=my_email, password=my_password)
        if user is  None:
            self.add_error('email','login failed')
            self.add_error('password','password failed')
            self.add_error(None,'something failed')


class RegisterForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
    acc_type = forms.ChoiceField(choices=Constants.ACC_TYPE_CHOICES)

    def clean(self):
        cleaned_data = super(RegisterForm,self).clean()

        my_email = cleaned_data.get("email")
        my_password = cleaned_data.get("password")
        my_password2 = cleaned_data.get("password2")
        my_acc_type = cleaned_data.get("acc_type")


        users = User.objects.filter(email = my_email)

        if users.exists():
            self.add_error('email','email is used!')


        if len(my_password) < 6:
            self.add_error('password','password must be 6 character long!')

        if not my_password == my_password2:
            self.add_error('password2','password not the same !')
