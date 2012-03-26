from pyramid.i18n import TranslationStringFactory

SiteMF = TranslationStringFactory('voteit.site')


def includeme(config):
    """ Include Site adapter and register views."""
    config.scan('voteit.site')
    config.include('voteit.site.models.support_storage')
    config.add_translation_dirs('voteit.site:locale/')