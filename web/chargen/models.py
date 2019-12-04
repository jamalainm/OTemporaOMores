# in mygame/web/chargen/models.py
from django import forms
from django.db import models
from .choices import *

class CharApp(models.Model):
    app_id = models.AutoField(primary_key=True)
    gens = models.IntegerField(choices=GENTES_CHOICES,default=1)
    gender = models.IntegerField(choices=GENDER_CHOICES,default=1)
    praenomen = models.IntegerField(choices=PRAENOMINA_CHOICES,default=1)
    date_applied = models.DateTimeField(verbose_name='Date Applied')
    background = models.TextField(verbose_name='Background')
    account_id = models.IntegerField(default=1, verbose_name='Account ID')
    submitted = models.BooleanField(default=False)
