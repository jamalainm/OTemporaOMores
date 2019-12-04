from django import forms
from django.db import models
# added for captcha
from .choices import *
from nocaptcha_recaptcha.fields import NoReCaptchaField

class AppForm(forms.Form):
    gens = forms.ChoiceField(choices=GENTES_CHOICES, required=True)
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect, required=True)
    praenomen = forms.ChoiceField(choices=PRAENOMINA_CHOICES, required=True)
    captcha = NoReCaptchaField()
