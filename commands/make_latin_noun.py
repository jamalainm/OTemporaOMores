# file mygame/commands/make_latin_noun.py

from evennia import Command
from evennia import create_object
# Redefining ObjManipCommand for room building
from evennia.commands.default.building import ObjManipCommand
#from evennia.utils.utils import class_from_module
from django.conf import settings
#COMMAND_DEFAULT_CLASS = class_from_module(settings.COMMAND_DEFAULT_CLASS)
#
#class ObjManipCommand(COMMAND_DEFAULT_CLASS):
#    """
#    This is a parent class for some of the defining objmanip commands
#    since they tend to have some more variables to define new objects.
#
#    Each object definition can have several components. First is
#    always a name, followed by an optional alias list and finally an
#    some optional data, such as a typeclass or a location. A comma ','
#    separates different objects. Like this:
#
#        name1;alias;alias;alias:option, name2;alias;alias ...
#
#    Spaces between all components are stripped.
#
#    A second situation is attribute manipulation. Such commands
#    are simpler and offer combinations
#
#        objname/attr/attr/attr, objname/attr, ...
#
#    """
#
#    # OBS - this is just a parent - it's not intended to actually be
#    # included in a commandset on its own!
#
#    def parse(self):
#        """
#        We need to expand the default parsing to get all
#        the cases, see the module doc.
#        """
#        # get all the normal parsing done (switches etc)
#        super().parse()
#
#        obj_defs = ([], [])  # stores left- and right-hand side of '='
#        obj_attrs = ([], [])  # "
#
#        for iside, arglist in enumerate((self.lhslist, self.rhslist)):
#            # lhslist/rhslist is already split by ',' at this point
#            for objdef in arglist:
#                aliases, option, attrs = [], None, []
#                if ":" in objdef:
#                    objdef, option = [part.strip() for part in objdef.rsplit(":", 1)]
#                if ";" in objdef:
#                    objdef, aliases = [part.strip() for part in objdef.split(";", 1)]
#                    aliases = [alias.strip() for alias in aliases.split(";") if alias.strip()]
#                if "/" in objdef:
#                    objdef, attrs = [part.strip() for part in objdef.split("/", 1)]
#                    attrs = [part.strip().lower() for part in attrs.split("/") if part.strip()]
#                # store data
#                obj_defs[iside].append({"name": objdef, "option": option, "aliases": aliases})
#                obj_attrs[iside].append({"name": objdef, "attrs": attrs})
#
#        # store for future access
#        self.lhs_objs = obj_defs[0]
#        self.rhs_objs = obj_defs[1]
#        self.lhs_objattr = obj_attrs[0]
#        self.rhs_objattr = obj_attrs[1]

class CmdMakeLatinObject(Command):
    """
    Create a latin object through a dialog

    Usage:
        +latin_object <nominative>
        <confirm nominative>
        <establish genitive>
        <establish gender>

    For the future, it would be nice to
    have some checks to make sure the
    genitive is suitable for this
    nominative form

    Also need to think about gender

    Consider using evmenu to for this
    dialog process
    """

    key = "+latin_object"
    locks = "cmd:perm(Builders)"
    help_category = 'Latin'

    def func(self):

        caller = self.caller

        args = self.args.strip()
        # Make sure that we just have a single word
        if ' ' in args:
            caller.msg("At this point nouns may only be single words without spaces")
            return
        # Verify that the nominative is acceptable
        while True:
            answer = yield(f"Is '{args}' an acceptible name? [(Y)es/(N)o] ")
            if answer.strip().lower() in ('yes', 'y'):
                break
            else:
                caller.msg("Okay. Start over.")
                return
        nominative = args

        # Get the genitive form
        genitive = ''
        while True:
            genitive = yield(f"What is the genitive form for '{nominative}'? ")
            if genitive[-2:] in ('ae','is','us') or genitive[-1] == 'i':
                answer = yield(f"Is '{genitive}' an acceptible genitive form for '{nominative}'? [(Y)es/(N)o] ")
                if answer.strip().lower() in ('yes', 'y'):
                    break
                else:
                    caller.msg("Okay. Start over.")
                    return
            else:
                caller.msg("I'm sorry, that is not an acceptible genitive ending. Start over")
                return

        # Get the gender
        genders = ['f','m','n']
        genders_long = ['Feminine','Masculine','Neither']
        gender = ''
        while True:
            gender = yield(f"What is the gender for '{nominative}'? [(F)eminine, (M)asculine, (N)either] ")
            if gender.strip().lower() in genders:
                gender = genders.index(gender) + 1
                answer = yield(f"Is the gender of '{nominative}' {genders_long[gender-1]}? [(Y)es/(N)o] ")
                if answer.strip().lower() in ('yes','y'):
                    break
                else:
                    caller.msg("Okay. Start over.")
            else:
                caller.msg("I'm sorry, that is not an acceptible response. Start over.")

        # Create the object
        obj = create_object('typeclasses.objects.Object',
                key = nominative,
                location = caller.location,
                attributes=[('gender',gender),('nom_sg',[nominative]),('gen_sg',[genitive])],
                )

        # Announce object's creation
        message = "%s created an object called %s"
        caller.msg(message % ('You', obj.db.nom_sg[0]))
        caller.location.msg_contents(message % (caller.key, obj.db.nom_sg[0]),exclude=caller)

class CmdMakeLatinCharacter(Command):
    """
    Create a latin object through a dialog

    Usage:
        +latin_character <nominative>
        <confirm nominative>
        <establish genitive>
        <establish gender>

    For the future, it would be nice to
    have some checks to make sure the
    genitive is suitable for this
    nominative form

    Also need to think about gender

    Consider using evmenu to for this
    dialog process
    """

    key = "+latin_character"
    locks = "cmd:perm(Builders)"
    help_category = 'Latin'

    def func(self):

        caller = self.caller

        args = self.args.strip()
        # Make sure that we just have a single word
        if ' ' in args:
            caller.msg("At this point nouns may only be single words without spaces")
            return
        # Verify that the nominative is acceptable
        while True:
            answer = yield(f"Is '{args}' an acceptible name? [(Y)es/(N)o] ")
            if answer.strip().lower() in ('yes', 'y'):
                break
            else:
                caller.msg("Okay. Start over.")
                return
        nominative = args

        # Get the genitive form
        genitive = ''
        while True:
            genitive = yield(f"What is the genitive form for '{nominative}'? ")
            if genitive[-2:] in ('ae','is','us') or genitive[-1] == 'i':
                answer = yield(f"Is '{genitive}' an acceptible genitive form for '{nominative}'? [(Y)es/(N)o] ")
                if answer.strip().lower() in ('yes', 'y'):
                    break
                else:
                    caller.msg("Okay. Start over.")
                    return
            else:
                caller.msg("I'm sorry, that is not an acceptible genitive ending. Start over")
                return

        # Get the gender
        genders = ['f','m','n']
        genders_long = ['Feminine','Masculine','Neither']
        gender = ''
        while True:
            gender = yield(f"What is the gender for '{nominative}'? [(F)eminine, (M)asculine, (N)either] ")
            if gender.strip().lower() in genders:
                gender = genders.index(gender) + 1
                answer = yield(f"Is the gender of '{nominative}' {genders_long[gender-1]}? [(Y)es/(N)o] ")
                if answer.strip().lower() in ('yes','y'):
                    break
                else:
                    caller.msg("Okay. Start over.")
            else:
                caller.msg("I'm sorry, that is not an acceptible response. Start over.")

        # Create the object
        obj = create_object('typeclasses.characters.Character',
                key = nominative,
                location = caller.location,
                attributes=[('gender',gender),('nom_sg',[nominative]),('gen_sg',[genitive])],
                )

        # Announce object's creation
        message = "%s created an character called %s"
        caller.msg(message % ('You', obj.db.nom_sg[0]))
        caller.location.msg_contents(message % (caller.key, obj.db.nom_sg[0]),exclude=caller)

class CmdMakeLatinRoom(ObjManipCommand):
    """
    build new rooms and connect them to the current location

    Usage:
      dig[/switches] <roomname>[;alias;alias...][:typeclass]
            [= <exit_to_there>[;alias][:typeclass]]
               [, <exit_to_here>[;alias][:typeclass]]

    Switches:
       tel or teleport - move yourself to the new room

    Examples:
       dig kitchen = north;n, south;s
       dig house:myrooms.MyHouseTypeclass
       dig sheer cliff;cliff;sheer = climb up, climb down

    This command is a convenient way to build rooms quickly; it creates the
    new room and you can optionally set up exits back and forth between your
    current room and the new one. You can add as many aliases as you
    like to the name of the room and the exits in question; an example
    would be 'north;no;n'.
    """

    key = "+latin_room"
    switch_options = ("teleport",)
    locks = "cmd:perm(dig) or perm(Builder)"
    help_category = "Latin"

    # lockstring of newly created rooms, for easy overloading.
    # Will be formatted with the {id} of the creating object.
    new_room_lockstring = (
        "control:id({id}) or perm(Admin); "
        "delete:id({id}) or perm(Admin); "
        "edit:id({id}) or perm(Admin)"
    )

    def func(self):
        """Do the digging. Inherits variables from ObjManipCommand.parse()"""

        caller = self.caller

        if not self.lhs:
            string = "Usage: dig[/teleport] <roomname>;<genitive>;<gender>]" "[:parent] [= <exit_there>"
            string += "[;alias;alias..][:parent]] "
            string += "[, <exit_back_here>[;alias;alias..][:parent]]"
            caller.msg(string)
            return

        room = self.lhs_objs[0]

        if not room["name"]:
            caller.msg("You must supply a new room name.")
            return
        location = caller.location
        nominative = room["name"]
        genitive = room["aliases"][0]
        gender = room["aliases"][1]

        # Create the new room
        typeclass = room["option"]
        if not typeclass:
            typeclass = settings.BASE_ROOM_TYPECLASS

        # create room
        # taking out the "create" before the "create_object"
        # new_room = create.create_object(
        new_room = create_object(
            typeclass, room["name"], attributes=[('gender',gender),('nom_sg',[nominative]),('gen_sg',[genitive])], report_to=caller
        )
        lockstring = self.new_room_lockstring.format(id=caller.id)
        new_room.locks.add(lockstring)
        alias_string = ""
        if new_room.aliases.all():
            alias_string = " (%s)" % ", ".join(new_room.aliases.all())
        room_string = "Created room %s(%s), %s of type %s." % (
            new_room,
            new_room.dbref,
            genitive,
#            gender, # no string variable in the above string for gender, don't want numeral
            typeclass,
        )

        # create exit to room

        exit_to_string = ""
        exit_back_string = ""

        if self.rhs_objs:
            to_exit = self.rhs_objs[0]
            if not to_exit["name"]:
                exit_to_string = "\nNo exit created to new room."
            elif not location:
                exit_to_string = "\nYou cannot create an exit from a None-location."
            else:
                # Build the exit to the new room from the current one
                typeclass = to_exit["option"]
                if not typeclass:
                    typeclass = settings.BASE_EXIT_TYPECLASS

                # deleting 'create.' from the command
                # new_to_exit = create.create_object(
                new_to_exit = create_object(
                    typeclass,
                    to_exit["name"],
                    location,
                    aliases=to_exit["aliases"],
                    locks=lockstring,
                    destination=new_room,
                    report_to=caller,
                )
                alias_string = ""
                if new_to_exit.aliases.all():
                    alias_string = " (%s)" % ", ".join(new_to_exit.aliases.all())
                exit_to_string = "\nCreated Exit from %s to %s: %s(%s)%s."
                exit_to_string = exit_to_string % (
                    location.name,
                    new_room.name,
                    new_to_exit,
                    new_to_exit.dbref,
                    alias_string,
                )

        # Create exit back from new room

        if len(self.rhs_objs) > 1:
            # Building the exit back to the current room
            back_exit = self.rhs_objs[1]
            if not back_exit["name"]:
                exit_back_string = "\nNo back exit created."
            elif not location:
                exit_back_string = "\nYou cannot create an exit back to a None-location."
            else:
                typeclass = back_exit["option"]
                if not typeclass:
                    typeclass = settings.BASE_EXIT_TYPECLASS
                # deleting 'create.' from the command
                # new_back_exit = create.create_object(
                new_back_exit = create_object(
                    typeclass,
                    back_exit["name"],
                    new_room,
                    aliases=back_exit["aliases"],
                    locks=lockstring,
                    destination=location,
                    report_to=caller,
                )
                alias_string = ""
                if new_back_exit.aliases.all():
                    alias_string = " (%s)" % ", ".join(new_back_exit.aliases.all())
                exit_back_string = "\nCreated Exit back from %s to %s: %s(%s)%s."
                exit_back_string = exit_back_string % (
                    new_room.name,
                    location.name,
                    new_back_exit,
                    new_back_exit.dbref,
                    alias_string,
                )
        caller.msg("%s%s%s" % (room_string, exit_to_string, exit_back_string))
        if new_room and "teleport" in self.switches:
            caller.move_to(new_room)


