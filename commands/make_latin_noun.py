# file mygame/commands/make_latin_noun.py

from evennia import Command
from evennia import create_object

class CmdMakeLatinObject(Command):
    """
    Create a latin object through a dialog

    Usage:
        +create_latin_noun <nominative>
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

    key = "+create_latin_object"
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
                attributes=[('gender',gender),('nom_sg',nominative),('gen_sg',genitive)],
                tags=['latin'],
                )

        # Announce object's creation
        message = "%s created an object called %s"
        caller.msg(message % ('You', obj.db.nom_sg))
        caller.location.msg_contents(message % (caller.key, obj.db.nom_sg),exclude=caller)
