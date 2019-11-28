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

        self.tags.add('latin')

    def announce_move_from(self, destination, msg=None, mapping=None):
        """
        Called if the move is to be announced. This is
        called while we are still standing in the old
        location.

        Args:
            destination (Object): The place we are going to.
            msg (str, optional): a replacement message.
            mapping (dict, optional): additional mapping objects.

        You can override this method and call its parent with a
        message to simply change the default message.  In the string,
        you can use the following as mappings (between braces):
            object: the object which is moving.
            exit: the exit from which the object is moving (if found).
            origin: the location of the object before the move.
            destination: the location of the object after moving.

        """
        if not self.location:
            return

        # changing {origin} to {exit}
        string = msg or "{object} {exit} discessit." #, heading for {destination}."

        # Get the exit from location to destination
        location = self.location
        exits = [
            o for o in location.contents if o.location is location and o.destination is destination
        ]
        mapping = mapping or {}
        mapping.update({"character": self})

        if exits:
            exits[0].callbacks.call(
                "msg_leave", self, exits[0], location, destination, string, mapping
            )
            string = exits[0].callbacks.get_variable("message")
            mapping = exits[0].callbacks.get_variable("mapping")

        # If there's no string, don't display anything
        # It can happen if the "message" variable in events is set to None
        if not string:
            return

        super().announce_move_from(destination, msg=string, mapping=mapping)

    def announce_move_to(self, source_location, msg=None, mapping=None):
        """
        Called after the move if the move was not quiet. At this point
        we are standing in the new location.

        Args:
            source_location (Object): The place we came from
            msg (str, optional): the replacement message if location.
            mapping (dict, optional): additional mapping objects.

        You can override this method and call its parent with a
        message to simply change the default message.  In the string,
        you can use the following as mappings (between braces):
            object: the object which is moving.
            exit: the exit from which the object is moving (if found).
            origin: the location of the object before the move.
            destination: the location of the object after moving.

        """

        if not source_location and self.location.has_account:
            # This was created from nowhere and added to an account's
            # inventory; it's probably the result of a create command.
            string = "You now have %s in your possession." % self.get_display_name(self.location)
            self.location.msg(string)
            return

        # added the line below because
        origin = source_location
        # error checking
        self.location.msg(source_location)
        if source_location:
            origin = source_location.db.abl_sg
            string = msg or f"{self.db.nom_sg} ab {source_location.db.abl_sg} venit."
        else:
            string = "{character} venit."

        # adding '.db.abl_sg' to end of 'source_location' and moving from line below
        # up into the 'if source_location' conditional
        destination = self.location
        exits = []
        mapping = mapping or {}
        mapping.update({"character": self})

        if origin:
            exits = [
                o
                for o in destination.contents
                if o.location is destination and o.destination is origin
            ]
            if exits:
                exits[0].callbacks.call(
                    "msg_arrive", self, exits[0], origin, destination, string, mapping
                )
                string = exits[0].callbacks.get_variable("message")
                mapping = exits[0].callbacks.get_variable("mapping")

        # If there's no string, don't display anything
        # It can happen if the "message" variable in events is set to None
        if not string:
            return

        super().announce_move_to(source_location, msg=string, mapping=mapping)
