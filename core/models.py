from django.db import models

# Create your models here.

class Channel(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False, unique=True)
    language = models.CharField(max_length=2, null=False, blank=False, default='ES')
    picture = models.ImageField(null=False, blank=False)