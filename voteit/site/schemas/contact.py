import colander
from betahaus.pyracont.decorators import schema_factory
from voteit.core.schemas.contact import ContactSchema

from voteit.site import SiteMF as _


@schema_factory('FeedbackSchema', title=_("Feedback"),
                description = _(u"Contact the VoteIT team with feedback. Please enter your email address if you want to be able to receive a reply!"))
class FeedbackSchema(ContactSchema):
    """ Feedback contact form schema. Same as contact in voteit.core """
