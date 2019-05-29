import os
from telemetry2 import views

def includeme(config):
    #config.add_static_view('static', 'static', cache_max_age=3600)
    #config.add_static_view('deform_static', 'deform:static') # pour form
    #config.scan('.views.testAJ')
    config.add_route('home', '/')
    #config.add_route('test', '/test')
    # config.add_view(my_view, route_name='home')
    config.scan('.views.back')
    config.add_route('backapp', '/backapp')
    

