from django.db import models
from user.models import User

from user.constants import Constants
from django.db.models.signals import post_save

# Create your models here.


class Student(models.Model):
  user = models.OneToOneField(User,
    on_delete=models.CASCADE,)
  profile_tree = models.TextField(default="")

  def __str__(self):
      return self.user.email

def create_student(sender, instance, created, **kwargs):
    """
    :param sender: Class User.
    :param instance: The user instance.
    """
    if created:
        # Seems the following also works:
        #   UserProfile.objects.create(user=instance)
        # TODO: Which is correct or better?
        if instance.acc_type == Constants.STUDENT:
            student = Student(user=instance)
            student.save()

post_save.connect(create_student,
                  sender=User,
                  dispatch_uid="student-creation-signal")
