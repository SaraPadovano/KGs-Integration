#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#get_ipython().system(' pip install SPARQLWrapper')
#get_ipython().system(' pip install python-dateutil')


# In[ ]:


from SPARQLWrapper import SPARQLWrapper
from rdflib import Graph
import _pickle as cPickle
import pandas as pd
import rdflib
import os
import re
os.environ['TF_CPP_MIN_LOG_LEVEL']='4'



# In[ ]:


def getRdfType(Q):
    Q_types = []

    queryString = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dbr: <http://dbpedia.org/resource>
    PREFIX dbo: <http://dbpedia.org/ontology>
    SELECT DISTINCT ?obj WHERE{
    """+ Q +""" rdf:type ?obj
    FILTER strstarts(str(?obj), str(dbo:))
    }
    """

    sparql = SPARQLWrapper("http://dbpedia.org/sparql")

    sparql.setQuery(queryString)  
    sparql.setTimeout(1000)

    sparql.setReturnFormat("json")

    try:
        results = sparql.query().convert()
        for result in results["results"]["bindings"]:
            Q_types.append(result["obj"]["value"].replace("http://dbpedia.org/ontology/",""))
        return Q_types
    except TimeoutError:
        return []

def dataType(string):
    odp='string'
    patternBIT=re.compile('[01]')
    patternINT=re.compile('[0-9]+')
    patternFLOAT=re.compile('[0-9]+\.[0-9]+')
    patternTEXT=re.compile('[a-zA-Z0-9]+')
    patternDate=re.compile('(\d{4})-(\d{2})-(\d{2})')
    if patternTEXT.match(string):
        odp= "string"
    if patternINT.match(string):
        odp= "integer"
    if patternFLOAT.match(string):
        odp= "float"
    if patternDate.match(string):
        odp= "date"
    return odp


def getRDFData(o):
    if str(o).startswith('http://dbpedia.org/resource/'):
        Q_entity = "<"+o+">"
        data_type = getRdfType(Q_entity)
    else:
        data_type = [dataType(o)]
    
    return o, data_type




# In[ ]:


def add_to_set(types, typeset):
    for t in types:
        typeset.add(t)






