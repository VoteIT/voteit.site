from zope.interface import Interface
from zope.interface import Attribute


class ISupportStorage(Interface):
    """ An adapter for sites that handle storage of support requests. """
    support_storage = Attribute("Conatins the support request saved on the site")

    def __init__(context):
        """ Object needs a meeting to adapt. """
        
    def add(message, subject='', name='', email='', meeting=None):
        """ Add a support request.
        """
        
class ISupportRequest(Interface):
    """ A persistent support request. """
    created = Attribute("When it was created, in UTC time.")
    message = Attribute("The message.")
    subject = Attribute("The subject.")
    name = Attribute("The name specified.")
    email = Attribute("The email specified.")
    meeting = Attribute("The meeting the user was on if any.")

    def __init__(message, subject='', name='', email='', meeting=None):
        """ Create a support request.
        """