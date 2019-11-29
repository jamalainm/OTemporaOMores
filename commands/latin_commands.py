"""
General Character commands usually available to all characters
"""
import re
from django.conf import settings
from evennia.utils import utils, evtable
from evennia.typeclasses.attributes import NickTemplateInvalid

COMMAND_DEFAULT_CLASS = utils.class_from_module(settings.COMMAND_DEFAULT_CLASS)
# Added for dealing with multiple objects

# limit symbol import for API
__all__ = (
    "CmdHome",
    "CmdLook",
    "CmdNick",
    "CmdInventory",
    "CmdSetDesc",
    "CmdGet",
    "CmdDrop",
    "CmdGive",
    "CmdSay",
    "CmdWhisper",
    "CmdPose",
    "CmdAccess",
)

def which_one(args,caller,stuff):
    if '-' in args:
        thing = args.split('-')
        args = thing[-1].strip().lower()
        # get the contents of the room
#        everything = stuff
        # identify what items are the same AND match the intended case
        same = []
        for item in stuff:
            characteristics = item.aliases.all()
            [x.lower() for x in characteristics]
            if args in characteristics:
                same.append(item)
        # Return feedback if a number higher than the number of matches
        # was provided
        if len(same) == 0:
            caller.msg("Non invenisti!")
            return None, args
        if len(same) < int(thing[0]):
            caller.msg(f"Non sunt {thing[0]}, sed {len(same)}!")
            return None, args
        # match the number with the item
        target = same[int(thing[0])-1]
        return target, args
    else:
        same = []
        args = args.lower()
        for item in stuff:
            characteristics = item.aliases.all()
            [x.lower() for x in characteristics]
            if args in characteristics:
                same.append(item)
        if len(same) == 0:
            caller.msg("Non invenisti!")
            return None, args
        elif len(same) != 1:
            caller.msg(f"Sunt {len(same)}. Ecce:")
            for index,item in enumerate(same):
                caller.msg(f"{index + 1}-{item}")
            return None, args
        else:
            target = same[0]
        return target, args

class CmdHome(COMMAND_DEFAULT_CLASS):
    """
    move to your character's home location

    Usage:
      home

    Teleports you to your home location.
    """

    key = "home"
    locks = "cmd:perm(home) or perm(Builder)"
    arg_regex = r"$"

    def func(self):
        """Implement the command"""
        caller = self.caller
        home = caller.home
        if not home:
            caller.msg("You have no home!")
        elif home == caller.location:
            caller.msg("You are already home!")
        else:
            caller.msg("There's no place like home ...")
            caller.move_to(home)


class CmdLook(COMMAND_DEFAULT_CLASS):
    """
    look at location or object

    Usage:
      aspice
      aspice <obj>
      aspice *<account>

    Observes your location or objects in your vicinity.
    """

    key = "aspice"
    locks = "cmd:all()"
    arg_regex = r"\s|$"
    help_category = 'Latin'

    def func(self):
        """
        Handle the looking.
        """
        caller = self.caller
        if not self.args:
            target = caller.location
            if not target:
                caller.msg("Nihil est quod aspicere potes!")
                return
        else:
            stuff = caller.location.contents + caller.contents
            target, self.args = which_one(self.args,caller,stuff)
            if not target:
                return
        if self.args.strip().lower() != target.db.acc_sg.lower() and self.args:
            self.msg(f"(Did you mean '{target.db.acc_sg}'?)")
            return
        self.msg((caller.at_look(target), {"type": "look"}), options=None)

class CmdInventory(COMMAND_DEFAULT_CLASS):
    """
    view inventory

    Usage:
      habeo

    Shows your inventory.
    """

    key = "habeo"
    locks = "cmd:all()"
    arg_regex = r"$"
    help_category = 'Latin'

    def func(self):
        """check inventory"""
        items = self.caller.contents
        if not items:
            string = "Nihil habes."
        else:
            table = self.styled_table(border="header")
            for item in items:
                table.add_row("|C%s|n" % item.name, item.db.desc or "")
            string = "|wEcce:\n%s" % table
        self.caller.msg(string)


class CmdGet(COMMAND_DEFAULT_CLASS):
    """
    pick up something

    Usage:
      cape <rem>

    Picks up an object from your location and puts it in
    your inventory.
    """

    key = "cape"
    locks = "cmd:all()"
    arg_regex = r"\s|$"
    help_category = 'Latin'

    def func(self):
        """implements the command."""
        # try to duplicate 'try_num_prefixes' from 'evennia/commands/cmdparser.py'
        
        caller = self.caller

        if not self.args:
            caller.msg("Quid capere velis?")
            return
        stuff = caller.location.contents
        obj, self.args = which_one(self.args,caller,stuff)
        if not obj:
            return
        if obj.db.acc_sg.lower() != self.args.strip().lower():
            self.msg(f"(Did you mean '{obj.db.acc_sg}'?)")
            return
        if caller == obj:
            caller.msg("Tu te capere non potes.")
            return
        if not obj.access(caller, "get"):
            if obj.db.get_err_msg:
                caller.msg(obj.db.get_err_msg)
            else:
                caller.msg(f"Tu {obj.db.acc_sg} capere non potes.")
            return

        # calling at_before_get hook method
        if not obj.at_before_get(caller):
            return

        obj.move_to(caller, quiet=True)
        caller.msg("%s cepisti." % obj.db.acc_sg)
        caller.location.msg_contents("%s %s cepit." % (caller.name, obj.db.acc_sg), exclude=caller)
        # calling at_get hook method
        obj.at_get(caller)


class CmdDrop(COMMAND_DEFAULT_CLASS):
    """
    Get rid of something

    Usage:
      relinque <rem>

    Lets you drop an object from your inventory into the
    location you are currently in.
    """

    key = "relinque"
    locks = "cmd:all()"
    arg_regex = r"\s|$"
    help_category = 'Latin'

    def func(self):
        """Implement command"""

        caller = self.caller
        if not self.args:
            caller.msg("Quid relinquere velis?") # What would you like to give up?
            return

        # Because the DROP command by definition looks for items
        # in inventory, call the search function using location = caller
#        obj = caller.search(
#            self.args,
#            location=caller,
#            nofound_string="You aren't carrying %s." % self.args,
#            multimatch_string="You carry more than one %s:" % self.args,
#        )
        stuff = caller.contents
        obj, self.args = which_one(self.args,caller,stuff)
        if not obj:
            return
        if obj.db.acc_sg.lower() != self.args.strip().lower():
            self.msg(f"(Did you mean '{obj.db.acc_sg}'?)")
            return

        # Call the object script's at_before_drop() method.
        if not obj.at_before_drop(caller):
            return

        obj.move_to(caller.location, quiet=True)
        caller.msg("%s reliquisti." % (obj.db.acc_sg,)) # You have given X up
        caller.location.msg_contents("%s %s reliquit." % (caller.name, obj.name), exclude=caller)
        # Call the object script's at_drop() method.
        obj.at_drop(caller)


class CmdGive(COMMAND_DEFAULT_CLASS):
    """
    give away something to someone

    Usage:
      da <rem> <alicui>

    Gives an item from your inventory to another character,
    placing it in their inventory.
    """

    key = "da"
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """Implement give"""

        caller = self.caller
        if not self.args:
            caller.msg("Usage: da <rem> <alicui>")
            return
        # get the various arguments
        objects = self.args.split(' ')
        for thing in objects:
            if not thing:
                objects.remove(thing)
        # require 2 arguments
        if len(objects) != 2:
            caller.msg("Usage: da <rem> <alicui>")
            return
        # create the pool of things to search
        external = caller.location.contents
        for noun in external:
            if not noun.db.nom_sg:
                external.remove(noun)
        possessions = caller.contents
        stuff = external + possessions
        # see if first argument is in either pool
        thing1, arg1 = which_one(objects[0],caller,stuff)
        arg1 = arg1.lower()
        if not thing1:
            return
        # see if second argument is in either pool
        thing2, arg2 = which_one(objects[1],caller,stuff)
        arg2 = arg2.lower()
        if not thing2:
            return
        # make a list of the object forms of the inventory:
        accusatives = []
        for possession in possessions:
            if possession:
                accusatives.append(possession.db.acc_sg.lower())
        # make a list of the dative forms of the things outside of the inventory
        datives = []
        for extern in external:
            if extern:
                datives.append(extern.db.dat_sg.lower())

        # check grammar

        if thing1 in possessions and thing2 in external:
            if arg1 not in accusatives:
                caller.msg(f"(Did you mean '{thing1.db.acc_sg}'?)")
                return
            elif arg2 not in datives:
                caller.msg(f"(Did you mean '{thing2.db.dat_sg}'?)")
                return
            else:
                direct_object = thing1
                indirect_object = thing2
        elif thing1 in external and thing2 in possessions:
            if arg1 not in datives:
                caller.msg(f"(Did you mean '{thing1.db.dat_sg}'?)")
                return
            if arg2 not in accusatives:
                caller.msg(f"(Did you mean '{thing2.db.acc_sg}'?)")
                return
            else:
                direct_object = thing2
                indirect_object = thing1
        else:
            caller.msg("Usage: da <rem> <alicui>")
            return

        to_give = direct_object
        
        target = indirect_object
        if not (to_give and target):
            return
        if target == caller:
            caller.msg("Tu %s tibi dedisti." % to_give.db.acc_sg)
            return
        if not to_give.location == caller:
            caller.msg("%s in manibus non habes." % to_give.db.acc_sg)
            return

        # calling at_before_give hook method
        if not to_give.at_before_give(caller, target):
            return

        # give object
        caller.msg("%s %s dedisti." % (to_give.db.acc_sg, target.db.dat_sg))
        to_give.move_to(target, quiet=True)
        target.msg("%s %s tibi dedit." % (caller.key, to_give.db.acc_sg))
        # Call the object script's at_give() method.
        to_give.at_give(caller, target)


class CmdSetDesc(COMMAND_DEFAULT_CLASS):
    """
    describe yourself

    Usage:
      setdesc <description>

    Add a description to yourself. This
    will be visible to people when they
    look at you.
    """

    key = "setdesc"
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """add the description"""

        if not self.args:
            self.caller.msg("You must add a description.")
            return

        self.caller.db.desc = self.args.strip()
        self.caller.msg("You set your description.")


class CmdSay(COMMAND_DEFAULT_CLASS):
    """
    speak as your character

    Usage:
      dic <message>

    Talk to those in your current location.
    """

    key = "dic"
    aliases = ['"', "'"]
    locks = "cmd:all()"

    def func(self):
        """Run the say command"""

        caller = self.caller

        if not self.args:
            caller.msg("Say what?")
            return

        speech = self.args

        # Calling the at_before_say hook on the character
        speech = caller.at_before_say(speech)

        # If speech is empty, stop here
        if not speech:
            return

        # Call the at_after_say hook on the character
        caller.at_say(speech, msg_self=True)


class CmdWhisper(COMMAND_DEFAULT_CLASS):
    """
    Speak privately as your character to another

    Usage:
      whisper <character> = <message>
      whisper <char1>, <char2> = <message>

    Talk privately to one or more characters in your current location, without
    others in the room being informed.
    """

    key = "whisper"
    locks = "cmd:all()"

    def func(self):
        """Run the whisper command"""

        caller = self.caller

        if not self.lhs or not self.rhs:
            caller.msg("Usage: whisper <character> = <message>")
            return

        receivers = [recv.strip() for recv in self.lhs.split(",")]

        receivers = [caller.search(receiver) for receiver in set(receivers)]
        receivers = [recv for recv in receivers if recv]

        speech = self.rhs
        # If the speech is empty, abort the command
        if not speech or not receivers:
            return

        # Call a hook to change the speech before whispering
        speech = caller.at_before_say(speech, whisper=True, receivers=receivers)

        # no need for self-message if we are whispering to ourselves (for some reason)
        msg_self = None if caller in receivers else True
        caller.at_say(speech, msg_self=msg_self, receivers=receivers, whisper=True)


class CmdPose(COMMAND_DEFAULT_CLASS):
    """
    strike a pose

    Usage:
      pose <pose text>
      pose's <pose text>

    Example:
      pose is standing by the wall, smiling.
       -> others will see:
      Tom is standing by the wall, smiling.

    Describe an action being taken. The pose text will
    automatically begin with your name.
    """

    key = "pose"
    aliases = [":", "emote"]
    locks = "cmd:all()"

    def parse(self):
        """
        Custom parse the cases where the emote
        starts with some special letter, such
        as 's, at which we don't want to separate
        the caller's name and the emote with a
        space.
        """
        args = self.args
        if args and not args[0] in ["'", ",", ":"]:
            args = " %s" % args.strip()
        self.args = args

    def func(self):
        """Hook function"""
        if not self.args:
            msg = "What do you want to do?"
            self.caller.msg(msg)
        else:
            msg = "%s%s" % (self.caller.name, self.args)
            self.caller.location.msg_contents(text=(msg, {"type": "pose"}), from_obj=self.caller)


class CmdAccess(COMMAND_DEFAULT_CLASS):
    """
    show your current game access

    Usage:
      access

    This command shows you the permission hierarchy and
    which permission groups you are a member of.
    """

    key = "access"
    aliases = ["groups", "hierarchy"]
    locks = "cmd:all()"
    arg_regex = r"$"

    def func(self):
        """Load the permission groups"""

        caller = self.caller
        hierarchy_full = settings.PERMISSION_HIERARCHY
        string = "\n|wPermission Hierarchy|n (climbing):\n %s" % ", ".join(hierarchy_full)

        if self.caller.account.is_superuser:
            cperms = "<Superuser>"
            pperms = "<Superuser>"
        else:
            cperms = ", ".join(caller.permissions.all())
            pperms = ", ".join(caller.account.permissions.all())

        string += "\n|wYour access|n:"
        string += "\nCharacter |c%s|n: %s" % (caller.key, cperms)
        if hasattr(caller, "account"):
            string += "\nAccount |c%s|n: %s" % (caller.account.key, pperms)
        caller.msg(string)
