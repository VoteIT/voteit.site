from pyramid.i18n import TranslationStringFactory

PROJECTNAME = 'voteit.site'
SiteMF = TranslationStringFactory(PROJECTNAME)


def includeme(config):
    """ Include Site adapter and register views."""
    config.scan(PROJECTNAME)
    config.include('voteit.site.models.support_storage')
    config.add_translation_dirs('%s:locale/' % PROJECTNAME)
    cache_ttl_seconds = int(config.registry.settings.get('cache_ttl_seconds', 7200))
    config.add_static_view('site_static', '%s:static' % PROJECTNAME, cache_max_age = cache_ttl_seconds)

    #Register fanstatic resource
    from voteit.core.models.interfaces import IFanstaticResources
    from .fanstaticlib import voteit_site
    util = config.registry.getUtility(IFanstaticResources)
    util.add('voteit_site', voteit_site)
