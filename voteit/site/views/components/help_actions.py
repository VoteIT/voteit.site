from pyramid.renderers import render
from pyramid.url import resource_url
from betahaus.viewcomponent import view_action

from voteit.site import SiteMF as _


@view_action('help_action', 'support')
def action_support(context, request, va, **kw):
    api = kw['api']
    if api.root:
        link = resource_url(api.root, request) + "support"
        return """<li><a id="support" class="tab buttonize" href="%s">%s</a></li>""" % (link, api.translate(_(u"Support")))
        
    return ""