import sys
import os
import warnings
import importlib.util
from KB_entity_type import getRDFData, add_to_set
from rdflib import Graph
#from selenium import webdriver
#from selenium.webdriver.chrome.service import Service
#from selenium.webdriver.chrome.options import Options
from prompt_gen import union_typeset, prompt, call_for_sim, call_llm_without_api, another_try, gpt_score, clean_match
from match_type import match_entities

# Funzione che richiama le funzioni di KB_entity_type per la definzione dei tipi per la generazione dei prox graph
def entity_prox_graph(filename, file_prox_graph, KG1_flag):

    print("Entrato nella funzione entity_prox_graph")
    graph = Graph()
    # Definiamo il formato turtle non nt perchè i file non hanno semplici triple ma più complesse per il formato nt
    graph.parse(location=filename, format='turtle')
    print("len(graph):", len(graph))
    typeset1 = set()
    typeset2 = set()

    prox_graph = []
    i = 0
    open(f"{file_prox_graph}.txt", 'w', encoding='utf-8').close()

    # Ciclo che itera sulle triple del grafo indentificando i tipi dei soggetti e degli oggetti per ogni tripla
    for s, p, o in graph:
        i += 1
        print(f"\n--- Tripla {i} ---")
        print(f"s: {s}, p: {p}, o: {o}")
        s, s_data_type = getRDFData(str(s), KG1_flag, graph)
        print(f"🟢 Tipo soggetto: {s_data_type}")
        o, o_data_type = getRDFData(str(o), KG1_flag, graph)
        print(f"🔵 Tipo oggetto: {o_data_type}")


        add_to_set(s_data_type, typeset1)
        add_to_set(o_data_type, typeset2)
        prox_triple_list = [','.join(s_data_type), p, ','.join(o_data_type)]
        prox_triple_string = '\t'.join(prox_triple_list)
        print(f"✅ Tripla prossimità: {prox_triple_string}")

        prox_graph.append(prox_triple_string)


        if i % 1000 == 0:
            with open(f"{file_prox_graph}.txt", 'a+', encoding='utf-8') as f:
                for prox_i in prox_graph:
                    f.write(str(prox_i))
                    f.write('\n')
            prox_graph = []
            print("i: ", i)

    print("uscito for")

    if prox_graph:
        with open(f"{file_prox_graph}.txt", 'a+', encoding='utf-8') as f:
            for prox_i in prox_graph:
                f.write(str(prox_i))
                f.write('\n')
        print("✔️ Scrittura finale completata")

    if KG1_flag:
        print("Scrittura file con i tipi per KG1")
        with open('../files/typeset1_KG1.txt', 'w', encoding='utf-8') as f:
            f.write(','.join(list(typeset1)))
        with open('../files/typeset2_KG1.txt', 'w', encoding='utf-8') as f:
            f.write(','.join(list(typeset2)))
    else:
        print("Scrittura file con i tipi per KG2")
        with open('../files/typeset1_KG2.txt', 'w', encoding='utf-8') as f:
            f.write(','.join(list(typeset1)))
        with open('../files/typeset2_KG2.txt', 'w', encoding='utf-8') as f:
            f.write(','.join(list(typeset2)))

def main():

    print("Entrato in main")
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
    writer = open("../files/training_log2.txt", "w", encoding="utf-8")

    #service = Service(r'C:\Users\acer\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe')
    #options = Options()
    #options.add_argument("--headless")
    #options.add_argument("--disable-gpu")
    #driver = webdriver.Chrome(service=service, options=options)

    # KG di prova
    #KG1_filename = r'C:\Users\acer\KGs-Integration\KGs\KG_PROVA.ttl'
    #KG1_prox_graph_file = r'C:\Users\acer\KGs-Integration\files\KG_PROVA_pred_prox_graph'
    #KG1_flag = True
    #entity_prox_graph(KG1_filename, KG1_prox_graph_file, KG1_flag)

    # Definiamo il primo KG in ttl che deve essere fatto il grafo di prossimità e i tipi delle entità
    #KG1_filename = r'C:\Users\acer\KGs-Integration\KGs\KG1.ttl'
    #KG1_prox_graph_file = r'C:\Users\acer\KGs-Integration\files\KG1_pred_prox_graph'
    #KG1_flag = True
    #entity_prox_graph(KG1_filename, KG1_prox_graph_file, KG1_flag)
    #file1 = r'C:\Users\acer\KGs-Integration\files\typeset1_KG1.txt'
    #file2 = r'C:\Users\acer\KGs-Integration\files\typeset2_KG1.txt'
    #fileUnion = r'C:\Users\acer\KGs-Integration\files\final_typeset_KG1.txt'
    #union_typeset(file1, file2, fileUnion)

    # Definiamo il secondo KG in ttl che deve essere fatto il grafo di prossimità e i tipi delle entità
    #KG2_filename = r'C:\Users\acer\KGs-Integration\KGs\KG2.ttl'
    #KG2_prox_graph_file = r'C:\Users\acer\KGs-Integration\files\KG2_pred_prox_graph'
    #KG1_flag = False
    #entity_prox_graph(KG2_filename, KG2_prox_graph_file, KG1_flag)
    #file1 = r'C:\Users\acer\KGs-Integration\files\typeset1_KG2.txt'
    #file2 = r'C:\Users\acer\KGs-Integration\files\typeset2_KG2.txt'
    #fileUnion = r'C:\Users\acer\KGs-Integration\files\final_typeset_KG2.txt'
    #union_typeset(file1, file2, fileUnion)

    # Creiamo il prompt per l'LLM
    #file_type_KG1 = r'C:\Users\acer\KGs-Integration\files\final_typeset_KG1.txt'
    #file_type_KG2 = r'C:\Users\acer\KGs-Integration\files\final_typeset_KG2.txt'
    #prompt_file = r'C:\Users\acer\KGs-Integration\files\prompt.txt'
    #prompt(file_type_KG1, file_type_KG2, prompt_file)
    # Richiamiamo la funzione per richiamare prima un modello di similarità
    #match_file_sim = r'C:\Users\acer\KGs-Integration\files\matched_types_SIM.txt'
    #match_score = r'C:\Users\acer\KGs-Integration\files\matched_score.txt'
    #call_for_sim(match_file_sim, file_type_KG1, file_type_KG2, match_score)
    # Richiamo la funzione per richiamare un llm generativo
    #match_file_gen = r'C:\Users\acer\KGs-Integration\files\matched_types_LLM_GEN.txt'
    #call_llm_without_api(prompt_file, match_file_gen)
    # Un altro modello generativo più potente
    #match_file_gen2 = r'C:\Users\acer\KGs-Integration\files\matched_types_LLM_GEN2.txt'
    #another_try(prompt_file, match_file_gen2)
    # Calcoliamo lo score delle coppie date da GPT
    #score_gpt = r'C:\Users\acer\KGs-Integration\files\matched_score_GPT.txt'
    match_gpt = r'C:\Users\acer\KGs-Integration\files\GPT_match.txt'
    #gpt_score(score_gpt, match_gpt)
    # Ripuliamo il file dei sinonimi da quelli con stesso type1 ma score più basso dell'altro
    #clean_gpt_score = r'C:\Users\acer\KGs-Integration\files\cleaned_matched_score_GPT.txt'
    #clean_match(score_gpt, clean_gpt_score)

    # Creiamo il grafo di prossimità finale per KG1
    prox_graph_KG1 = r'C:\Users\acer\KGs-Integration\files\KG1_pred_prox_graph.txt'
    match_entities(match_gpt, prox_graph_KG1)

    try:
        # Carichiamo specifica del modulo
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        # Iniettiamo writer
        module.__dict__['writer'] = writer
        # Eseguiamo AutoAlign
        # spec.loader.exec_module(module)

    except ImportError as e:
        print("Errore di import:", e)
    except Exception as e:
        print(f"Errore durante l'esecuzione di AutoAlign.py: {e}")
    finally:
        print("Chiusura file")
        writer.close()  # Chiudiamo writer

if __name__ == "__main__":
    main()
