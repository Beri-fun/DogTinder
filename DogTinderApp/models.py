from django.db import models

# Create your models here.
class Dog(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False)
    age = models.CharField(max_length=256, null=False, blank=False)
    size = models.CharField(max_length=256, null=False, blank=False)
    sex = models.CharField(max_length=256, null=False, blank=False)
    activity_level = models.CharField(max_length=256, null=False, blank=False)
    hair_length = models.CharField(max_length=256, null=False, blank=False)
    another_pets = models.BooleanField(default=False, null=False, blank=False)
    children = models.BooleanField(default=False, null=False, blank=False)
    description = models.TextField(null=False, blank=False)