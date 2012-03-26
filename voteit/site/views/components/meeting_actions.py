from pyramid.url import resource_url
from betahaus.viewcomponent import view_action

from voteit.site import SiteMF as _


@view_action('admin_menu', 'support requests', title = _(u"Support requests"), link = "support_requests")
def generic_root_menu_link(context, request, va, **kw):
    """ This is for simple menu items for the root """
    api = kw['api']
    url = api.resource_url(api.root, request) + va.kwargs['link']
    return """<li><a href="%s">%s</a></li>""" % (url, api.translate(va.title))