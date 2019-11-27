# in mygame/web/chargen/models.py
from django import forms
from django.db import models

class CharApp(models.Model):
    app_id = models.AutoField(primary_key=True)
    char_name = models.CharField(max_length=80, verbose_name='Character Name')
# Added the following line in order to grab gender as well
    genitive = models.CharField(max_length=80, verbose_name='Genitive Form')
    date_applied = models.DateTimeField(verbose_name='Date Applied')
    background = models.TextField(verbose_name='Background')
    account_id = models.IntegerField(default=1, verbose_name='Account ID')
    submitted = models.BooleanField(default=False)
