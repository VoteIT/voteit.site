from pyramid.renderers import render
from pyramid.url import resource_url
from betahaus.viewcomponent import view_action

from voteit.site import SiteMF as _
from voteit.site.views.help import HelpView


@view_action('help_action', 'feedback')
def action_feedback(context, request, va, **kw):
    api = kw['api']
    if api.root:
        return """<li><a class="tab buttonize" href="%s">%s</a></li>""" % (resource_url(api.root, request)+"@@feedback", api.translate(_(u"Feedback")),)
    return ""

@view_action('help_action', 'support')
def action_support(context, request, va, **kw):
    api = kw['api']
    if api.root:
        return """<li><a class="tab buttonize" href="%s">%s</a></li>""" % (resource_url(api.root, request)+"@@support", api.translate(_(u"Support")),)
    return ""