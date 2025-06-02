import pickle
import os

def substitute_with_synonyms(text, align_dict):
    if ',' in text:
        parts = [p.strip() for p in text.split(',')]
        return ','.join([align_dict.get(p, p) for p in parts])
    else:
        return align_dict.get(text, text)

def match_entities(match_file, prox_graph_KG1, prox_graph_KG2):
    base_path = r"C:\Users\acer\KGs-Integration\files"
    align_dict = {}

    # 1. Carica il dizionario di sinonimi
    with open(match_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip().strip("()")
            if not line:
                continue
            parts = [p.strip() for p in line.split(",")]
            if len(parts) == 2:
                align_dict[parts[0]] = parts[1]
            else:
                print(f"Riga malformata: {line}")

    merged_prox_graph = []

    with open(prox_graph_KG1, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip().split('\t')
            if len(line) < 2:
                continue
            line = [substitute_with_synonyms(part, align_dict) for part in line]
            merged_prox_graph.append(line)

    with open(prox_graph_KG2, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) < 2:
                continue
            merged_prox_graph.append(parts)

    output_pickle = os.path.join(base_path, "KGs_merged_pred_prox_graph.pickle")
    with open(output_pickle, 'wb') as pkl_file:
        pickle.dump(merged_prox_graph, pkl_file)


    output_txt = os.path.join(base_path, "KGs_merged_pred_prox_graph.txt")
    with open(output_txt, 'w', encoding='utf-8') as txt_file:
        for line in merged_prox_graph:
            txt_file.write('\t'.join(line) + '\n')