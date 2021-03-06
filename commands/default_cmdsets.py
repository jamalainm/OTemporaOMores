"""
Command sets

All commands in the game must be grouped in a cmdset.  A given command
can be part of any number of cmdsets and cmdsets can be added/removed
and merged onto entities at runtime.

To create new commands to populate the cmdset, see
`commands/command.py`.

This module wraps the default command sets of Evennia; overloads them
to add/remove commands from the default lineup. You can create your
own cmdsets by inheriting from them or directly from `evennia.CmdSet`.

"""
from world import tb_basic
from evennia import default_cmds
from evennia.contrib.ingame_python.commands import CmdCallback
from commands import make_latin_noun
from commands import latin_commands
from commands import myaccount
from commands import command
# Adding the following to give clothing functionality
from typeclasses.latin_clothing import ClothedCharacterCmdSet

class CharacterCmdSet(default_cmds.CharacterCmdSet):
    """
    The `CharacterCmdSet` contains general in-game commands like `look`,
    `get`, etc available on in-game Character objects. It is merged with
    the `AccountCmdSet` when an Account puppets a Character.
    """

    key = "DefaultCharacter"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        # For ingame python, I'm commenting out the line below and
        # using the next 'super' command.
        #
        # super().at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #
        super(CharacterCmdSet, self).at_cmdset_creation()
        self.add(CmdCallback())
        self.add(make_latin_noun.CmdMakeLatinObject())
        self.add(make_latin_noun.CmdMakeLatinCharacter())
        self.add(make_latin_noun.CmdMakeLatinRoom())
        self.add(latin_commands.CmdLook())
        # Using new Clothing inventory command
        # self.add(latin_commands.CmdInventory())
        self.add(latin_commands.CmdGet())
        self.add(latin_commands.CmdDrop())
        self.add(latin_commands.CmdGive())
        self.add(ClothedCharacterCmdSet())
        self.add(latin_commands.CmdSay())
        self.add(command.CmdNPC())
        self.add(latin_commands.CmdPut())
        self.add(latin_commands.CmdGetOut())
        self.add(latin_commands.CmdLookIn())
        self.add(latin_commands.CmdHold())
        self.add(latin_commands.CmdStats())
        self.add(tb_basic.BattleCmdSet())


class AccountCmdSet(default_cmds.AccountCmdSet):
    """
    This is the cmdset available to the Account at all times. It is
    combined with the `CharacterCmdSet` when the Account puppets a
    Character. It holds game-account-specific commands, channel
    commands, etc.
    """

    key = "DefaultAccount"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super().at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #
        self.add(myaccount.CmdCharCreate())

class UnloggedinCmdSet(default_cmds.UnloggedinCmdSet):
    """
    Command set available to the Session before being logged in.  This
    holds commands like creating a new account, logging in, etc.
    """

    key = "DefaultUnloggedin"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super().at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #
        # self.add(myaccount.CmdCharCreate())

class SessionCmdSet(default_cmds.SessionCmdSet):
    """
    This cmdset is made available on Session level once logged in. It
    is empty by default.
    """

    key = "DefaultSession"

    def at_cmdset_creation(self):
        """
        This is the only method defined in a cmdset, called during
        its creation. It should populate the set with command instances.

        As and example we just add the empty base `Command` object.
        It prints some info.
        """
        super().at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #
