from SPARQLWrapper import SPARQLWrapper
import os
import re
os.environ['TF_CPP_MIN_LOG_LEVEL']='4'


def query_sparql(Q, KG1_flag):
    print("Entrato in query_sparql")

    if KG1_flag:
        print("entrato per query KG1")
        queryString = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX dcterms: <http://purl.org/dc/terms/> 
            PREFIX foaf: <http://xmlns.com/foaf/0.1/> 
            PREFIX ns1: <https://github.com/PeppeRubini/EVA-KG/tree/main/ontology/ontology.owl#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
            SELECT DISTINCT ?obj WHERE{
            """ + Q + """ rdf:type ?obj
            FILTER strstarts(str(?obj), str(ns1:))
            }
            """
        return queryString
    else:
        print("Entrato per query KG2")
        queryString = """
                    PREFIX : <http://example.org/abuse-of-women#>
                    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                    PREFIX owl: <http://www.w3.org/2002/07/owl#> 
                    SELECT DISTINCT ?obj WHERE{
                    """ + Q + """ rdf:type ?obj
                    FILTER strstarts(str(?obj), str(:))
                    }
                    """
        return queryString


def getRdfType(Q, KG1_flag):
    print("Entrato in getRdfType")
    Q_types = []

    query = query_sparql(Q, KG1_flag)
    print("Uscito query_sparql")
    if KG1_flag:
        print("primo kg endpoint")
        sparql = SPARQLWrapper("http://localhost:5000/sparql")
    else:
        print("secondo kg endpoint")
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")

    sparql.setQuery(query)
    sparql.setTimeout(1000)

    sparql.setReturnFormat("json")

    try:
        results = sparql.query().convert()
        for result in results["results"]["bindings"]:
            if KG1_flag:
                print("kg1 type append")
                Q_types.append(result["obj"]["value"].replace("https://github.com/PeppeRubini/EVA-KG/tree/main/ontology/ontology.owl#", ""))
            else:
                print("kg2 type append")
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
    print("Entrato in getRDFdata")
    if KG1_flag:
        if str(o).startswith('https://github.com/PeppeRubini/EVA-KG/tree/main/ontology/ontology.owl#'):
            print("Entrato in if per il primo KG")
            Q_entity = "<"+o+">"
            data_type = getRdfType(Q_entity, KG1_flag)
            print("uscito getRdfType")
        else:
            data_type = [dataType(o)]
        return o, data_type
    else:
        if str(o).startswith('http://dbpedia.org/resource/'):
            print("Entrato in if per il secondo KG")
            Q_entity = "<"+o+">"
            data_type = getRdfType(Q_entity, KG1_flag)
            print("uscito getRdfType")
        else:
            data_type = [dataType(o)]
        return o, data_type


def add_to_set(types, typeset):
    print("entrato in add_to_set")
    for t in types:
        typeset.add(t)






