#!/usr/bin/env python
# -*- coding:utf8 -*-

import lxml.etree as ET
#import unicodedata as ud
#import sys
import re

def retrieveEntries(infile):
    dom = ET.parse(infile)
    chapters = dom.find("volumes").findall("chapter")
    entries = [e  for chp in chapters for e in chp.findall("shuowen")]
    d = {}
    for e in entries:
        key = e.find("wordhead").text.strip()
        if key not in d :
            d[key] = []
        for expl in e.findall("explanation"):
            if expl.text == None :
                continue
            for sentence in expl.text.strip().split(u"。"):
                d[key].append(sentence)
    return d
    
def buildDecompositions(d):
    decomp = {}
    for e,expl in d.iteritems():
        if e not in decomp:
            decomp[e] = {"graphic":[], "phonetic":[]}
        for s in expl:
            if re.match(ur"^从",s):
                decomp[e]["graphic"].extend(list(s[1:]))
            if re.match(ur"^.聲$",s):
                decomp[e]["phonetic"].append(s[0])
    return decomp
    
    
def decompose(d,z):
    def recdec(z1):
        r = {"graphic":[], "phonetic":[]}
        if z1 not in d:
            return ()
        for z2 in d[z1]["graphic"]:
            r["graphic"].append((z2,recdec(z2)))
        for z2 in d[z1]["phonetic"]:
            r["phonetic"].append((z2,recdec(z2)))
        return r
    return (z,recdec(z))


def printDec(z,pad=0):
    print "\t"*pad,z[0]
    if z[1] == ():
        return
    for z2 in z[1]["graphic"]:
        print "\t"*(pad+1),"graphic"
        printDec(z2,pad+1)
    for z2 in z[1]["phonetic"]:
        print "\t"*(pad+1),"phonetic"
        printDec(z2,pad+1)

def toJSON(z):
    import json
    def convert(z1):
        name = z1[0].encode("utf8")
        children = []
        if z1[1] != ():
            if len(z1[1]["graphic"]) > 0:
                children.append({"name": "gr", "children": map(convert,z1[1]["graphic"]) })
            if len(z1[1]["phonetic"]) > 0:
                children.append({"name": "ph", "children": map(convert,z1[1]["phonetic"]) })
        return {"name": name, "children": children}
    return json.dumps(convert(z))
