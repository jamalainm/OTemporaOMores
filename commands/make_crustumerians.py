# file mygame/commands/make_crustumerians.py

from commands.gentes import clans
from random import choice
from random import randint

class Citizen():
    """
    Create a citizen with age, gender, class, suitable name
    """

    def __init__(self):
        self.clans = clans
        demographics = {
                (1,8): {'gender': 2, 'age':(0,6)},
                (9,16): {'gender': 2, 'age':(7,12)},
                (17,24): {'gender': 2, 'age':(13,19)},
                (25,34): {'gender': 2, 'age':(20,29)},
                (35,41): {'gender': 2, 'age':(30,39)},
                (42,47): {'gender': 2, 'age':(40,49)},
                (48,48): {'gender': 2, 'age':(50,100)},
                (49,56): {'gender': 1, 'age':(0,6)},
                (57,64): {'gender': 1, 'age':(7,12)},
                (65,72): {'gender': 1, 'age':(13,19)},
                (73,82): {'gender': 1, 'age':(20,29)},
                (83,92): {'gender': 1, 'age':(30,39)},
                (93,98): {'gender': 1, 'age':(40,49)},
                (99,100): {'gender': 1, 'age':(50,100)},
                }

        self.demographics = demographics
        self.demographics_list = list(demographics.keys())
        self.gens, self.details = self.choose_gens()
        self.gender, self.age = self.make_demo()
        self.praenomen,self.nomen = self.choose_name()
        self.genitive = self.make_genitive()
        self.stats = self.create_stats()
        self.pedigree = self.details['class']
        self.name = f"{self.praenomen} {self.nomen}"
        self.hometown = 'Crustumerium'

        self.character = {
                'name' : f"{self.praenomen} {self.nomen}",
                'gender' : self.gender,
                'age': self.age,
                'gens': self.gens,
                'hometown': 'Crustumerium',
                'pedigree': self.details['class'],
                'praenomen' : self.praenomen,
                'nomen': self.nomen,
                'nom_sg' : self.praenomen,
                'gen_sg' : self.genitive,
                'stats' : self.stats
                }
        
    def choose_gens(self):
        gentes = {}

        for clan in self.clans:
            gentes[clan[0]] = {'class':clan[1],'praenomina':clan[2:]}

        gens_list = list(gentes.keys())

        gens = choice(gens_list)

        return (gens, gentes[gens])

    def make_demo(self):
        roll = randint(1,100)

        for demo in self.demographics_list:
            if roll in range(demo[0],demo[1]+1):
                self.gender = self.demographics[demo]['gender']
                age_range = self.demographics[demo]['age']
                self.age = randint(age_range[0],age_range[1])

        return (self.gender, self.age)

    def choose_name(self):
        praenomina = self.details['praenomina']
        gens = self.gens
        gender = self.gender
        
        temp_names = praenomina
        if gender == 1:
            for index,value in enumerate(temp_names):
                if value in ['Marcus','Titus','Tullus']:
                    temp_names[index] = value[:-2] + 'ia'
                elif value[-2:] == 'us':
                    temp_names[index] = value[:-2] + 'a'
                elif value == 'Agrippa':
                    temp_names[index] = 'Agrippina'
                elif value == 'Caeso':
                    temp_names[index] = 'Caesula'
                elif value == 'Opiter':
                    temp_names[index] = 'Opita'
                elif value == 'Sertor':
                    temp_names[index] = 'Sertora'
                elif value == 'Volero':
                    temp_names[index] = 'Volerona'

            nomen = gens
        else:
            nomen = gens[:-1] + 'us'

        return (choice(temp_names), nomen)

    def make_genitive(self):
        praenomen = self.praenomen
        if praenomen[-1] == 'a':
            genitive = praenomen + 'e'
        elif praenomen[-1] == 'r':
            genitive = praenomen + 'is'
        elif praenomen[-2:] == 'us':
            genitive = praenomen[:-2] + 'i'
        else:
            genitive = praenomen + 'nis'
        return genitive

    def create_stats(self):
        age = self.age
        stats = []
        if age < 1:
            cha = randint(1,6) + randint(1,6) + randint(1,6)
            stats = [1,1,1,1,1,cha]

        elif age < 3:
            for i in range(1,6):
                stats.append(randint(1,3))
            cha = randint(1,6) + randint(1,6) + randint(1,6)
            stats.append(cha)

        elif age < 5:
            for i in range(1,6):
                stat = randint(1,3) + randint(1,3)
                stats.append(stat)
            cha = randint(1,6) + randint(1,6) + randint(1,6)
            stats.append(cha)

        elif age < 10:
            for i in range(1,6):
                stat = randint(1,3) + randint(1,3) + randint(1,3)
                stats.append(stat)
            cha = randint(1,6) + randint(1,6) + randint(1,6)
            stats.append(cha)

        elif age < 16:
            for i in range(1,6):
                stat = randint(1,4) + randint(1,4) + randint(1,4)
                stats.append(stat)
            cha = randint(1,6) + randint(1,6) + randint(1,6)
            stats.append(cha)

        else:
            for i in range(1,7):
                stat = randint(1,6) + randint(1,6) + randint(1,6)
                stats.append(stat)

        if age > 60:
            if stats[0] >= 5:
                stats[0] -=2
            if stats[1] >= 5:
                stats[1] -=2
            if stats[2] >= 5:
                stats[2] -=2
            stats[3] +=2
            stats[4] +=2
        elif age > 80:
            if stats[0] >= 7:
                stats[0] -=4
            if stats[1] >= 7:
                stats[1] -=4
            if stats[2] >= 7:
                stats[2] -=4
            stats[3] +=4
            stats[4] +=4

        return {
                'str':stats[0], 
                'dex':stats[1],
                'con':stats[2],
                'int':stats[3],
                'wis':stats[4],
                'cha':stats[5]
                }
