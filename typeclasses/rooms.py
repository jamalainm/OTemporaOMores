"""
Room

Rooms are simple containers that has no location of their own.

"""

# from evennia import DefaultRoom
from evennia.contrib.ingame_python.typeclasses import EventRoom


# Commenting out and changing inherit to EventRoom for ingame python
# class Room(DefaultRoom):
#
class Room(EventRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See examples/object.py for a list of
    properties and methods available on all Objects.
    """

    pass
