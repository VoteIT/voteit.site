from pyramid.renderers import render
from pyramid.url import resource_url
from betahaus.viewcomponent import view_action

from voteit.site import SiteMF as _
from voteit.site.views.help import HelpView


@view_action('help_action', 'support')
def action_support(context, request, va, **kw):
    api = kw['api']
    if api.root:
        return """<li><a class="tab buttonize" href="#help-tab-support">%s</a></li>""" % (api.translate(_(u"Support")),)
    return ""

@view_action('help_tab', 'support')
def tap_support(context, request, va, **kw):
    api = kw['api']
    if api.root:
        hw = HelpView(api.root, request)
        return """<div id="help-tab-support" class="tab">%s</div>""" % (hw.support(),)
    return ""