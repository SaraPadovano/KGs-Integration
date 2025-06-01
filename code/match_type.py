import pickle
import os

def match_entities(match_file, prox_graph_file):
    base_path = r"C:\Users\acer\KGs-Integration\files"
    align_dict = {}
    with open(match_file, 'r') as f:
        for line in f:
            line = line.strip().split('\t')
            align_dict[line[0]] = line[1]

    meta_prox_graph = 'KG1_final_pred_prox_graph'
    aligned_prox_graph = []

    with open(prox_graph_file, 'r') as f:
        for line in f:
            line = line.strip().split('\t')
            if line[0] in align_dict:
                line[0] = align_dict[line[0]]
            if line[1] in align_dict:
                line[1] = align_dict[line[1]]

            aligned_prox_graph.append(line)

    output_filename = f"{meta_prox_graph}_matched.pickle"
    output_path = os.path.join(base_path, output_filename)

    pickle.dump(aligned_prox_graph, open(output_path, 'wb'))