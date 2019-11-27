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

######################################################################
# Evennia base server config
######################################################################

# This is the name of your game. Make it catchy!
SERVERNAME = "O Tempora, O Mores"
GAME_SLOGAN = "Adventures in Latin"
TELNET_ENABLED = False
ALLOWED_HOSTS = ["otemporaomor.es","155.133.131.65"]
WEBSERVER_PORTS = [(80, 4005)]
WEBSERVER_INTERFACES = ["155.133.131.65"]
TIME_FACTOR = 6.0
MULTISESSION_MODE = 2
MAX_NR_CHARACTERS = 5
DEBUG = True
INSTALLED_APPS += ('web.chargen','nocaptcha_recaptcha')
NORECAPTCHA_SITE_KEY = '6Lc1-8QUAAAAAAeoIIemPrC5xJH5AB14l3zq-mWr'
NORECAPTCHA_SECRET_KEY = '6Lc1-8QUAAAAAEouvVA5tuNYefT9X_myaO9ZHLoo'

######################################################################
# Settings given in secret_settings.py override those in this file.
######################################################################
try:
    from server.conf.secret_settings import *
except ImportError:
    print("secret_settings.py file not found or failed to import.")
