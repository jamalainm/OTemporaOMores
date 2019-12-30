r"""
Evennia settings file.

The available options are found in the default settings file found
here:

/home/jaalin/muddev/evennia/evennia/settings_default.py

Remember:

Don't copy more from the default file than you actually intend to
change; this will make sure that you don't overload upstream updates
unnecessarily.

When changing a setting requiring a file system path (like
path/to/actual/file.py), use GAME_DIR and EVENNIA_DIR to reference
your game folder and the Evennia library folders respectively. Python
paths (path.to.module) should be given relative to the game's root
folder (typeclasses.foo) whereas paths within the Evennia library
needs to be given explicitly (evennia.foo).

If you want to share your game dir, including its settings, you can
put secret game- or server-specific settings in secret_settings.py.

"""

# Use the defaults from Evennia unless explicitly overridden
from evennia.settings_default import *
import os

######################################################################
# Evennia base server config
######################################################################

# This is the name of your game. Make it catchy!
SERVERNAME = "O Tempora, O Mores"
GAME_SLOGAN = "Adventures in Latin"
#COMMAND_PARSER = "commands.cmdparser"
# Adding the following line so that a command prompt appears after every command
COMMAND_DEFAULT_CLASS = "commands.command.MuxCommand"
TELNET_ENABLED = True
TELNET_PORTS = [4000]
TELNET_INTERFACES = ["0.0.0.0"]
ALLOWED_HOSTS = ["otemporaomor.es","155.133.131.65"]
WEBSERVER_PORTS = [(80, 4005)]
WEBSERVER_INTERFACES = ["155.133.131.65"]
TIME_FACTOR = 6.0
MULTISESSION_MODE = 2
MAX_NR_CHARACTERS = 5
DEBUG = True
INSTALLED_APPS += ('web.chargen','nocaptcha_recaptcha')
######################################################################
# Settings given in secret_settings.py override those in this file.
######################################################################
try:
    from server.conf.secret_settings import *
except ImportError:
    print("secret_settings.py file not found or failed to import.")


try:
    # Created by the `evennia connections` wizard
    from .connection_settings import *
except ImportError:
    pass
