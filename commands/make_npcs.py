# file mygame/commands/make_npcs.py

import time
from evennia.utils import utils, create, logger, search
from evennia.objects.models import ObjectDB
from django.conf import settings
from commands.make_crustumerians import Citizen

self = Citizen()

typeclass = settings.BASE_CHARACTER_TYPECLASS
start_location = ObjectDB.objects.get_id(settings.START_LOCATION)
default_home = ObjectDB.objects.get_id(settings.DEFAULT_HOME)
permissions = settings.PERMISSION_ACCOUNT_DEFAULT
new_character = create.create_object(
        typeclass, 
        key=self.name, 
        location='#249', 
        home=default_home, 
        permissions=permissions,
        attributes=[
            ('gender',self.gender),
            ('age',self.age),
            ('gens',self.gens),
            ('hometown',self.hometown),
            ('pedigree',self.pedigree),
            ('praenomen',self.praenomen),
            ('nomen',self.nomen),
            ('nom_sg',[self.praenomen]),
            ('gen_sg',[self.genitive]),
            ('stats', self.stats)
            ]
)
# only allow creator (and developers) to puppet this char
#new_character.locks.add(
#    "puppet:id(%i) or pid(%i) or perm(Developer) or pperm(Developer);delete:id(%i) or perm(Admin)"
#    % (new_character.id, account.id, account.id)
#)
#if desc:
#    new_character.db.desc = desc
#else:
#    new_character.db.desc = "This is a character."
#
#logger.log_sec(
#    "Character Created: %s (Caller: %s, IP: %s)."
#    % (new_character, account, self.session.address)
#)


