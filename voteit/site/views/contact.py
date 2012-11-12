from deform import Form
from deform.exception import ValidationFailure
from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.view import view_config
from pyramid.renderers import render
from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message
from pyramid.traversal import find_root
from pyramid.httpexceptions import HTTPFound
from betahaus.pyracont.factories import createSchema

from voteit.core import security
from voteit.core.views.base_edit import BaseEdit
from voteit.core.models.interfaces import ISiteRoot
from voteit.core.models.interfaces import IMeeting
from voteit.core.models.schemas import add_csrf_token
from voteit.core.models.schemas import button_send
from voteit.core import fanstaticlib

from voteit.site import SiteMF as _
from voteit.site.models.interfaces import ISupportStorage 


class SupportView(BaseEdit):

    @view_config(name = 'feedback', context=ISiteRoot, renderer="voteit.core.views:templates/base_edit.pt", permission=NO_PERMISSION_REQUIRED)
    @view_config(name = 'feedback', context=IMeeting, renderer="voteit.core.views:templates/base_edit.pt", permission=security.VIEW)
    def feedback(self):
        """ Feedback form
        """
        fanstaticlib.jquery_form.need()
        schema = createSchema('FeedbackSchema').bind(context=self.context, request=self.request, api = self.api)
        add_csrf_token(self.context, self.request, schema)
        form = Form(schema, action=self.request.resource_url(self.context, 'feedback'), buttons=(button_send,))
        #FIXME: This doesn't seem to work when loaded with ajax. We need to investigate more.
        self.api.register_form_resources(form)

        post = self.request.POST
        if self.request.method == 'POST':
            controls = post.items()
            try:
                appstruct = form.validate(controls)
            except ValidationFailure, e:
                self.response['form'] = e.render()
                return self.response
            sender = appstruct['email'] and appstruct['email'] or "VoteIT <noreply@voteit.se>"
            recipients = ("feedback@voteit.se",) 
            response = {'api': self.api,
                        'meeting': self.api.meeting,
                        'name': appstruct['name'],
                        'email': appstruct['email'],
                        'subject': appstruct['subject'],
                        'message': appstruct['message'],
                        }
            body_html = render('templates/email/support.pt', response, request=self.request)
            subject = "[%s] | %s" % (self.api.translate(_(u"VoteIT Feedback")), appstruct['subject'])
            msg = Message(subject = subject,
                          sender = sender and sender or None,
                          recipients=recipients,
                          html=body_html)
            mailer = get_mailer(self.request)
            mailer.send(msg)
            self.api.flash_messages.add(_(u"Message sent to VoteIT"))
            url = self.request.resource_url(self.context)
            return HTTPFound(location = url)

        #No action - Render form
        self.response['form'] = form.render()
        return self.response
    
    @view_config(name = 'support', context=ISiteRoot, renderer="voteit.core.views:templates/base_edit.pt", permission=NO_PERMISSION_REQUIRED)
    @view_config(name = 'support', context=IMeeting, renderer="voteit.core.views:templates/base_edit.pt", permission=security.VIEW)
    def support(self):
        """ Support form
        """
        fanstaticlib.jquery_form.need()
        schema = createSchema('SupportSchema').bind(context=self.context, request=self.request, api = self.api)
        add_csrf_token(self.context, self.request, schema)
        form = Form(schema, action=self.request.resource_url(self.context, 'support'), buttons=(button_send,))
        self.api.register_form_resources(form)

        post = self.request.POST
        if self.request.method == 'POST':
            controls = post.items()
            try:
                appstruct = form.validate(controls)
            except ValidationFailure, e:
                self.response['form'] = e.render()
                return self.response
            
            sender = appstruct['email'] and appstruct['email'] or "VoteIT <noreply@voteit.se>"
            recipients = ("support@voteit.se",) 
            response = {'api': self.api,
                        'meeting': self.api.meeting,
                        'name': appstruct['name'],
                        'email': appstruct['email'],
                        'subject': appstruct['subject'],
                        'message': appstruct['message'],
                        'meeting_title': appstruct.get('meeting_title', ''),
                        }
            body_html = render('templates/email/support.pt', response, request=self.request)
            subject = "[%s] | %s" % (self.api.translate(_(u"VoteIT Support")), appstruct['subject'])
            msg = Message(subject = subject,
                          sender = sender and sender or None,
                          recipients=recipients,
                          html=body_html)
            mailer = get_mailer(self.request)
            mailer.send(msg)

            # add the message to the support storage    
            root = find_root(self.context)
            support_storage = self.request.registry.getAdapter(root, ISupportStorage)
            support_storage.add(appstruct['message'], subject=appstruct['subject'], name=appstruct['name'], email=appstruct['email'], meeting=self.api.meeting)
            self.api.flash_messages.add(_(u"Message sent to VoteIT"))
            url = self.request.resource_url(self.context)
            return HTTPFound(location = url)

        #No action - Render form
        self.response['form'] = form.render()
        return self.response

