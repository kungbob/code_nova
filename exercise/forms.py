from django.forms import ModelForm, Textarea
from .models import Exercise
from django_ace import AceWidget
 # extend Django's built-in UserCreationForm and UserChangeForm to
 # remove the username field (and optionally add any others that are
 # required)
class ExerciseForm(ModelForm):

    class Meta:
        model = Exercise
        fields = '__all__'
        widgets = {
            'template': AceWidget(mode='python',theme='monokai'),
        }
