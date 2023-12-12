from django.db import models

# Create your models here.

class ATCharacter(models.Model):
    name = models.CharField(max_length=80)
    real_name = models.CharField(max_length=150, null=True)
    image = models.CharField(max_length=500)
    short_description = models.CharField(max_length=500, null=True)
    description = models.CharField(max_length=1000, null=True)
    friends = models.JSONField(max_length=200, null=True)