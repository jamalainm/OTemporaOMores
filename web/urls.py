"""
Url definition file to redistribute incoming URL requests to django
views. Search the Django documentation for "URL dispatcher" for more
help.

"""
from django.conf.urls import url, include

# default evennia patterns
from evennia.web.urls import urlpatterns

# eventual custom patterns
custom_patterns = [
    # url(r'/desired/url/', view, name='example'),
    # may want to change the first url in the future in order to
    # connect it with the webpage's link for making new characters
    url(r'^chargen/', include('web.chargen.urls')),
]

# this is required by Django.
urlpatterns = custom_patterns + urlpatterns
