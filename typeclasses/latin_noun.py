# file mygame/typeclasses/latin_noun.py

from evennia import DefaultObject
# adding the following for colors in names for pluralization
from evennia.utils import ansi

class LatinNoun(DefaultObject):

    def at_first_save(self):
        """
        This is called by the typeclass system whenever an instance of
        this class is saved for the first time. It is a generic hook
        for calling the startup hooks for the various game entities.
        When overloading you generally don't overload this but
        overload the hooks called by this method.

        """
        self.basetype_setup()
        # moving the below line to just before basetype_posthook
        # at the bottom of this defenitiion
        # self.at_object_creation()

        if hasattr(self, "_createdict"):
            # this will only be set if the utils.create function
            # was used to create the object. We want the create
            # call's kwargs to override the values set by hooks.
            cdict = self._createdict
            updates = []
            if not cdict.get("key"):
                if not self.db_key:
                    self.db_key = "#%i" % self.dbid
                    updates.append("db_key")
            elif self.key != cdict.get("key"):
                updates.append("db_key")
                self.db_key = cdict["key"]
            if cdict.get("location") and self.location != cdict["location"]:
                self.db_location = cdict["location"]
                updates.append("db_location")
            if cdict.get("home") and self.home != cdict["home"]:
                self.home = cdict["home"]
                updates.append("db_home")
            if cdict.get("destination") and self.destination != cdict["destination"]:
                self.destination = cdict["destination"]
                updates.append("db_destination")
            if updates:
                self.save(update_fields=updates)

            if cdict.get("permissions"):
                self.permissions.batch_add(*cdict["permissions"])
            if cdict.get("locks"):
                self.locks.add(cdict["locks"])
            if cdict.get("aliases"):
                self.aliases.batch_add(*cdict["aliases"])
            if cdict.get("location"):
                cdict["location"].at_object_receive(self, None)
                self.at_after_move(None)
            if cdict.get("tags"):
                # this should be a list of tags, tuples (key, category) or (key, category, data)
                self.tags.batch_add(*cdict["tags"])
            if cdict.get("attributes"):
                # this should be tuples (key, val, ...)
                self.attributes.batch_add(*cdict["attributes"])
            if cdict.get("nattributes"):
                # this should be a dict of nattrname:value
                for key, value in cdict["nattributes"]:
                    self.nattributes.add(key, value)

            del self._createdict

        self.at_object_creation()
        self.basetype_posthook_setup()

# adding the pluralization rules; so far they will only work for
# nominative plurals for when you look in a new room; not sure
# what to do with other plural functionality

    def get_numbered_name(self, count, looker, **kwargs):
        """ 
        Return the numbered (Singular, plural) forms of this object's key.
        This is by default called by return_appearance and is used for
        grouping multiple same-named of this object. Note that this will
        be called on *every* member of a group even though the plural name
        will be only shown once. Also the singular display version, such as
        'an apple', 'a tree' is determined from this method.

        Args:
            count (int): Number of objects of this type
            looker (Object): Onlooker. Not used by default
        Kwargs:
            key (str): Optional key to pluralize, if given, use this instead of
            the object's key
        Returns:
            singular (str): The singular form to display
            plural (str): The determined plural form of the key, including count.
        """
        key = kwargs.get("key", self.key)
        key = ansi.ANSIString(key) # This is needed to allow inflection of colored names
        plural = self.db.nom_pl
        plural = "%s %s" % (count, plural)
        singular = self.db.nom_sg
        if not self.aliases.get(plural, category="plural_key"):
            # We need to wipe any old plurals/an/a in case key changed in the interim
            self.aliases.clear(category="plural_key")
            self.aliases.add(plural, category="plural_key")
            # save the singular form as an alias here too so we can display "an egg"
            # and also look at "an egg".
            self.aliases.add(singular, category="plural_key")
        return singular, plural

    def at_say(
        self,
        message,
        msg_self=None,
        msg_location=None,
        receivers=None,
        msg_receivers=None,
        **kwargs,
    ):
        """
        Display the actual say (or whisper) of self.

        This hook should display the actual say/whisper of the object in its
        location.  It should both alert the object (self) and its
        location that some text is spoken.  The overriding of messages or
        `mapping` allows for simple customization of the hook without
        re-writing it completely.

        Args:
            message (str): The message to convey.
            msg_self (bool or str, optional): If boolean True, echo `message` to self. If a string,
                return that message. If False or unset, don't echo to self.
            msg_location (str, optional): The message to echo to self's location.
            receivers (Object or iterable, optional): An eventual receiver or receivers of the message
                (by default only used by whispers).
            msg_receivers(str): Specific message to pass to the receiver(s). This will parsed
                with the {receiver} placeholder replaced with the given receiver.
        Kwargs:
            whisper (bool): If this is a whisper rather than a say. Kwargs
                can be used by other verbal commands in a similar way.
            mapping (dict): Pass an additional mapping to the message.

        Notes:


            Messages can contain {} markers. These are substituted against the values
            passed in the `mapping` argument.

                msg_self = 'You say: "{speech}"'
                msg_location = '{object} says: "{speech}"'
                msg_receivers = '{object} whispers: "{speech}"'

            Supported markers by default:
                {self}: text to self-reference with (default 'You')
                {speech}: the text spoken/whispered by self.
                {object}: the object speaking.
                {receiver}: replaced with a single receiver only for strings meant for a specific
                    receiver (otherwise 'None').
                {all_receivers}: comma-separated list of all receivers,
                                 if more than one, otherwise same as receiver
                {location}: the location where object is.

        """
        # Need to split the statement into two parts if there's more than 1 word
        # Having a problem with displaying speaker's name; changing 'object' to 'self.key'
        sentence = message.strip()
        words = sentence.split(' ')
        speeches = [f'"{words[0]}", inquis.',f'{self.key} "{words[0]}" inquit.']
        first = words[0]
        if len(words) > 1:
            rest = ' '.join(words[1:])
            speeches = [f'"{words[0]}" inquis "{rest}"',f'{self.key} "{words[0]}" inquit "{rest}"']    
        # Added the above on 11/24
        msg_type = "say"
        if kwargs.get("whisper", False):
            # whisper mode
            msg_type = "whisper"
            msg_self = (
                '{self} whisper to {all_receivers}, "{speech}"' if msg_self is True else msg_self
            )
            msg_receivers = msg_receivers or '{object} whispers: "{speech}"'
            msg_location = None
        else:
            # altering the commented out line immediately below to the line below that
            # msg_self = '{self} say, "{speech}"' if msg_self is True else msg_self
            msg_self = speeches[0] if msg_self is True else msg_self
            # altering the immediately below commented line
            # msg_location = msg_location or '{object} says, "{speech}"'
            msg_location = msg_location or speeches[1]
            msg_receivers = msg_receivers or message

        custom_mapping = kwargs.get("mapping", {})
        receivers = make_iter(receivers) if receivers else None
        location = self.location

        if msg_self:
            self_mapping = {
                "self": "You",
                "object": self.get_display_name(self),
                "location": location.get_display_name(self) if location else None,
                "receiver": None,
                "all_receivers": ", ".join(recv.get_display_name(self) for recv in receivers)
                if receivers
                else None,
                "speech": message,
            }
            self_mapping.update(custom_mapping)
            self.msg(text=(msg_self.format(**self_mapping), {"type": msg_type}), from_obj=self)

        if receivers and msg_receivers:
            receiver_mapping = {
                "self": "You",
                "object": None,
                "location": None,
                "receiver": None,
                "all_receivers": None,
                "speech": message,
            }
            for receiver in make_iter(receivers):
                individual_mapping = {
                    "object": self.get_display_name(receiver),
                    "location": location.get_display_name(receiver),
                    "receiver": receiver.get_display_name(receiver),
                    "all_receivers": ", ".join(recv.get_display_name(recv) for recv in receivers)
                    if receivers
                    else None,
                }
                receiver_mapping.update(individual_mapping)
                receiver_mapping.update(custom_mapping)
                receiver.msg(
                    text=(msg_receivers.format(**receiver_mapping), {"type": msg_type}),
                    from_obj=self,
                )

        if self.location and msg_location:
            location_mapping = {
                "self": "You",
                "object": self,
                "location": location,
                "all_receivers": ", ".join(str(recv) for recv in receivers) if receivers else None,
                "receiver": None,
                "speech": message,
            }
            location_mapping.update(custom_mapping)
            exclude = []
            if msg_self:
                exclude.append(self)
            if receivers:
                exclude.extend(receivers)
            self.location.msg_contents(
                text=(msg_location, {"type": msg_type}),
                from_obj=self,
                exclude=exclude,
                mapping=location_mapping,
            )

        destination.msg_contents(string, exclude=(self,), mapping=mapping)
