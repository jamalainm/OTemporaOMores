"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
# from evennia import DefaultCharacter
from evennia.contrib.ingame_python.typeclasses import EventCharacter
from latin.latin_declension import DeclineNoun
from typeclasses.latin_noun import LatinNoun

# Commenting out and replacing DefaultCharacter so we can use ingame python
#
# class Character(DefaultCharacter):
#
class Character(EventCharacter,LatinNoun):
    """
    The Character defaults to reimplementing some of base Object's hook methods with the
    following functionality:

    at_basetype_setup - always assigns the DefaultCmdSet to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead).
    at_after_move(source_location) - Launches the "look" command after every move.
    at_post_unpuppet(account) -  when Account disconnects from the Character, we
                    store the current location in the pre_logout_location Attribute and
                    move it to a None-location so the "unpuppeted" character
                    object does not need to stay on grid. Echoes "Account has disconnected"
                    to the room.
    at_pre_puppet - Just before Account re-connects, retrieves the character's
                    pre_logout_location Attribute and move it back on the grid.
    at_post_puppet - Echoes "AccountName has entered the game" to the room.

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
