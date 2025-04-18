from SPARQLWrapper import SPARQLWrapper
import os
import re
os.environ['TF_CPP_MIN_LOG_LEVEL']='4'


def query_sparkle(Q, KG1_flag):

    if KG1_flag:
        queryString = """
            PREFIX dcterms: <http://purl.org/dc/terms/> 
            PREFIX foaf: <http://xmlns.com/foaf/0.1/> 
            PREFIX ns1: <https://github.com/PeppeRubini/EVA-KG/tree/main/ontology/ontology.owl#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
            SELECT DISTINCT ?obj WHERE{
            """ + Q + """ rdf:type ?obj
            FILTER strstarts(str(?obj), str(dbo:))
            }
            """
        return queryString
    else:
        queryString = """
                    PREFIX : <http://example.org/abuse-of-women#>
                    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                    PREFIX owl: <http://www.w3.org/2002/07/owl#> 
                    SELECT DISTINCT ?obj WHERE{
                    """ + Q + """ rdf:type ?obj
                    FILTER strstarts(str(?obj), str(dbo:))
                    }
                    """
        return queryString


def getRdfType(Q, KG1_flag):
    Q_types = []

    query = query_sparkle(Q, KG1_flag)

    if KG1_flag:
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    else:
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")

    sparql.setQuery(query)
    sparql.setTimeout(1000)

    sparql.setReturnFormat("json")

    try:
        results = sparql.query().convert()
        for result in results["results"]["bindings"]:
            if KG1_flag:
                Q_types.append(result["obj"]["value"].replace("http://dbpedia.org/ontology/",""))
            else:
                Q_types.append(result["obj"]["value"].replace("http://dbpedia.org/ontology/", ""))
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


def getRDFData(o, KG1_flag):
    if str(o).startswith('http://dbpedia.org/resource/'):
        Q_entity = "<"+o+">"
        data_type = getRdfType(Q_entity, KG1_flag)
    else:
        data_type = [dataType(o)]
    
    return o, data_type


def add_to_set(types, typeset):
    for t in types:
        typeset.add(t)






