from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.


class Course(models.Model):
  course_code = models.CharField(max_length=20)
  content = RichTextUploadingField()
