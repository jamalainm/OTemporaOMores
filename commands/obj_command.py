from commands.command import MuxCommand
from commands.latin_commands import which_one
from evennia import CmdSet

class CmdLight(MuxCommand):
    """
    For objects that can be light, flips on the "is lit" tag
    
    Usage: accende <rem>

    ignite something intended to be lit
    """

    key = 'accende'
    locks = 'cmd:all()'
    help_category = 'Latin'

    def func(self):
        """ 
        Handle the ignition, setting a "is_glowing" flag on it
        """
        caller = self.caller
        
        if not self.args:
            caller.msg("Usage: incende <rem>")
        else:
            stuff = caller.location.contents + caller.contents
            target, self.args = which_one(self.args,caller,stuff)
            if not target:
                return
        lower_case = [x.lower() for x in target.db.acc_sg]
        if self.args.strip().lower() not in lower_case and self.args:
            caller.msg(f"(Did you mean '{target.db.acc_sg[0]}'?)")
            return

        if not target.db.flammable:
            caller.msg(f"{target.db.nom_sg[0]} ardere non potest!")
            return
        elif target.db.is_glowing:
            caller.msg(f"{target.db.nom_sg[0]} iam ardet!")
            return

        target.db.is_glowing = True
        caller.msg(f"{target.db.acc_sg[0]} accendisti.")
        caller.location.msg_contents(f"|c{caller.key}|n {target.db.acc_sg[0]} accendit.")
            
class CmdPutOut(MuxCommand):
    """
    For objects that are lit, flips off the "is_glowing" attribute
    
    Usage: exstingue <rem>

    Exstinguish a lit light source
    """

    key = 'exstingue'
    locks = 'cmd:all()'
    help_category = 'Latin'

    def func(self):
        """ 
        Handle the dousing, setting a "is_glowing" flag to false
        """
        caller = self.caller
        
        if not self.args:
            caller.msg("Usage: incende <rem>")
        else:
            stuff = caller.location.contents + caller.contents
            target, self.args = which_one(self.args,caller,stuff)
            if not target:
                return
        lower_case = [x.lower() for x in target.db.acc_sg]
        if self.args.strip().lower() not in lower_case and self.args:
            target.msg(f"(Did you mean '{target.db.acc_sg[0]}'?)")
            return

        if not target.db.is_glowing:
            caller.msg(f"{target.db.nom_sg[0]} non ardet!")
            return

        target.db.is_glowing = False
        caller.msg(f"{target.db.acc_sg[0]} exstinxisti")
        caller.location.msg_contents(f"|c{caller.key}|n {target.db.acc_sg[0]} exstinxit.")

class FlammableCmdSet(CmdSet):
    def at_cmdset_creation(self):
        self.add(CmdLight())
        self.add(CmdPutOut())
