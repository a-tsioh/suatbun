# -*- coding:utf8 -*-


# Create your views here.
from django.http import HttpResponse
from django.template import Context, loader
from django.core.cache import cache

import SWReader


SHUOWEN_SRC="/home/pierre/SRCs/ShuoWen/swjz.xml"

def fiche(request):
    t = loader.get_template('browse/fiche.html')
    c = Context( {  })
    return HttpResponse(t.render(c))



def cached_data():
    e = cache.get("dict",None)
    if e == None :
        e = SWReader.retrieveEntries(SHUOWEN_SRC)
        cache.set("dict",e)
    d = cache.get("dom",None)
    if d == None :
        d = SWReader.buildDecompositions(e)
        cache.set("dom",d)
    return (e,d)

def get_json(request,charcode):
    char = unichr(int(charcode))
    e,d = cached_data()
    json = SWReader.toJSON(SWReader.decompose(d,char))
    return HttpResponse(json)

def get_explanation(request,charcode):
    import json
    char = unichr(int(charcode))
    sw,d = cached_data()
    expl = ""
    if char in sw :
        expl = u"。".join(filter(lambda x:x.strip()!="",sw[char]))
    data = {"char": char, "def": list(expl)}
    return HttpResponse(json.dumps(data))
