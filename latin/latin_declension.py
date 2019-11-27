class DeclineNoun:
    def __init__(self,nom,gen,gender,irregular=False):
        self.nom = nom
        self.gen = gen
        self.gender = gender
        self.irregular = irregular

    def id_declension(self):

        if self.gen[-2:] == "ae":
            return [1, self.gen[:-2]]
        elif self.gen[-2:] == "is":
            return [3, self.gen[:-2]]
        elif self.gen[-2:] == "us":
            return [4, self.gen[:-2]]
        elif self.nom[-2:] == "es":
            return [5, self.gen[:-1]]
        else:
            return [2, self.gen[:-1]]

    def first_declension(self):

        base = DeclineNoun.id_declension(self)[1] 

        endings = ['ae', 'am', 'a', 'a', 'ae', 'arum', 'is', 'as', 'is', 'ae']

        forms = [self.nom, self.gen]

        for i in endings:
            forms.append(base + i)

        return forms

    def second_declension(self):

        base = DeclineNoun.id_declension(self)[1] 

        endings = ['o', 'um','o','e','i','orum','is','os','is','i']

        forms = [self.nom,self.gen]

        for i in endings:
            forms.append(base + i)

        if base[-1] == 'r':
            forms[5] = self.nom
        elif base[-1] == 'i':
            forms[5] = base[:-1] + 'i'

        if self.gender == 3:
            forms[3] = self.nom
            forms[5] = self.nom
            forms[6] = base + 'a'
            forms[9] = base + 'a'
            forms[11] = base + 'a'

        return forms

    def third_declension(self):

        from cltk.stem.latin.syllabifier import Syllabifier

        syllabifier = Syllabifier()

        vowels = ['a','e','i','o','u','a','e','i','o','u']

        base = DeclineNoun.id_declension(self)[1]

        forms = [self.nom,self.gen]

        endings = ['i','em','e','blah','es','um','ibus','es','ibus','es']

        for i in endings:
            forms.append(base + i)

        forms[5] = self.nom

        nom_syllable = len(syllabifier.syllabify(self.nom))
        gen_syllable = len(syllabifier.syllabify(self.gen))

        i_stem = False

        if nom_syllable == gen_syllable:
            if self.nom[-2:] in ['is', 'es']:
                i_stem = True
        elif self.nom[-1] in ['x', 's']:
             if base[-1] not in vowels and base[-2] not in vowels:
                 i_stem = True

        if i_stem == True:

            forms[7] = forms[7][:-2] + 'i' + forms[7][-2:]

        if self.gender == 3:
            forms[5] = self.nom
            forms[3] = self.nom
            forms[6] = base + 'a'
            forms[9] = base + 'a'
            forms[11] = base + 'a'
            if self.nom[-1] == 'e' or self.nom[-2:] in ['al','ar']:
                forms[4] = base + 'i'
                forms[6] = base + 'ia'
                forms[7] = base + 'ium'
                forms[9] = base + 'ia'
                forms[11] = base + 'ia'
        return forms


    def fourth_declension(self):

        base = DeclineNoun.id_declension(self)[1]

        endings = ['ui','um','u','us','us','uum','ibus','us','ibus','us']

        forms = [self.nom,self.gen]

        for i in endings:
            forms.append(base + i)

        if self.gender == 3:
            forms[3] = self.nom
            forms[2] = base + 'u'
            forms[5] = self.nom
            forms[6] = base + 'ua'
            forms[9] = base + 'ua'
            forms[11] = base + 'ua'

        return forms

    def fifth_declension(self):

        base = DeclineNoun.id_declension(self)[1] 

        base = base[:-1] + "e"

        endings = ['i', 'm', '', 's', 's', 'rum', 'bus', 's', 'bus', 's']

        forms = [self.nom,self.gen]

        for i in endings:
            forms.append(base + i)

        forms[3] = forms[3][:-2] + 'em'

        if base[-2] != 'i':
            forms[1] = forms[1][:-2] + 'ei'
            forms[2] = forms[2][:-2] + 'ei'

        return forms

    def make_paradigm(self):
        
        labels = ['nom_sg','gen_sg','dat_sg','acc_sg','abl_sg','voc_sg','nom_pl','gen_pl','dat_pl','acc_pl','abl_pl','voc_pl']

        forms = []

        if DeclineNoun.id_declension(self)[0] == 1:
            forms = self.first_declension()
        elif DeclineNoun.id_declension(self)[0] == 2:
            forms = DeclineNoun.second_declension(self)
        elif DeclineNoun.id_declension(self)[0] == 3:
            forms = DeclineNoun.third_declension(self)
        elif DeclineNoun.id_declension(self)[0] == 4:
            forms = DeclineNoun.fourth_declension(self)
        else:
            forms = DeclineNoun.fifth_declension(self)

        declension = []
        for index,value in enumerate(labels):
            declension.append((value,forms[index]))

        return declension
