"""
Simple turn-based combat system

Contrib - Tim Ashley Jenkins 2017

This is a framework for a simple turn-based combat system, similar
to those used in D&D-style tabletop role playing games. It allows
any character to start a fight in a room, at which point initiative
is rolled and a turn order is established. Each participant in combat
has a limited time to decide their action for that turn (30 seconds by
default), and combat progresses through the turn order, looping through
the participants until the fight ends.

Only simple rolls for attacking are implemented here, but this system
is easily extensible and can be used as the foundation for implementing
the rules from your turn-based tabletop game of choice or making your
own battle system.

To install and test, import this module's TBBasicCharacter object into
your game's character.py module:

    from evennia.contrib.turnbattle.tb_basic import TBBasicCharacter

And change your game's character typeclass to inherit from TBBasicCharacter
instead of the default:

    class Character(TBBasicCharacter):

Next, import this module into your default_cmdsets.py module:

    from evennia.contrib.turnbattle import tb_basic

And add the battle command set to your default command set:

    #
    # any commands you add below will overload the default ones.
    #
    self.add(tb_basic.BattleCmdSet())

This module is meant to be heavily expanded on, so you may want to copy it
to your game's 'world' folder and modify it there rather than importing it
in your game and using it as-is.
"""
import copy
from random import choice
from random import randint
from random import random
from evennia import DefaultCharacter, Command, default_cmds, DefaultScript
from evennia.commands.default.help import CmdHelp
# adding the following to begin translation into Latin
from commands.latin_commands import which_one
"""
----------------------------------------------------------------------------
OPTIONS
----------------------------------------------------------------------------
"""

TURN_TIMEOUT = 3  # Time before turns automatically end, in seconds
ACTIONS_PER_TURN = 1  # Number of actions allowed per turn

"""
----------------------------------------------------------------------------
COMBAT FUNCTIONS START HERE
----------------------------------------------------------------------------
"""
# Added the following function to calculates stat bonuses
def calc_bonus(stat):
    bonus = round((stat - 11 if stat % 2 else stat - 10)/2)
    return bonus

def roll_init(character):
    """
    Rolls a number between 1-1000 to determine initiative.

    Args:
        character (obj): The character to determine initiative for

    Returns:
        initiative (int): The character's place in initiative - higher
        numbers go first.

    Notes:
        By default, does not reference the character and simply returns
        a random integer from 1 to 1000.

        Since the character is passed to this function, you can easily reference
        a character's stats to determine an initiative roll - for example, if your
        character has a 'dexterity' attribute, you can use it to give that character
        an advantage in turn order, like so:

        return (randint(1,20)) + character.db.dexterity

        This way, characters with a higher dexterity will go first more often.
    """
    bonus = calc_bonus(character.db.stats['dex'])
    return random() * 20 + bonus


def get_attack(attacker, defender):
    """
    Returns a value for an attack roll.

    Args:
        attacker (obj): Character doing the attacking
        defender (obj): Character being attacked

    Returns:
        attack_value (int): Attack roll value, compared against a defense value
            to determine whether an attack hits or misses.

    Notes:
        By default, returns a random integer from 1 to 100 without using any
        properties from either the attacker or defender.

        This can easily be expanded to return a value based on characters stats,
        equipment, and abilities. This is why the attacker and defender are passed
        to this function, even though nothing from either one are used in this example.
    """
    # For this example, just return a random integer up to 100.
    # adjusting to take into account attacker's strength
    bonus = calc_bonus(attacker.db.stats['str'])
    attack_roll = randint(1, 20)
    attack_value = (attack_roll + bonus) if attack_roll > 0 else 1
#    attacker.location.msg_contents(f"{attacker.db.praenomen} rolls an {attack_roll} and gets {attack_value} with the bonus")
    return (attack_roll,attack_value)


def get_defense(attacker, defender):
    """
    Returns a value for defense, which an attack roll must equal or exceed in order
    for an attack to hit.

    Args:
        attacker (obj): Character doing the attacking
        defender (obj): Character being attacked

    Returns:
        defense_value (int): Defense value, compared against an attack roll
            to determine whether an attack hits or misses.

    Notes:
        By default, returns 50, not taking any properties of the defender or
        attacker into account.

        As above, this can be expanded upon based on character stats and equipment.
    """
    # For this example, just return 50, for about a 50/50 chance of hit.
    # adjusting to take into account defender's dex
    bonus = calc_bonus(defender.db.stats['dex'])
    defense_value = 10 + bonus
    return defense_value


def get_damage(attacker, defender):
    """
    Returns a value for damage to be deducted from the defender's HP after abilities
    successful hit.

    Args:
        attacker (obj): Character doing the attacking
        defender (obj): Character being damaged

    Returns:
        damage_value (int): Damage value, which is to be deducted from the defending
            character's HP.

    Notes:
        By default, returns a random integer from 15 to 25 without using any
        properties from either the attacker or defender.

        Again, this can be expanded upon.
    """
    # Changed damage to 5e unarmed values to match lower hp values
    good_hand = attacker.db.handedness
    weapon = False
    stuff = attacker.contents
    for thing in stuff:
        if thing.db.held:
            if thing.db.damage and thing.db.held == good_hand:
                weapon = thing
#                attacker.location.msg_contents(f"|gWEAPON|n")
    bonus = calc_bonus(attacker.db.stats['str'])
    if weapon:
        damage_value = randint(1,weapon.db.damage) + bonus
    else:
        damage_value = 1 + bonus
    damage_value = 1 if damage_value < 1 else damage_value
    return damage_value


def apply_damage(defender, damage):
    """
    Applies damage to a target, reducing their HP by the damage amount to a
    minimum of 0.

    Args:
        defender (obj): Character taking damage
        damage (int): Amount of damage being taken
    """
    # Adjusting so it recognizes my hp syntax
    defender.db.hp['current'] -= damage  # Reduce defender's HP by the damage dealt.
    # If this reduces it to 0 or less, set HP to 0.
    if defender.db.hp['current'] <= 0:
        defender.db.hp['current'] = 0


def at_defeat(defeated):
    """
    Announces the defeat of a fighter in combat.
    
    Args:
        defeated (obj): Fighter that's been defeated.
    
    Notes:
        All this does is announce a defeat message by default, but if you
        want anything else to happen to defeated fighters (like putting them
        into a dying state or something similar) then this is the place to
        do it.
    """
    # adding the following line to deal with dumb workaround to limit number
    # of initial combatants
    defeated.db.fighting = False
    defeated.location.msg_contents(f"|c%s|n |rest vict{'a' if defeated.db.gender == 1 else 'us' if defeated.db.gender == 2 else 'um'}!|n" % defeated,exclude=defeated)
    defeated.msg(f"|rTu es vict{'a' if defeated.db.gender == 1 else 'us' if defeated.db.gender == 2 else 'um'}!|n")


def resolve_attack(attacker, defender, attack_value=None, defense_value=None):
    """
    Resolves an attack and outputs the result.

    Args:
        attacker (obj): Character doing the attacking
        defender (obj): Character being attacked

    Notes:
        Even though the attack and defense values are calculated
        extremely simply, they are separated out into their own functions
        so that they are easier to expand upon.
    """
    # get the attacker's weapon
    good_hand = attacker.db.handedness
    has_weapon = False
    stuff = attacker.contents
    weapon = ''
    for thing in stuff:
        if thing.db.held:
            if thing.db.held == good_hand:
                weapon = thing.db.abl_sg
    if not weapon:
        weapon = 'manu'

    # Get an attack roll from the attacker.
    if not attack_value:
        attack_roll,attack_value = get_attack(attacker, defender)
    # Get a defense value from the defender.
    if not defense_value:
        defense_value = get_defense(attacker, defender)
    # If the attack value is lower than the defense value, miss. Otherwise, hit.
    if (attack_value < defense_value or attack_roll == 1) and attack_roll != 20:
        attacker.location.msg_contents("|c%s|n |c%s|n |w%s|n |gnon percussit|n!" % (attacker, defender.db.acc_sg,weapon),exclude=(attacker,defender))
        attacker.msg("|cTu|n |y%s|n |w%s|n |rnon percussisti|n!" % (defender.db.acc_sg,weapon))
        defender.msg("|y%s|n te |w%s|n |gnon percussit|n!" % (attacker,weapon))
    else:
        if attack_roll == 20:
            damage_value = 2 * (get_damage(attacker, defender))  # Calculate damage value.
        else:
            damage_value = get_damage(attacker, defender)  # Calculate damage value.
        # Announce damage dealt and apply damage.
        attacker.location.msg_contents("|c%s|n |c%s|n |w%s|n |rpercussit|n!" % (attacker, defender.db.acc_sg,weapon),exclude=(attacker,defender))
        attacker.msg("|cTu|n |y%s|n |w%s|n |gpercussisti|n!" % (defender.db.acc_sg,weapon))
        defender.msg("|y%s|n te |w%s|n |rpercussit|n!" % (attacker,weapon))
        
        apply_damage(defender, damage_value)
        # If defender HP is reduced to 0 or less, call at_defeat.
        # Adjusting so that script recognizes my hp syntax
        if defender.db.hp['current'] <= 0:
            at_defeat(defender)
            # adding the following to deal with my dumb workaround to limit
            # initial number of combatants
            defender.db.fighting = False


def combat_cleanup(character):
    """
    Cleans up all the temporary combat-related attributes on a character.

    Args:
        character (obj): Character to have their combat attributes removed

    Notes:
        Any attribute whose key begins with 'combat_' is temporary and no
        longer needed once a fight ends.
    """
    for attr in character.attributes.all():
        if attr.key[:7] == "combat_":  # If the attribute name starts with 'combat_'...
            character.attributes.remove(key=attr.key)  # ...then delete it!
        # adding the next line to deal with my dumb workaround to limit
        # initial number of fighters
        if attr.key == 'fighting':
            character.attributes.remove(key=attr.key)


def is_in_combat(character):
    """
    Returns true if the given character is in combat.

    Args:
        character (obj): Character to determine if is in combat or not

    Returns:
        (bool): True if in combat or False if not in combat
    """
    return bool(character.db.combat_turnhandler)


def is_turn(character):
    """
    Returns true if it's currently the given character's turn in combat.

    Args:
        character (obj): Character to determine if it is their turn or not

    Returns:
        (bool): True if it is their turn or False otherwise
    """
    turnhandler = character.db.combat_turnhandler
    currentchar = turnhandler.db.fighters[turnhandler.db.turn]
    return bool(character == currentchar)


def spend_action(character, actions, action_name=None):
    """
    Spends a character's available combat actions and checks for end of turn.

    Args:
        character (obj): Character spending the action
        actions (int) or 'all': Number of actions to spend, or 'all' to spend all actions

    Kwargs:
        action_name (str or None): If a string is given, sets character's last action in
        combat to provided string
    """
    if action_name:
        character.db.combat_lastaction = action_name
    if actions == "all":  # If spending all actions
        character.db.combat_actionsleft = 0  # Set actions to 0
    else:
        character.db.combat_actionsleft -= actions  # Use up actions.
        if character.db.combat_actionsleft < 0:
            character.db.combat_actionsleft = 0  # Can't have fewer than 0 actions
    character.db.combat_turnhandler.turn_end_check(character)  # Signal potential end of turn.


"""
----------------------------------------------------------------------------
CHARACTER TYPECLASS
----------------------------------------------------------------------------
"""


class TBBasicCharacter(DefaultCharacter):
    """
    A character able to participate in turn-based combat. Has attributes for current
    and maximum HP, and access to combat commands.
    """

# Commenting out because we have our own hp syntax
#    def at_object_creation(self):
#        """
#        Called once, when this object is first created. This is the
#        normal hook to overload for most object types.
#        """
#        # did not include this bit in typeclass, since an alternate syntax
#        # already established
#        self.db.max_hp = 100  # Set maximum HP to 100
#        self.db.hp = self.db.max_hp  # Set current HP to maximum
#        """
#        Adds attributes for a character's current and maximum HP.
#        We're just going to set this value at '100' by default.
#
#        You may want to expand this to include various 'stats' that
#        can be changed at creation and factor into combat calculations.
#        """
#
    def at_before_move(self, destination):
        """
        Called just before starting to move this object to
        destination.

        Args:
            destination (Object): The object we are moving to

        Returns:
            shouldmove (bool): If we should move or not.

        Notes:
            If this method returns False/None, the move is cancelled
            before it is even started.

        """
        # Keep the character from moving if at 0 HP or in combat.
        if is_in_combat(self):
            self.msg("Tibi pugnanti discedere non licet!")
            return False  # Returning false keeps the character from moving.
        # Adjusting so that the script recognizes my hp
        if self.db.hp['current'] <= 0:
            self.msg(f"Tu discedere non potes: es vict{'a' if self.db.gender == 1 else 'us' if self.db.gender == 2 else 'um'}!")
            # adding the following to deal with dumb workaround for limiting
            # initial number of fighters
            self.db.fighting = False
            return False
        return True


"""
----------------------------------------------------------------------------
SCRIPTS START HERE
----------------------------------------------------------------------------
"""


class TBBasicTurnHandler(DefaultScript):
    """
    This is the script that handles the progression of combat through turns.
    On creation (when a fight is started) it adds all combat-ready characters
    to its roster and then sorts them into a turn order. There can only be one
    fight going on in a single room at a time, so the script is assigned to a
    room as its object.

    Fights persist until only one participant is left with any HP or all
    remaining participants choose to end the combat with the 'disengage' command.
    """

    def at_script_creation(self):
        """
        Called once, when the script is created.
        """
        self.key = "Combat Turn Handler"
        self.interval = 1  # Once every 5 seconds
        self.persistent = True
        self.db.fighters = []

        # Add all fighters in the room with at least 1 HP to the combat."
        for thing in self.obj.contents:
            # adjusted so it would recognize my hp syntax
            if thing.db.hp:
                if thing.db.hp['current'] > 0:
                    if thing.db.fighting == True:
                        self.db.fighters.append(thing)

        # Initialize each fighter for combat
        for fighter in self.db.fighters:
            self.initialize_for_combat(fighter)

        # Add a reference to this script to the room
        self.obj.db.combat_turnhandler = self

        # Roll initiative and sort the list of fighters depending on who rolls highest to determine turn order.
        # The initiative roll is determined by the roll_init function and can be customized easily.
        ordered_by_roll = sorted(self.db.fighters, key=roll_init, reverse=True)
        self.db.fighters = ordered_by_roll

        # Announce the turn order.
        self.obj.msg_contents("|wOrdo pugnandi:|n %s " % ", ".join(obj.key for obj in self.db.fighters))

        # Start first fighter's turn.
        self.start_turn(self.db.fighters[0])

        # Set up the current turn and turn timeout delay.
        self.db.turn = 0
        self.db.timer = TURN_TIMEOUT  # Set timer to turn timeout specified in options

    def at_stop(self):
        """
        Called at script termination.
        """
        for fighter in self.db.fighters:
            combat_cleanup(fighter)  # Clean up the combat attributes for every fighter.
        self.obj.db.combat_turnhandler = None  # Remove reference to turn handler in location

    def at_repeat(self):
        """
        Called once every self.interval seconds.
        """
        currentchar = self.db.fighters[
            self.db.turn
        ]  # Note the current character in the turn order.
        self.db.timer -= self.interval  # Count down the timer.

        if self.db.timer <= 0:
            # adding following to have auto attack at timer end
            attacker = currentchar
            # In large battles defeated characters still involved
            if attacker.db.hp['current'] <= 0:
                spend_action(currentchar, "all", action_name="disengage")  # Use up one action.
                return
            # need to deal with group combat situations?
            victims = []
            for fighter in self.db.fighters:
                if fighter != currentchar and fighter.db.hp['current'] > 0:
                    victims.append(fighter)
            # commenting out for experiment in group combat and efficiency as folks
            # are defeated
#            if self.db.fighters[0] == currentchar:
#                defender = self.db.fighters[1]
#            else:
#                defender = self.db.fighters[0]
            if len(victims) == 0:
                spend_action(currentchar, "all", action_name="disengage")  # Use up one action.
                return
                    
            else:
                defender = choice(victims)
            resolve_attack(attacker,defender)
            spend_action(currentchar, "all", action_name="attack")  # Use up one action.
            # Force current character to disengage if timer runs out.
#            self.obj.msg_contents("%s's turn timed out!" % currentchar)
#            spend_action(
#                currentchar, "all", action_name="disengage"
#            )  # Spend all remaining actions.
            return
#        elif self.db.timer <= 10 and not self.db.timeout_warning_given:  # 10 seconds left
#            # Warn the current character if they're about to time out.
#            currentchar.msg("WARNING: About to time out!")
#            self.db.timeout_warning_given = True

    def initialize_for_combat(self, character):
        """
        Prepares a character for combat when starting or entering a fight.

        Args:
            character (obj): Character to initialize for combat.
        """
        combat_cleanup(character)  # Clean up leftover combat attributes beforehand, just in case.
        character.db.combat_actionsleft = (
            0
        )  # Actions remaining - start of turn adds to this, turn ends when it reaches 0
        character.db.combat_turnhandler = (
            self
        )  # Add a reference to this turn handler script to the character
        character.db.combat_lastaction = "null"  # Track last action taken in combat

    def start_turn(self, character):
        """
        Readies a character for the start of their turn by replenishing their
        available actions and notifying them that their turn has come up.

        Args:
            character (obj): Character to be readied.

        Notes:
            Here, you only get one action per turn, but you might want to allow more than
            one per turn, or even grant a number of actions based on a character's
            attributes. You can even add multiple different kinds of actions, I.E. actions
            separated for movement, by adding "character.db.combat_movesleft = 3" or
            something similar.
        """
        character.db.combat_actionsleft = ACTIONS_PER_TURN  # Replenish actions
        # Prompt the character for their turn and give some information.
        # Adjusting so script understands my hp syntax
        character.msg("|wNunc tibi agere licet! Vita: |c%i|n|w.|n" % character.db.hp['current'])

    def next_turn(self):
        """
        Advances to the next character in the turn order.
        """

        # Check to see if every character disengaged as their last action. If so, end combat.
        disengage_check = True
        for fighter in self.db.fighters:
            if (
                fighter.db.combat_lastaction != "disengage"
            ):  # If a character has done anything but disengage
                disengage_check = False
        if disengage_check:  # All characters have disengaged
            self.obj.msg_contents("|wOmnes cesserunt! Pugna peracta est!|n")
            # added this next line to remove the 'fighting' attribute
            for fighter in self.db.fighters:
                fighter.db.fighting = False
            self.stop()  # Stop this script and end combat.
            return
            
        # adding following for "flee"
        flee_check = True
        cowards = []
        hostiles = []
        for fighter in self.db.fighters:
            if fighter.db.combat_lastaction == 'flee':
                cowards.append(fighter)
                fighter.db.combat_lastaction = 'null'
#                fighter.location.msg_contents(f"cowards: {cowards}; hostiles: {hostiles}!")
            else:
                if fighter.db.hp['current'] > 0:
                    hostiles.append(fighter)
#                    fighter.location.msg_contents(f"cowards: {cowards}; hostiles: {hostiles}!")
        if len(cowards) == 0:
            flee_check = False
        if flee_check:
            if len(hostiles) <= 0:
                for fighter in self.db.fighters:
                    fighter.db.fighting = False
                self.stop()
                return
            else:
                coward = cowards[0]
                bonus = calc_bonus(coward.db.stats['dex'])
                coward_dex_check = randint(1,20) + bonus
#                coward.location.msg_contents(f"{coward} rolls a {coward_dex_check}, trying to |cflee|n!")
                for hostile in hostiles:
                    bonus = calc_bonus(hostile.db.stats['dex'])
                    hostile_dex_check = randint(1,20) + bonus
#                    hostile.location.msg_contents(f"{hostile} rolled a {hostile_dex_check}!")
                    if hostile_dex_check > coward_dex_check:
                        flee_check = False
                        coward.location.msg_contents('|rFugere non potes!|n')
                        break
                if flee_check:
                    coward.location.msg_contents(f"|r{coward} fugit|n!",exclude=coward)
                    coward.msg("|gFugisti|n!")
                    exits = [
                            o for o in coward.location.contents if o.destination
                            ]
                    escape = choice(exits)
#                    coward.location.msg_contents(f"{escape.destination}")
                    combat_cleanup(coward)
                    self.db.fighters.remove(coward)
                    escape.at_traverse(coward,escape.destination)

        # Check to see if only one character is left standing. If so, end combat.
        defeated_characters = 0
        for fighter in self.db.fighters:
            # Adjusting so the script recognizes my syntax for hp
            if fighter.db.hp['current'] == 0:
                # initial number of fighters
                # added the following to deal with dumb workaround to limit
                # now commenting out, bc combat seems to keep going for some reason
#                fighter.db.fighting = False
                defeated_characters += 1  # Add 1 for every fighter with 0 HP left (defeated)
        if defeated_characters == (
            len(self.db.fighters) - 1
        ):  # If only one character isn't defeated
            for fighter in self.db.fighters:
                # Adjusting so that script recognizes my hp syntax
                if fighter.db.hp['current'] != 0:
                    LastStanding = fighter  # Pick the one fighter left with HP remaining
            self.obj.msg_contents(f"|c%s|n |west vict{'rix' if LastStanding.db.gender == 1 else 'or'}! Pugna est peracta!|n" % LastStanding,exclude=LastStanding)
            LastStanding.msg(f"|gTu vicisti!! Pugna est peracta!|n")
            self.stop()  # Stop this script and end combat.
            # added the following to deal with my dumb work around to limit
            # number of initial fighters
            LastStanding.db.fighting = False
            return

        # Cycle to the next turn.
        currentchar = self.db.fighters[self.db.turn]
        self.db.turn += 1  # Go to the next in the turn order.
        if self.db.turn > len(self.db.fighters) - 1:
            self.db.turn = 0  # Go back to the first in the turn order once you reach the end.
        newchar = self.db.fighters[self.db.turn]  # Note the new character
        self.db.timer = TURN_TIMEOUT + self.time_until_next_repeat()  # Reset the timer.
        self.db.timeout_warning_given = False  # Reset the timeout warning.
#        self.obj.msg_contents("%s tempus egit - nunc  %s agere licet!" % (currentchar, newchar.db.dat_sg))
        self.start_turn(newchar)  # Start the new character's turn.

    def turn_end_check(self, character):
        """
        Tests to see if a character's turn is over, and cycles to the next turn if it is.

        Args:
            character (obj): Character to test for end of turn
        """
        if not character.db.combat_actionsleft:  # Character has no actions remaining
            self.next_turn()
            return

    def join_fight(self, character):
        """
        Adds a new character to a fight already in progress.

        Args:
            character (obj): Character to be added to the fight.
        """
        # Inserts the fighter to the turn order, right behind whoever's turn it currently is.
        self.db.fighters.insert(self.db.turn, character)
        # Tick the turn counter forward one to compensate.
        self.db.turn += 1
        # added next line to account for attempts at limiting number of fighters
        self.db.fighting = True
        # Initialize the character like you do at the start.
        self.initialize_for_combat(character)



"""
----------------------------------------------------------------------------
COMMANDS START HERE
----------------------------------------------------------------------------
"""


class CmdFight(Command):
    """
    Starts a fight with the target.

    Usage:
      pugna <rem>

    When you start a fight, everyone in the room who is able to
    fight is added to combat, and a turn order is randomly rolled.
    When it's your turn, you can attack other characters.
    """

    key = "pugna"
    help_category = "pugna"

    def func(self):
        """
        This performs the actual command.
        """
        here = self.caller.location
        fighters = []
        # Adding the following so that you have to specify someone to fight
        if not self.args:
            self.caller.msg("Usage: pugna <rem>")
            return
        else:
            stuff = here.contents
            target, self.args = which_one(self.args,self.caller,stuff)
            if not target:
                return
        if self.args.strip().lower() != target.db.acc_sg.lower() and self.args:
            self.caller.msg(f"(Did you mean '{target.db.acc_sg}'?)")
            return

        attacker = self.caller
        defender = target
#        defender = self.caller.search(self.args)
#        attacker.msg(f"{defender} is your target")

        if not defender:  # No valid target given.
            self.caller.msg("Quem pugnare velis?")
            return
        if not defender.db.hp:
            self.caller.msg(f"Tibi {defender.db.acc_sg} pugnare non licet!")
            return

        # Adjusting so it recognizes my hp syntax
        if not defender.db.hp['current']:  # Target object has no HP left or to begin with
            self.caller.msg(f"{defender.db.nom_sg} iam vict{'a' if defender.db.gender == 1 else 'us' if defender.db.gender == 2 else 'um'} est!")
            return

        if attacker == defender:  # Target and attacker are the same
            self.caller.msg("Tu te pugnare non potes!!")
            return

        # Adjusting so script recognizes my syntax for hp
        if not self.caller.db.hp['current']:  # If you don't have any hp
            self.caller.msg(f"Vict{'a' if self.caller.db.gender == 1 else 'us' if self.caller.db.gender == 2 else 'um'} tu pugnare non potes!")
            return
        if is_in_combat(self.caller):  # Already in a fight
            self.caller.msg("Tu iam pugnas!")
            return
        # commenting out to len(fighters) and just adding attacker and defender
#        for thing in here.contents:  # Test everything in the room to add it to the fight.
#            # Adjusting so that script recognizes my hp syntax
#            if thing.db.hp:  # If the object has HP...
#                if thing.db.hp['current'] > 0:
#                    # added this premise for the conditional
#                    if thing == self.args:
#                        fighters.append(thing)  # ...then add it to the fight.
        fighters.append(attacker)
        fighters.append(defender)
        # the following two lines are my dumb workaround for trying to limit
        # the number of initial combatants
        attacker.db.fighting = True
        defender.db.fighting = True
        if len(fighters) <= 1:  # If you're the only able fighter in the room
            self.caller.msg("Nemo est quocum tu pugnare potes!")
            return
        if here.db.combat_turnhandler:  # If there's already a fight going on...
            here.msg_contents("|c%s|n pugnam commisit!" % self.caller, exclude=self.caller)
            self.caller.msg("Tu pugnam commisi!")
            here.db.combat_turnhandler.join_fight(self.caller)  # Join the fight!
            return
        here.msg_contents("|c%s|n |c%s|n pugnare coepit!" % (self.caller,defender.db.acc_sg),exclude=(self.caller,defender))
        self.caller.msg(f"Tu |c%s|n pugnare coepisti!" % defender.db.acc_sg)
        defender.msg(f"|c{self.caller}|n te pugnare coepit!")
        # Add a turn handler script to the room, which starts combat.
        # change to this script
        here.scripts.add("world.tb_basic.TBBasicTurnHandler")
        # Remember you'll have to change the path to the script if you copy this code to your own modules!


class CmdAttack(Command):
    """
    Attacks another character.

    Usage:
      pete <rem>

    When in a fight, you may attack another character. The attack has
    a chance to hit, and if successful, will deal damage.
    """

    key = "pete"
    help_category = "pugna"

    def func(self):
        "This performs the actual command."
        "Set the attacker to the caller and the defender to the target."

        # Moving this block from before the "resolve attack" code #

        here = self.caller.location

        if not self.args:
            self.caller.msg("Usage: pugna <rem>")
            return
        else:
            stuff = here.contents
            target, self.args = which_one(self.args,self.caller,stuff)
            if not target:
                return
        if self.args.strip().lower() != target.db.acc_sg.lower() and self.args:
            self.caller.msg(f"(Did you mean '{target.db.acc_sg}'?)")
            return

        attacker = self.caller
        defender = target

        if not defender:  # No valid target given.
            self.caller.msg("Quem pugnare velis?")
            return

        # Adjusting so it recognizes my hp syntax
        if not defender.db.hp:
            self.caller.msg(f"Tibi {defender.db.acc_sg} pugnare non licet!")
            return
        if not defender.db.hp['current']:  # Target object has no HP left or to begin with
            self.caller.msg(f"{defender.db.nom_sg} iam vict{'a' if defender.db.gender == 1 else 'us' if defender.db.gender == 2 else 'um'} est!")           
            return

        if attacker == defender:  # Target and attacker are the same
            self.caller.msg("Tu te pugnare non potes!")
            return

        # The above used to be right before the "resolve attack" code #

        # the blow used to be after 'is_turn'
        # Adjusting so it recognizes my hp syntax
        if not self.caller.db.hp['current']:  # Can't attack if you have no HP.
            self.caller.msg(f"Vict{'a' if self.caller.db.gender == 1 else 'us' if self.caller.db.gender == 2 else 'um'} tu pugnare non potes!")
            return

        # after I moved the top block, the above was just after 'is_turn'

        if not is_in_combat(self.caller):  # If not in combat, can't attack.
            # Join fight if defender is already fighting
            if is_in_combat(defender):  # Already in a fight
                here.msg_contents("|c%s|n pugnam commisit!" % self.caller, exclude=(self.caller,defender))
                self.caller.msg("Tu pugnam commisisti!")
                defender.msg(f"|c%s|n tecum pugnam commisit!" % self.caller)
                here.db.combat_turnhandler.join_fight(attacker)  # Join the fight!
                return
            # start fight if defender not already fighting
            else:
                
                fighters = []
                fighters.append(attacker)
                fighters.append(defender)
                # the following two lines are my dumb workaround for trying to limit
                # the number of initial combatants
                attacker.db.fighting = True
                defender.db.fighting = True
                if len(fighters) <= 1:  # If you're the only able fighter in the room
                    self.caller.msg("Nemo est quocum pugnare potes!")
                    return
                if here.db.combat_turnhandler:  # If there's already a fight going on...
                    here.msg_contents("|c%s|n pugnam cum |c%s|n commisit!" % (self.caller,defender.db.abl_sg), exclude=(self.caller,defender))
                    self.caller.msg("Tu cum |c%s|n pugnam comisisti!" % defender.db.abl_sg)
                    defender.msg("|c%s|n tecum pugnam comisit!" % self.caller)
                    here.db.combat_turnhandler.join_fight(self.caller)  # Join the fight!
                    return
                here.msg_contents("|c%s|n pugnam cum |c%s|n commisit!" % (self.caller,defender.db.abl_sg), exclude=(self.caller,defender))
                self.caller.msg("Tu cum |c%s|n pugnam comisisti!" % defender.db.abl_sg)
                defender.msg("|c%s|n tecum pugnam comisit!" % self.caller)
                # Add a turn handler script to the room, which starts combat.
                # change to this script
                here.scripts.add("world.tb_basic.TBBasicTurnHandler")
                # Remember you'll have to change the path to the script if you copy this code to your own modules!

            # Commenting out the below so that this command can start a fight
#            self.caller.msg("You can only do that in combat. (see: help fight)")
#            return

        # Adding to deal with attacking someone not in combat
        if not is_in_combat(defender):
            here.msg_contents("|c%s|n pugnam cum |c%s|n commisit!" % (self.caller,defender.db.abl_sg), exclude=(self.caller,defender))
            self.caller.msg("Tu cum |c%s|n pugnam comisisti!" % defender.db.abl_sg)
            defender.msg("|c%s|n tecum pugnam comisit!" % self.caller)
            here.db.combat_turnhandler.join_fight(defender)  # Join the fight!
            return

        if not is_turn(self.caller):  # If it's not your turn, can't attack.
            # commenting out, since I don't think it's all that helpful
#            self.caller.msg("You can only do that on your turn.")
            return

        "If everything checks out, call the attack resolving function."
        resolve_attack(attacker, defender)
        spend_action(self.caller, 1, action_name="attack")  # Use up one action.


class CmdPass(Command):
    """
    Passes on your turn.

    Usage:
      exspecta

    When in a fight, you can use this command to end your turn early, even
    if there are still any actions you can take.
    """

    key = "exspecta"
    help_category = "pugna"

    def func(self):
        """
        This performs the actual command.
        """
        if not is_in_combat(self.caller):  # Can only pass a turn in combat.
            self.caller.msg("You can only do that in combat. (see: help fight)")
            return

        if not is_turn(self.caller):  # Can only pass if it's your turn.
#            self.caller.msg("You can only do that on your turn.")
            return

        self.caller.location.msg_contents("|c%s|n nihil egit." % self.caller, exclude=self.caller)
        self.caller.msg('Tu nihil egisti.')
        spend_action(self.caller, "all", action_name="pass")  # Spend all remaining actions.


class CmdDisengage(Command):
    """
    Passes your turn and attempts to end combat.

    Usage:
      cede

    Ends your turn early and signals that you're trying to end
    the fight. If all participants in a fight disengage, the
    fight ends.
    """

    key = "cede"
    help_category = "pugna"

    def func(self):
        """
        This performs the actual command.
        """
        if not is_in_combat(self.caller):  # If you're not in combat
            self.caller.msg("You can only do that in combat. (see: help fight)")
            return

        if not is_turn(self.caller):  # If it's not your turn
#            self.caller.msg("You can only do that on your turn.")
            return

        self.caller.location.msg_contents("|c%s|n |ycessit: pugnare non vult|n." % self.caller, exclude=self.caller)
        self.caller.msg("|yCessisti|n.")
        spend_action(self.caller, "all", action_name="disengage")  # Spend all remaining actions.
        """
        The action_name kwarg sets the character's last action to "disengage", which is checked by
        the turn handler script to see if all fighters have disengaged.
        """


class CmdRest(Command):
    """
    Recovers damage.

    Usage:
      requiesce

    Resting recovers your HP to its maximum, but you can only
    rest if you're not in a fight.
    """

    key = "requiesce"
    help_category = "pugna"

    def func(self):
        "This performs the actual command."

        if is_in_combat(self.caller):  # If you're in combat
            self.caller.msg("Tibi pugnanti requiescere non licet.")
            return

        # Adjusting so it recognizes the syntax of my hp
        self.caller.db.hp['current'] = self.caller.db.hp['max']  # Set current HP to maximum
        self.caller.location.msg_contents("|c%s|n requievit ut vitam reficeret." % self.caller,exclude=self.caller)
        self.caller.msg("Requievisti ut vitam reficeres.")
        """
        You'll probably want to replace this with your own system for recovering HP.
        """


class CmdCombatHelp(CmdHelp):
    """
    View help or a list of topics

    Usage:
      help <topic or command>
      help list
      help all

    This will search for help on commands and other
    topics related to the game.
    """

    # Just like the default help command, but will give quick
    # tips on combat when used in a fight with no arguments.

    def func(self):
        if is_in_combat(self.caller) and not self.args:  # In combat and entered 'help' alone
            self.caller.msg(
                "Available combat commands:|/"
                + "|wPete:|n Attack a target, attempting to deal damage.|/"
                + "|wExspecta:|n Pass your turn without further action.|/"
                + "|wCede:|n End your turn and attempt to end combat.|/"
                + "|wFug:|n End your turn and attempt to run away.|/"
            )
        else:
            super().func()  # Call the default help command


class CmdFlee(Command):
    """
    You do not attack, but attempt to escape.

    Usage:
      fug

    Ends your turn early and signals that you're trying to run away.
    """

    key = "fug"
    help_category = "pugna"

    def func(self):
        """
        This performs the actual command.
        """
        if not is_in_combat(self.caller):  # If you're not in combat
            self.caller.msg("You can only do that in combat. (see: help fight)")
            return

        if not is_turn(self.caller):  # If it's not your turn
#            self.caller.msg("You can only do that on your turn.")
            return

        self.caller.location.msg_contents("|c%s|n fugere conatur!" % self.caller,exclude=self.caller)
        self.caller.msg("|cFugere conaris|n!")
        spend_action(self.caller, "all", action_name="flee")  # Spend all remaining actions.
        """
        The action_name kwarg sets the character's last action to "disengage", which is checked by
        the turn handler script to see if all fighters have disengaged.
        """

class BattleCmdSet(default_cmds.CharacterCmdSet):
    """
    This command set includes all the commmands used in the battle system.
    """

    key = "DefaultCharacter"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        self.add(CmdFight())
        self.add(CmdAttack())
        self.add(CmdRest())
        self.add(CmdPass())
        self.add(CmdDisengage())
        self.add(CmdCombatHelp())
        self.add(CmdFlee())
