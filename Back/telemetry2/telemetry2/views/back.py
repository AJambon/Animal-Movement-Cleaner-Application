import os
import logging
import random
import copy
import sys
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.request import Request

#log = logging.getLogger(__name__)

@view_config(route_name='backapp', renderer='json',request_method='POST')

def init_back(request):
    #log.debug('%s %s', request, request.params)
    if "geometry" in request.POST:
        geometry = request.POST.get('geometry')
        print(geometry)
        pb=[]
        points_distinct,pb=parsingRequest(geometry,pb)
        print(pb)
        if len(pb)==0:
            points_distinct_del=annotatedResult(points_distinct)
            return points_distinct,points_distinct_del
        else :
            return 'souci'
    else:
        return 'no params'
        )




def parsingRequest(options,pb):
    points=options.split('\n')
    points_distinct={}    
    i=0
    long=len(points)
    print(long,points)
    while i < long : 
        tempData = points[i].split(',')
        print(len(tempData))
        if len(tempData)!= 4:
            print('souci')
            pb.append(1)
        else:
            print('Thank you')
            points_distinct[i] = {
                'id':tempData[0],
                'date':tempData[1],
                'LON':tempData[2],
                'LAT':tempData[3]
            }
        i=i+1
    return points_distinct, pb
   


def annotatedResult(dico):
    points_distinct_del=copy.deepcopy(dico)
    R=random.randint(0, 3)
    print(R)
    i=0
    while i < len(points_distinct_del) :
        if i==R:
            points_distinct_del[i]['status']='deleted'
        else :
            points_distinct_del[i]['status']='kept'
        i=i+1
    #del points_distinct_del[R]
    return points_distinct_del

