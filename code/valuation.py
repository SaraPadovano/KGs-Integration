import pickle
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import os
from sentence_transformers import SentenceTransformer

def merge_prox_graphs(prox_graph1, prox_graph2, prox_graph_final):
    base_path = r"C:\Users\acer\KGs-Integration\files"
    merged_prox_graph = []

    with open(prox_graph1, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip()
            if parts:
                merged_prox_graph.append(parts)

    with open(prox_graph2, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip()
            if parts:
                merged_prox_graph.append(parts)

    with open(prox_graph_final, 'w', encoding='utf-8') as f_out:
        for line in merged_prox_graph:
            f_out.write(line + '\n')

    output_pickle = os.path.join(base_path, "pred_prox_graph_merge_before_align.pickle")
    with open(output_pickle, 'wb') as pkl_file:
        pickle.dump(merged_prox_graph, pkl_file)


def load_align_dict(file_path):
    align_dict = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip().strip('()')
            if not line:
                continue
            parts = [p.strip() for p in line.split(',')]
            if len(parts) == 2:
                align_dict[parts[0]] = parts[1]
            else:
                print(f"Riga malformata: {line}")
    return align_dict

def normalize_and_deduplicate(text, align_dict):
    seen = set()
    result = []

    for item in text.split(','):
        item = item.strip()
        substituted = align_dict.get(item, item)

        for part in substituted.split(','):
            part = part.strip()
            if part not in seen:
                seen.add(part)
                result.append(part)

    return ','.join(result)

def process_and_write(input_text_file, align_file, output_file):
    # Carichiamo dizionario
    align_dict = load_align_dict(align_file)

    # Leggiamo la riga di input
    with open(input_text_file, 'r', encoding='utf-8') as f:
        raw_text = f.read().strip()

    # Normalizziamo e rimuoviamo duplicati
    normalized_text = normalize_and_deduplicate(raw_text, align_dict)

    # Scriviamo output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(normalized_text + '\n')

def type_unique_valuation(type_before_file, type_after_file, results):
    # Leggiamo i tipi da file e trasformali in liste
    with open(type_before_file, 'r', encoding='utf-8') as f:
        type_before = f.read().strip().split(',')

    with open(type_after_file, 'r', encoding='utf-8') as f:
        type_after = f.read().strip().split(',')

    # Calcoliamo le statistiche
    unique_before = len(set(type_before))
    unique_after = len(set(type_after))
    reduction = unique_before - unique_after
    reduction_percent = (reduction / unique_before) * 100
    unified_types = set(type_before) - set(type_after)

    # Costruziamo il testo da salvare
    output_lines = [
        "=== Risultato Analisi Riduzione Tipi ===",
        f"Numero di tipi unici prima dell’allineamento: {unique_before}",
        f"Numero di tipi unici dopo l’allineamento: {unique_after}",
        f"Riduzione assoluta del numero di tipi: {reduction}",
        f"Riduzione percentuale: {reduction_percent:.2f}%",
        f"Tipi unificati (sostituiti): {sorted(unified_types)}",
        "========================================"
    ]

    # Scrittura su file
    with open(results, "w", encoding='utf-8') as results_file:
        for line in output_lines:
            results_file.write(line + "\n")

def load_predicates_from_txt(file_path):
    predicates = set()
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) == 3:
                predicates.add(parts[1])  # il predicato è in mezzo
    return predicates

def load_predicates_from_txt(file_path):
    predicates = set()
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) == 3:
                predicates.add(parts[1])
    return predicates

def embedding_predicate():
    before_path = r'C:\Users\acer\KGs-Integration\files\pred_prox_graph_merge_before_align.txt'
    after_path = r'C:\Users\acer\KGs-Integration\files\KGs_merged_pred_prox_graph.txt'
    result_path = r'C:\Users\acer\KGs-Integration\files\embedding_analysis_results.txt'
    image_path = r'C:\Users\acer\KGs-Integration\files\embedding_tsne_comparison.png'

    preds_before = load_predicates_from_txt(before_path)
    preds_after = load_predicates_from_txt(after_path)

    common_preds = sorted(preds_before & preds_after)
    num_common = len(common_preds)

    if num_common == 0:
        print("⚠️ Nessun predicato comune trovato.")
        return

    # Usa embedding reali da sentence-transformers
    model = SentenceTransformer('all-MiniLM-L6-v2')
    emb_before = model.encode(common_preds)
    emb_after = model.encode(common_preds)

    X_b_2d = TSNE(n_components=2, random_state=42, perplexity=15, init="pca", learning_rate="auto").fit_transform(emb_before)
    X_a_2d = TSNE(n_components=2, random_state=42, perplexity=15, init="pca", learning_rate="auto").fit_transform(emb_after)

    # Grafico
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))

    ax1.scatter(X_b_2d[:, 0], X_b_2d[:, 1], alpha=0.7)
    for i, label in enumerate(common_preds):
        ax1.annotate(label, (X_b_2d[i, 0], X_b_2d[i, 1]), fontsize=7, alpha=0.6)
    ax1.set_title("Prima dell’allineamento tipi")

    ax2.scatter(X_a_2d[:, 0], X_a_2d[:, 1], alpha=0.7)
    for i, label in enumerate(common_preds):
        ax2.annotate(label, (X_a_2d[i, 0], X_a_2d[i, 1]), fontsize=7, alpha=0.6)
    ax2.set_title("Dopo l’allineamento tipi")

    plt.tight_layout()
    plt.savefig(image_path)
    plt.close()

    # Scrittura risultati
    with open(result_path, 'w', encoding='utf-8') as f:
        f.write("=== Analisi Embedding Predicati ===\n")
        f.write(f"Numero di predicati prima: {len(preds_before)}\n")
        f.write(f"Numero di predicati dopo: {len(preds_after)}\n")
        f.write(f"Numero di predicati comuni per confronto: {num_common}\n")
        f.write("Predicati comuni:\n")
        for p in common_preds:
            f.write(f"- {p}\n")
        f.write(f"\nGrafico salvato in: {image_path}\n")
        f.write("===================================\n")

    print(f"✅ Completato. Risultati in:\n- {result_path}\n- {image_path}")