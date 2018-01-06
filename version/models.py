from django.db import models
from student.models import Student
from exercise.models import Exercise
from room.models import Room
# Create your models here.

class Version(models.Model):
    room = models.ForeignKey(Room,unique=False, on_delete=models.CASCADE,)
    code = models.TextField(default="")
    result = models.TextField(default="")
    version_tree = models.TextField(default='')
    overall_success = models.BooleanField(default=False)
