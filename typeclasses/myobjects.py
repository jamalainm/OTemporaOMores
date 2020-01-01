from typeclasses.objects import Object
from latin.latin_declension import DeclineNoun
from typeclasses.latin_noun import LatinNoun
from commands import obj_command

class Flammable(Object):

    def at_object_creation(self):

        # add all of the case endings to attributes

        word = DeclineNoun(self.db.nom_sg[0],self.db.gen_sg[0],self.db.gender)
        forms = word.make_paradigm()
        all_forms = forms
        forms = forms[2:]
        self.db.dat_sg = [forms[0][1]]
        self.db.acc_sg = [forms[1][1]]
        self.db.abl_sg = [forms[2][1]]
        self.db.voc_sg = [forms[3][1]]
        self.db.nom_pl = [forms[4][1]]
        self.db.gen_pl = [forms[5][1]]
        self.db.dat_pl = [forms[6][1]]
        self.db.acc_pl = [forms[7][1]]
        self.db.abl_pl = [forms[8][1]]
        self.db.voc_pl = [forms[9][1]]

        # Add the variant forms to aliases for easy interaction
        for form in all_forms:
            self.aliases.add(form[1])

        self.db.flammable = True
        self.db.is_glowing = False

        self.tags.add('latin')

        self.cmdset.add(obj_command.FlammableCmdSet())
