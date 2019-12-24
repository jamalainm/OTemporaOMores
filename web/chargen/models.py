# in mygame/web/chargen/models.py
from django import forms
from django.db import models
from .choices import *

class CharApp(models.Model):
    app_id = models.AutoField(primary_key=True)
    gens = models.TextField(verbose_name='Gens')
    gender = models.TextField(verbose_name='Gender')
    praenomen = models.TextField(verbose_name='Praenomen')
    date_applied = models.DateTimeField(verbose_name='Date Applied')
    background = models.TextField(verbose_name='Background')
    account_id = models.IntegerField(default=1, verbose_name='Account ID')
    submitted = models.BooleanField(default=False)
