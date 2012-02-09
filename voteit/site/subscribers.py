from pyramid.events import subscriber
from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message
from pyramid.renderers import render
from pyramid.threadlocal import get_current_request
from pyramid.url import resource_url

from voteit.core.models.interfaces import IMeeting
from voteit.core.interfaces import IWorkflowStateChange

from voteit.site import SiteMF as _


@subscriber([IMeeting, IWorkflowStateChange])
def state_change_notification(meeting, event):
    """ Sends an email to info@voteit.se when a meeting changes state """
    
    request = get_current_request()
    url = resource_url(meeting, request)
    
    sender = "%s <%s>" % (meeting.get_field_value('meeting_mail_name'), meeting.get_field_value('meeting_mail_address'))
    
    response = {
                'title': meeting.get_field_value('title'),
                'new_state': event.new_state.title().lower(),
                'old_state': event.old_state.title().lower(),
                'url': url,
                }
    body_html = render('views/templates/email/state_change_notification.pt', response, request=request)

    msg = Message(subject=_(u"VoteIT meeting state changed"),
                  sender = sender and sender or None,
                  recipients=("info@voteit.se",),
                  html=body_html)

    mailer = get_mailer(request)
    mailer.send(msg)
