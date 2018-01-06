from django.contrib import admin
from .models import Exercise
from .forms import ExerciseForm
# Register your models here.


class ExerciseAdmin(admin.ModelAdmin):
    form = ExerciseForm

admin.site.register(Exercise, ExerciseAdmin)
