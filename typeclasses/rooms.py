"""
Room

Rooms are simple containers that has no location of their own.

"""

# from evennia import DefaultRoom
from evennia.contrib.ingame_python.typeclasses import EventRoom
from latin.latin_declension import DeclineNoun
from typeclasses.latin_noun import LatinNoun

# Commenting out and changing inherit to EventRoom for ingame python
# class Room(DefaultRoom):
#
class Room(EventRoom,LatinNoun):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See examples/object.py for a list of
    properties and methods available on all Objects.
    """

    def at_object_creation(self):

        # add all of the case endings to attributes

        word = DeclineNoun(self.db.nom_sg,self.db.gen_sg,self.db.gender)
        forms = word.make_paradigm()
        all_forms = forms
        forms = forms[2:]
        self.db.dat_sg = forms[0][1]
        self.db.acc_sg = forms[1][1]
        self.db.abl_sg = forms[2][1]
        self.db.voc_sg = forms[3][1]
        self.db.nom_pl = forms[4][1]
        self.db.gen_pl = forms[5][1]
        self.db.dat_pl = forms[6][1]
        self.db.acc_pl = forms[7][1]
        self.db.abl_pl = forms[8][1]
        self.db.voc_pl = forms[9][1]

        # Add the variant forms to aliases for easy interaction
        for form in all_forms:
            self.aliases.add(form[1])

        self.tags.add('latin')
