from betahaus.viewcomponent import view_action

from voteit.site import SiteMF as _


@view_action('help_action', 'feedback', title = _(u"Feedback"))
@view_action('help_action', 'support', title = _(u"Support"))
def action_contact(context, request, va, **kw):
    """ Register buttons for help actions. Keep in mind that the name and the link must be the same.
    """
    api = kw['api']
    context = api.meeting and api.meeting or api.root
    return """<li><a class="tab buttonize" href="%s">%s</a></li>""" % (request.resource_url(context, va.name),
                                                                       api.translate(va.title),)
