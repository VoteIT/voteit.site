from deform import Form
from deform.exception import ValidationFailure
from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPRedirection
from pyramid.url import resource_url
from pyramid.renderers import render
from pyramid.response import Response
from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message
from pyramid.traversal import find_root
from betahaus.pyracont.factories import createSchema

from voteit.core import security
from voteit.core.views.base_view import BaseView
from voteit.core.models.interfaces import ISiteRoot
from voteit.core.models.interfaces import IMeeting
from voteit.core.models.schemas import add_csrf_token
from voteit.core.models.schemas import button_send
from voteit.core import fanstaticlib

from voteit.site import SiteMF as _
from voteit.site.models.interfaces import ISupportStorage 


class HelpView(BaseView):
    @view_config(name = 'feedback', context=ISiteRoot, renderer="templates/ajax_edit.pt", permission=NO_PERMISSION_REQUIRED)
    def feedback(self):
        """ Feedback form
        """
        schema = createSchema('FeedbackSchema').bind(context=self.context, request=self.request, api = self.api)
        add_csrf_token(self.context, self.request, schema)
            
        form = Form(schema, action=resource_url(self.context, self.request)+"@@feedback", buttons=(button_send,), formid="help-tab-feedback-form", use_ajax=True)
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
            
            sender = "VoteIT <info@voteit.se>"

            recipients = ("feedback@voteit.se",) 

            response = {
                        'api': self.api,
                        'meeting': self.api.meeting,
                        'name': appstruct['name'],
                        'email': appstruct['email'],
                        'subject': appstruct['subject'],
                        'message': appstruct['message'],
                        }
            body_html = render('templates/email/help_support.pt', response, request=self.request)
        
            msg = Message(subject=_(u"VoteIT - Feedback"),
                          sender = sender and sender or None,
                          recipients=recipients,
                          html=body_html)
        
            mailer = get_mailer(self.request)
            mailer.send(msg)
            
            self.response['message'] = _(u"Message sent to VoteIT")
            return Response(render("templates/ajax_success.pt", self.response, request = self.request))

        #No action - Render form
        self.response['form'] = form.render()
        return self.response
    
    @view_config(name = 'support', context=ISiteRoot, renderer="templates/ajax_edit.pt", permission=NO_PERMISSION_REQUIRED)
    def support(self):
        """ Support form
        """
        schema = createSchema('SupportSchema').bind(context=self.context, request=self.request, api = self.api)
        add_csrf_token(self.context, self.request, schema)
            
        form = Form(schema, action=resource_url(self.context, self.request)+"@@support", buttons=(button_send,), formid="help-tab-support-form", use_ajax=True)
        self.api.register_form_resources(form)

        post = self.request.POST

        if self.request.method == 'POST':
            controls = post.items()
            try:
                appstruct = form.validate(controls)
            except ValidationFailure, e:
                self.response['form'] = e.render()
                return self.response
            
            sender = "VoteIT <info@voteit.se>"

            recipients = ("support@voteit.se",) 

            response = {
                        'api': self.api,
                        'meeting': self.api.meeting,
                        'name': appstruct['name'],
                        'email': appstruct['email'],
                        'subject': appstruct['subject'],
                        'message': appstruct['message'],
                        }
            body_html = render('templates/email/help_support.pt', response, request=self.request)
        
            msg = Message(subject=_(u"VoteIT - Support"),
                          sender = sender and sender or None,
                          recipients=recipients,
                          html=body_html)
        
            mailer = get_mailer(self.request)
            mailer.send(msg)

            # add the message to the support storage    
            root = find_root(self.context)
            support_storage = self.request.registry.getAdapter(root, ISupportStorage)
            support_storage.add(appstruct['message'], subject=appstruct['subject'], name=appstruct['name'], email=appstruct['email'], meeting=self.api.meeting)
            
            self.response['message'] = _(u"Message sent to VoteIT")
            return Response(render("templates/ajax_success.pt", self.response, request = self.request))

        #No action - Render form
        self.response['form'] = form.render()
        return self.response
