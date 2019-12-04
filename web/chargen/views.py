# file mygame/web/chargen/views.py
from django.shortcuts import render

# Create your views here.

from .choices import *
from .models import CharApp

def index(request):
    current_user = request.user # current user logged in
    p_id = current_user.id # the account id
    # submitted Characters by this account
    sub_apps = CharApp.objects.filter(account_id=p_id, submitted=True)
    context = {'sub_apps': sub_apps}
    # make the variables in 'context' available to the web page template
    return render(request, 'chargen/index.html', context)


def detail(request, app_id):
    app = CharApp.objects.get(app_id=app_id)
    praenomen = app.praenomen
    gens = app.gens
    gender = app.gender
    # This is a mess, since I don't know how to have a
    # dynamic character creation form where different
    # names become available based on gender and gens
    praenomen = PRAENOMINA_CHOICES[int(praenomen) - 1][1]
    gens = GENTES_CHOICES[int(gens) - 1][1]
    names = praenomen.split('/')
    if int(gender) == 2:
        name - names[1].strip()
        gens = gens[:-1] + 'us'
    else:
        name = names[0].strip()
    name = name + ' ' + gens
    # changes made aove this line
    submitted = app.submitted
    p_id = request.user.id
    context = {'name': name, 'genitive': genitive, 
        'p_id': p_id, 'submitted': submitted}
    return render(request, 'chargen/detail.html', context)

from web.chargen.models import CharApp
from web.chargen.forms import AppForm
from django.http import HttpResponseRedirect
from datetime import datetime
from evennia.objects.models import ObjectDB
from django.conf import settings
from evennia.utils import create

def creating(request):
    user = request.user
    if request.method == 'POST':
        form = AppForm(request.POST)
        if form.is_valid():
	    # Added the following line
            gender = form.cleaned_data['gender']
            gens = form.cleaned_data['gens']
            praenomen = form.cleaned_data['praenomen']
            applied_date = datetime.now()
            submitted = True
            if 'save' in request.POST:
                submitted = False
            app = CharApp(praenomen=praenomen,gens=gens,gender=gender,
            date_applied=applied_date, account_id=user.id,
            submitted=submitted)
            app.save()
            if submitted:
                praenomen = PRAENOMINA_CHOICES[int(praenomen) - 1][1]
                gens = GENTES_CHOICES[int(gens) - 1][1]
                names = praenomen.split('/')
                if int(gender) == 2:
                    name = names[1].strip()
                else:
                    name = names[0].strip()
                if name[-1] == 'a':
                    genitive = name + 'e'
                elif name[-2:] == 'us':
                    genitive = name[:-2] + 'i'
                elif name[-1] == 'r':
                    genitive = name + 'is'
                else:
                    genitive = name + 'nis'
                # Create the actual character object
                typeclass = settings.BASE_CHARACTER_TYPECLASS
                home = ObjectDB.objects.get_id(settings.GUEST_HOME)
                # turn the permissionhandler to a string
                perms = str(user.permissions)
                # create the character
                char = create.create_object(typeclass=typeclass, key=name,
                    home=home, permissions=perms,attributes=[('gender', gender),('gens', gens),('nom_sg', name),('gen_sg', genitive)])
                user.db._playable_characters.append(char)
                # add the right locks for the character so the account can
                #  puppet it
                # editing the below in order to give account permission
                # to delete, which for some reason it seems to be lacking
                # char.locks.add("puppet:id(%i) or pid(%i) or perm(Developers) "
                char.locks.add(f"puppet:id({char.id}) or pid({user.id}) or perm(Developers) or pperm(Developers);delete:id({user.id}) or perm(Admin)")
            # changing from "/chargen" to "/characters"
            return HttpResponseRedirect('/characters')
    else:
        form = AppForm()
    return render(request, 'chargen/create.html', {'form': form})
