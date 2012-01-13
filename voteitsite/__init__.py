from pyramid.config import Configurator
from voteitsite.resources import Root

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(root_factory=Root, settings=settings)
    config.add_view('voteitsite.views.my_view',
                    context='voteitsite:resources.Root',
                    renderer='voteitsite:templates/mytemplate.pt')
    config.add_static_view('static', 'voteitsite:static', cache_max_age=3600)
    return config.make_wsgi_app()
