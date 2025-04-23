from SPARQLWrapper import SPARQLWrapper
import os
import re
import xml.etree.ElementTree as ET
os.environ['TF_CPP_MIN_LOG_LEVEL']='4'


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

    # Verifica se è stato passato un grafo
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
                print("Cerchiamo nel file xml")
                if xml_root:
                    uri = Q.strip("<>")  # Rimuovi eventuali tag <>
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
            return Q_types

        except Exception as e:
            print(f"Errore interrogando KG2 locale: {e}")
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


def getRDFData(o, KG1_flag, graph):
    data_type = []

    # Se l'oggetto è un URI, otteniamo i tipi dall'entità
    if str(o).startswith('https://github.com/PeppeRubini/EVA-KG/tree/main/ontology/ontology.owl#'):
        # Si tratta di un'entità nel primo Knowledge Graph (KG1)
        Q_entity = "<" + o + ">"
        data_type = getRdfType(Q_entity, KG1_flag, graph)  # Ottieni i tipi associati all'entità

    elif str(o).startswith('http://example.org/abuse-of-women#'):
        # Si tratta di un'entità nel secondo Knowledge Graph (KG2)
        Q_entity = "<" + o + ">"
        data_type = getRdfType(Q_entity, KG1_flag, graph)

    else:
        # Se l'oggetto non è un URI, si tratta di un valore letterale
        # Determina il tipo del valore letterale (string, integer, date, etc.)
        data_type = [dataType(o)]  # Determina il tipo del valore letterale
        print(f"Tipo letterale identificato: {data_type}")

    return o, data_type


def add_to_set(types, typeset):
    for t in types:
        typeset.add(t)






