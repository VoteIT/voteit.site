from betahaus.pyracont.decorators import schema_factory
from voteit.core.schemas.help import ContactSchema

from voteit.site import SiteMF as _


@schema_factory('FeedbackSchema', title=_("Feedback"))
class FeedbacktSchema(ContactSchema):
    """ Feedback contact form schema. Same as contact in voteit.core """

@schema_factory('SupportSchema', title=_("Support"))
class SupportSchema(ContactSchema):
    """ Support contact form schema. Same as contact in voteit.core """
