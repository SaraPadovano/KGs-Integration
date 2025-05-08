import os
import re
import xml.etree.ElementTree as ET
from SPARQLWrapper import SPARQLWrapper, JSON
os.environ['TF_CPP_MIN_LOG_LEVEL']='4'


def get_wikidata_type(entity_uri):
    qid = entity_uri.split("/")[-1]
    print(qid)

    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setReturnFormat(JSON)

    query = f"""
        SELECT DISTINCT ?typeLabel WHERE {{
            wd:{qid} (p:P31|p:P279|p:P361) ?statement .
            ?statement ps:P31|ps:P279|ps:P361 ?type .
            SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        }}
        """

    print(query)

    sparql.setQuery(query)

    try:
        results = sparql.query().convert()
        print(results)
        types = [res["typeLabel"]["value"] for res in results["results"]["bindings"]]
        print(types)
        return types
    except Exception as e:
        print(f"Errore interrogando Wikidata: {e}")
        return ["wikidata_entity"]


def find_type_in_xml(uri, xml_root):
    ns = {"rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#"}
    types = []

    for description in xml_root.findall("rdf:Description", namespaces=ns):
        about_uri = description.attrib.get("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about")
        if about_uri == uri:
            type_elems = description.findall("rdf:type", namespaces=ns)
            for type_elem in type_elems:
                rdf_type = type_elem.attrib.get("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource")
                if rdf_type:
                    types.append(rdf_type)
    return types if types else None

def query_sparql(Q, KG1_flag):

    if KG1_flag:
        print("entrato per query KG1")
        queryString = """
                   PREFIX dcterms: <http://purl.org/dc/terms/> 
                   PREFIX foaf: <http://xmlns.com/foaf/0.1/> 
                   PREFIX ns1: <https://github.com/PeppeRubini/EVA-KG/tree/main/ontology/ontology.owl#>
                   PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
                   SELECT DISTINCT ?obj WHERE{
                    """ + Q + """ rdf:type ?obj
                    }
                   """
        return queryString
    else:
        queryString = """
                    PREFIX : <http://example.org/abuse-of-women#>
                    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                    PREFIX owl: <http://www.w3.org/2002/07/owl#>
                    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
                    SELECT DISTINCT ?obj WHERE{
                    """ + Q + """ rdf:type ?obj
                    }
                    """
        return queryString


def getRdfType(Q, KG1_flag, graph):
    Q_types = []

    if graph is None:
        print("Errore: nessun grafo passato")
        return []

    query = query_sparql(Q, KG1_flag)
    print("🧪 SPARQL query generata:\n", query)

    if KG1_flag:
        xml_tree = ET.parse(r"C:\Users\acer\EVA-KG\ontology\ontology.owl")
        xml_root = xml_tree.getroot()
        try:
            results = graph.query(query)
            print(f"✅ Query eseguita, risultati trovati: {len(results)}")
            if len(results) == 0:
                print("Cerchiamo nel file XML")
                if xml_root:
                    # Rimuoviamo eventuali tag <>
                    uri = Q.strip("<>")
                    type_from_xml = find_type_in_xml(uri, xml_root)
                    if type_from_xml:
                        for val in type_from_xml:
                            tipo = str(val).split('#')[-1]
                            Q_types.append(tipo)

                        # Rimuoviamo duplicati
                        Q_types = list(set(Q_types))
                        return Q_types

        except Exception as e:
            print(f"Errore interrogando KG1 locale: {e}")
            return []

    else:
        try:
            results = graph.query(query)
            print(f"✅ Query eseguita, risultati trovati: {len(results)}")
            for row in results:
                for val in row:
                    val_str = str(val)
                    if '#' in val_str:
                        tipo = val_str.split('#')[-1]
                    else:
                        tipo = val_str.split('/')[-1]
                    Q_types.append(tipo)

            # Rimuoviamo duplicati
            Q_types = list(set(Q_types))

            if not Q_types:
                print("Nessun tipo trovato in KG2.")
            return Q_types

        except Exception as e:
            print(f"Errore interrogando KG2 locale: {e}")
            return []

    # Fallback per Wikidata: cerca direttamente tramite l'endpoint
    if "wikidata" in Q.lower():
        print("🔎 URI esterna rilevata (Wikidata), interrogazione endpoint...")
        types_from_wikidata = get_wikidata_type(Q.strip("<>"))
        if types_from_wikidata:
            Q_types.extend(types_from_wikidata)
            Q_types = list(set(Q_types))  # Rimuove duplicati
            return Q_types


    return Q_types if Q_types else []


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


def getRDFData(o, KG1_flag, graph):
    data_type = []

    if str(o).startswith('https://github.com/PeppeRubini/EVA-KG/tree/main/ontology/ontology.owl#'):
        Q_entity = "<" + o + ">"
        data_type = getRdfType(Q_entity, KG1_flag, graph)

    elif "wikidata.org/entity/" in o:
        Q_entity = "<" + o + ">"
        data_type = getRdfType(Q_entity, KG1_flag, graph)

    elif str(o).startswith('http://example.org/abuse-of-women#'):
        Q_entity = "<" + o + ">"
        data_type = getRdfType(Q_entity, KG1_flag, graph)

    else:
        data_type = [dataType(o)]
        print(f"Tipo letterale identificato: {data_type}")

    return o, data_type


def add_to_set(types, typeset):
    for t in types:
        typeset.add(t)

