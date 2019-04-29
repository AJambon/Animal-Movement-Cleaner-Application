import os
from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings) as config:
        config.include('.models')
        config.include('pyramid_jinja2')
        
        config.include('.cors')
    
        # make sure to add this before other routes to intercept OPTIONS
        config.add_cors_preflight_handler()
        
        config.include('.routes')
        # config.add_route('home', '/')
        # config.add_route('test', '/test')
        # config.scan('.views.testAJ')
    return config.make_wsgi_app()
