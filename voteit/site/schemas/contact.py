import colander
import deform
from betahaus.pyracont.decorators import schema_factory
from voteit.core.validators import html_string_validator
from voteit.core.schemas.contact import ContactSchema
from voteit.core.schemas.common import deferred_default_user_fullname
from voteit.core.schemas.common import deferred_default_user_email

from voteit.site import SiteMF as _


@colander.deferred
def deferred_meeting_title(node, kw):
    context = kw['context']
    if context.content_type == 'Meeting':
        return context.title
    return u""


@schema_factory('FeedbackSchema', title=_("Feedback"),
                description = _(u"Contact the VoteIT team with feedback. Please enter your email address if you want to be able to receive a reply!"))
class FeedbacktSchema(ContactSchema):
    """ Feedback contact form schema. Same as contact in voteit.core """


@schema_factory('SupportSchema', title=_("Support"))
class SupportSchema(colander.Schema):
    """ Support contact form schema. Same as contact in voteit.core """
    name = colander.SchemaNode(colander.String(),
                               title = _(u"Name"),
                               default = deferred_default_user_fullname,
                               validator = colander.Length(max = 100),)
    email = colander.SchemaNode(colander.String(),
                               title = _(u"Email"),
                               description = _(u"contact_schema_email_description",
                                               default = u"Leave this field empty if you want to be anonymous. Remember that you won't be able to receive a reply if it's empty!"),
                               default = deferred_default_user_email,
                               validator = colander.Email(),
                               missing=u"") 
    subject = colander.SchemaNode(colander.String(),
                                  title = _(u"Subject"),
                                  validator = html_string_validator,)
    meeting_title = colander.SchemaNode(colander.String(),
                                        title = _(u"Meeting"),
                                        description = _(u"support_schema_meeting_description",
                                                        default = u"Is this support request about a specific meeting? "
                                                            u"In that case, what's the title of the meeting? "
                                                            u"(It doesn't have to be exact, it's just so we know what to look for!)"),
                                        default = deferred_meeting_title,
                                        validator = html_string_validator,
                                        missing = u"",)
    message = colander.SchemaNode(colander.String(),
                                  title = _(u'What do you need help with?'),
                                  description = _(u"support_schema_message_description",
                                                  default = u"Please take time to describe what you need help with, or what went wrong. "
                                                            u"If you're submitting an error report, please explain what you were doing and how we can reproduce the error. "
                                                            u"The more information you send us, the better. We're really bad at reading minds..."),
                                  widget = deform.widget.TextAreaWidget(rows=10, cols=40),
                                  validator = html_string_validator,)
