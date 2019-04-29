from pyramid.view import view_config
from pyramid.response import Response

@view_config(route_name='home')
def my_view(request):
    print('sxchtroudel')
    return Response('Hello test7 /home!')

@view_config(route_name='test')
def my_test_view(request):
    print('sxchtroudel2000')
    return Response('Wesh alors /(est)!')

# @view_config(route_name='backapp')
# def init_back(request):
#     print('sxchtroude4577')
#     return Response ('voilà le back!')
