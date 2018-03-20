from django.db import models
from exercise.models import Exercise
# Create your models here.
class Cluster(models.Model):
  exercise = models.ForeignKey(Exercise)
  total = models.IntegerField()
  centroid =  models.TextField(default="")
  skills = models.TextField(default="")
