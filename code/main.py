import sys
import os
import warnings
import importlib.util
from KB_entity_type import getRDFData, add_to_set
from rdflib import Graph

# Eliminiamo i warning futuri per funzioni obsolete soprattutto per numpy
warnings.simplefilter(action='ignore', category=FutureWarning)

# Aggiungiamo al path la cartella senza file
path_modulo = r'C:\Users\acer\AutoAlign\code'
if path_modulo not in sys.path:
    sys.path.append(path_modulo)

# Stampiamo per confermare che il file esiste
print("Controllo file:", os.path.exists(os.path.join(path_modulo, 'AutoAlign.py')))

module_name = 'AutoAlign'

# Percorso completo al file
file_path = os.path.join(path_modulo, 'AutoAlign.py')

# Aggiungiamo variabile mancante 'writer'
writer = open("training_log2.txt", "w", encoding="utf-8")

def entity_prox_graph(filename, file_prox_graph, KG1_flag):
    graph = Graph()
    graph.parse(location=filename, format='nt')
    print("len(graph):", len(graph))
    typeset1 = set()
    typeset2 = set()

    prox_graph = []
    i = 0
    for s, p, o in graph:
        i += 1
        s, s_data_type = getRDFData(str(s), KG1_flag)  # change data type
        o, o_data_type = getRDFData(str(o), KG1_flag)

        add_to_set(s_data_type, typeset1)
        add_to_set(o_data_type, typeset2)

        prox_triple_list = [','.join(s_data_type), p, ','.join(o_data_type)]
        prox_triple_string = '\t'.join(prox_triple_list)

        prox_graph.append(prox_triple_string)

        if i % 1000 == 0:
            with open(f"{file_prox_graph}.txt", 'a+') as f:
                for prox_i in prox_graph:
                    f.write(str(prox_i))
                    f.write('\n')
            prox_graph = []
            print("i: ", i)

    with open('./typeset1.txt', 'w') as f:
        f.write(','.join(list(typeset1)))
    with open('./typeset2.txt', 'w') as f:
        f.write(','.join(list(typeset2)))


# Definiamo il primo KG in ttl che deve essere fatto il grafo di prossimità e i tipi delle entità
KG1_filename = r'C:\Users\acer\KGs-Integration\KGs\KG1.ttl'
KG1_prox_graph_file = r'C:\Users\acer\KGs-Integration\KGs/KG1_pred_prox_graph'
KG1_flag = True
entity_prox_graph(KG1_filename, KG1_prox_graph_file, KG1_flag)

try:
    # Carichiamo specifica del modulo
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    # Iniettiamo writer
    module.__dict__['writer'] = writer
    # Eseguiamo AutoAlign
    #spec.loader.exec_module(module)

except ImportError as e:
    print("Errore di import:", e)
except Exception as e:
    print(f"Errore durante l'esecuzione di AutoAlign.py: {e}")
finally:
    print("Chiusura file")
    writer.close()  # Chiudiamo writer
