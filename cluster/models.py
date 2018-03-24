from django.db import models
from exercise.models import Exercise

# Create your models here.
class Cluster(models.Model):
  exercise = models.ForeignKey(Exercise)
  data_count = models.IntegerField()
  center =  models.TextField(default="")
  necessary_skill = models.TextField(default="")
  redundant_skill = models.TextField(default="")
  character_skill = models.TextField(default="")
