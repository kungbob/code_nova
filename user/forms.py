from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *
from django_ace import AceWidget
 # extend Django's built-in UserCreationForm and UserChangeForm to
 # remove the username field (and optionally add any others that are
 # required)
class UserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """
    def __init__(self, *args, **kargs):
        super(UserCreationForm, self).__init__(*args, **kargs)
        # del self.fields['username']
    class Meta:
        model = User
        fields = '__all__'

class UserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    def __init__(self, *args, **kargs):
        super(UserChangeForm, self).__init__(*args, **kargs)
        # del self.fields['username']
    class Meta:
        model = User
        fields = '__all__'


 # ======================================================
 # Forms for users themselves edit their profiles
 # ======================================================
# from django import forms
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Submit
# from .models import User
#
# class CurrentUserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('email','last_name', 'first_name')
#
#     def __init__(self, *args, submit_title="儲存編輯", **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.add_input(Submit('submit', submit_title))
#         my_field_text= [
#             ('email', '電子郵件', '電子郵件將會作為您往後登入時使用'),
#             ('last_name', '姓', ''),
#             ('first_name', '名', ''),
#          ]
#         for x in my_field_text:
#             self.fields[x[0]].label=x[1]
#             self.fields[x[0]].help_text=x[2]
