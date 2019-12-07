from django import forms
from django.db import models
# added for captcha
from .choices import *
from nocaptcha_recaptcha.fields import NoReCaptchaField
import random
# added in order to include a text string of character attributes
from django.utils.safestring import mark_safe

#This class is intended to create a widget that will display a text field with random values
class PlainTextWidgetWithHiddenCopy(forms.Widget):
    def render(self, name, value, attrs, renderer=None):
        if hasattr(self, 'initial'):
            value = self.initial

        return mark_safe(
                (str(value) if value is not None else '-') +
                    f"<input type='hidden' name='{name}' value='{value}'>"
                )

class AppForm(forms.Form):
    gens = forms.ChoiceField(choices=GENTES_CHOICES, required=True, label='Gens (This is the familial clan with which every natural born Roman citizen was associated and would be the basis for the name by which most people addressed them.')
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect, required=True, label='Gender')
    praenomen = forms.ChoiceField(choices=PRAENOMINA_CHOICES, required=True, label='Praenomen (This is the name by which very close friends and familiy members would address you.')
    # Trying out stat generation
#   It won't regenerate the numbers on page refresh this way
#    dict_attributes = {'str':8, 'dex':8, 'con':8, 'int':8, 'wis':8, 'cha':8}
#    points = 27
#    while points > 0:
#        attribute = random.choice(list(dict_attributes))
#        value = dict_attributes[attribute]
#        if value <= 14:
#            if points > 0:
#                if value < 13:
#                    dict_attributes[attribute] += 1
#                    points -= 1
#                elif value == 13 or value == 14:
#                    if points >= 2:
#                        dict_attributes[attribute] += 1
#                        points -= 2
#    strength = dict_attributes['str'] + 1
#    dexterity = dict_attributes['dex'] + 1
#    constitution = dict_attributes['con'] + 1
#    intelligence = dict_attributes['int'] + 1
#    wisdom = dict_attributes['wis'] + 1
#    charisma = dict_attributes['cha'] + 1
#    stuff = (f"Vires: {strength} Celeritas: {dexterity} Valetudo: {constitution} Mens: {intelligence} Sapientia: {wisdom} Amicitia: {charisma}")
    # Changed up to the comment above

    captcha = NoReCaptchaField()
#    stats = forms.CharField(widget=PlainTextWidgetWithHiddenCopy,initial=stuff,label='Attributes (These are your physical, mental, and social ratings; every set of scores is equally balanced, but you may reload the page if you would like a different distribution.')
