"""
Prototypes

A prototype is a simple way to create individualized instances of a
given `Typeclass`. For example, you might have a Sword typeclass that
implements everything a Sword would need to do. The only difference
between different individual Swords would be their key, description
and some Attributes. The Prototype system allows to create a range of
such Swords with only minor variations. Prototypes can also inherit
and combine together to form entire hierarchies (such as giving all
Sabres and all Broadswords some common properties). Note that bigger
variations, such as custom commands or functionality belong in a
hierarchy of typeclasses instead.

Example prototypes are read by the `@spawn` command but is also easily
available to use from code via `evennia.spawn` or `evennia.utils.spawner`.
Each prototype should be a dictionary. Use the same name as the
variable to refer to other prototypes.

Possible keywords are:
    prototype_parent - string pointing to parent prototype of this structure.
    key - string, the main object identifier.
    typeclass - string, if not set, will use `settings.BASE_OBJECT_TYPECLASS`.
    location - this should be a valid object or #dbref.
    home - valid object or #dbref.
    destination - only valid for exits (object or dbref).

    permissions - string or list of permission strings.
    locks - a lock-string.
    aliases - string or list of strings.

    ndb_<name> - value of a nattribute (the "ndb_" part is ignored).
    any other keywords are interpreted as Attributes and their values.

See the `@spawn` command and `evennia.utils.spawner` for more info.

"""
BAG = {
        "key":"saccus",
        "typeclass":"typeclasses.latin_clothing.Clothing",
        "nom_sg":["saccus"],
        "gen_sg":["sacci"],
        "gender":"2",
        "desc":"A bag",
        "clothing_type":"back",
        "can_hold":True,
        'physical':{"material":"linen","rigid":False,"volume":0.75,"mass":0.45},
        'container':{'max_vol':24,'rem_vol':24,"x":0.3,"y":0.4,"z":0.2}
        }
BANDEAU = {
        "key":"strophium",
        "typeclass":"typeclasses.latin_clothing.Clothing",
        "nom_sg":["strophium"],
        "gen_sg":["strophii"],
        "gender":"3",
        "desc":"A bandeau",
        "clothing_type":"undershirt",
        'physical':{"material":"linen","rigid":False,"volume":0.5,'mass':0.45}
        }

UNDERWEAR = {
        "key":"subligaculum",
        "typeclass":"typeclasses.latin_clothing.Clothing",
        "nom_sg":["subligaculum"],
        "gen_sg":["subligaculi"],
        "gender":"3",
        "desc":"Briefs",
        "clothing_type":"underpants",
        'physical':{"material":"linen","rigid":False,"volume":0.5,'mass':0.45}
        }

SWORD = {
        "key":"gladius",
        "typeclass":"typeclasses.objects.Object",
        "nom_sg":["gladius"],
        "gen_sg":["gladii"],
        "gender":"2",
        "desc":"A shortsword",
        "physical":{"material":"iron","rigid":True,"x":0.04,"y":0.65,"z":0.003,"mass":0.6,"volume":0.08},
        "damage":6
        }

WOOL = {
        "key":"lana",
        "typeclass":"typeclasses.objects.Object",
        "nom_sg":["lana"],
        "gen_sg":["lanae"],
        "gender":"1",
        "desc":"A small bale of wool",
        'physical':{"material":"wool","rigid":False,"volume":23,"mass":3},
        }
CLOAK = {
        "key":"pallium",
        "typeclass":"typeclasses.latin_clothing.Clothing",
        "clothing_type":"cloak",
        "nom_sg":["pallium"],
        "gen_sg":["pallii"],
        "gender":"3",
        "desc":"A simple, well-woven cloth, to wrap about your top",
        "physical":{"material":"wool","rigid":False,"x":3.04,"y":1.52,"z":0.005,"mass":3,"volume":23}
        }
HAT = {
        "key":"petasus",
        "typeclass": "typeclasses.latin_clothing.Clothing",
        "clothing_type":"hat",
        "nom_sg":["petasus"],
        "gen_sg":["petasi"],
        "gender":"2",
        "desc":"A broad-brimmed, traveler's hat",
        "physical":{"material":"wool","rigid":False,"mass":0.17,"volume":2.21}
        }

SANDALS = {
        "key":"soleae",
        "typeclass":"typeclasses.latin_clothing.Clothing",
        "clothing_type":"shoes",
        "nom_sg":["soleae"],
        "gen_sg":["solearum"],
        "gender":"1",
        "desc":"A pair of simple sandals",
        "physical":{"material":"leather","rigid":True,"x":0.107,"y":0.253,"z":0.0026,"mass":0.48,"volume":0.07}
        }

TUNIC = {
        "key":"tunica",
        "typeclass":"typeclasses.latin_clothing.Clothing",
        "clothing_type":"fullbody",
        "nom_sg":["tunica"],
        "gen_sg":["tunicae"],
        "gender":"1",
        "desc":"A sleeveless, knee-length tunic",
        "physical":{"material":"linen","rigid":False,"mass":1,"volume":2}
        }

LAMP = {
        "key":"lumen",
        "typeclass":"typeclasses.myobjects.Flammable",
        "nom_sg":["lumen"],
        "gen_sg":["luminis"],
        "gender":"3",
        "desc":"a small, simple, terracotta oil lamp",
        "physical":{"material":"clay","rigid":True,"mass":0.15,"volume":0.07}
        }
# from random import randint
#
# GOBLIN = {
# "key": "goblin grunt",
# "health": lambda: randint(20,30),
# "resists": ["cold", "poison"],
# "attacks": ["fists"],
# "weaknesses": ["fire", "light"]
# }
#
# GOBLIN_WIZARD = {
# "prototype_parent": "GOBLIN",
# "key": "goblin wizard",
# "spells": ["fire ball", "lighting bolt"]
# }
#
# GOBLIN_ARCHER = {
# "prototype_parent": "GOBLIN",
# "key": "goblin archer",
# "attacks": ["short bow"]
# }
#
# This is an example of a prototype without a prototype
# (nor key) of its own, so it should normally only be
# used as a mix-in, as in the example of the goblin
# archwizard below.
# ARCHWIZARD_MIXIN = {
# "attacks": ["archwizard staff"],
# "spells": ["greater fire ball", "greater lighting"]
# }
#
# GOBLIN_ARCHWIZARD = {
# "key": "goblin archwizard",
# "prototype_parent" : ("GOBLIN_WIZARD", "ARCHWIZARD_MIXIN")
# }
