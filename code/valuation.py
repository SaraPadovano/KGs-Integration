import pickle
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import os

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

def embedding_predicate():
    before_file = r'C:\Users\acer\KGs-Integration\files\pred_prox_graph_merge_before_align.pickle'
    after_file = r'C:\Users\acer\KGs-Integration\files\KGs_merged_pred_prox_graph.pickle'

    results_txt = r'C:\Users\acer\KGs-Integration\files\embedding_results.txt'
    output_img = r'C:\Users\acer\KGs-Integration\files\embedding_visualization.png'

    with open(before_file, 'rb') as f:
        emb_before = pickle.load(f)

    with open(after_file, 'rb') as f:
        emb_after = pickle.load(f)

    # Intersezione predicati comuni per confronto coerente
    common_preds = list(set(emb_before.keys()) & set(emb_after.keys()))
    print(f"🔗 Predicati comuni: {len(common_preds)}")
    num_common = len(common_preds)

    # Prepariamo array per t-SNE
    X_before = np.array([emb_before[p] for p in common_preds])
    X_after = np.array([emb_after[p] for p in common_preds])

    # Riduciamo la dimensionalità
    tsne = TSNE(n_components=2, random_state=42, perplexity=15, init="pca", learning_rate="auto")
    X_b_2d = tsne.fit_transform(X_before)
    X_a_2d = tsne.fit_transform(X_after)

    with open(results_txt, 'w', encoding='utf-8') as f:
        f.write("=== Embedding Predicate Alignment Results ===\n")
        f.write(f"Numero di predicati comuni per confronto: {num_common}\n")
        f.write(f"Dimensione originale embedding: {X_before.shape[1]}\n")
        f.write(f"Dimensione dopo riduzione t-SNE: {X_b_2d.shape[1]}\n")
        f.write("\nNota: la riduzione dimensionale è stata fatta separatamente per prima e dopo l’allineamento.\n")

    # Visualizzaziamo il tutto
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))

    # Prima dell'allineamento
    ax1.scatter(X_b_2d[:, 0], X_b_2d[:, 1], alpha=0.7)
    for i, label in enumerate(common_preds):
        ax1.annotate(label, (X_b_2d[i, 0], X_b_2d[i, 1]), fontsize=7, alpha=0.6)
    ax1.set_title("🔴 Prima dell’allineamento tipi")

    # Dopo l'allineamento
    ax2.scatter(X_a_2d[:, 0], X_a_2d[:, 1], alpha=0.7)
    for i, label in enumerate(common_preds):
        ax2.annotate(label, (X_a_2d[i, 0], X_a_2d[i, 1]), fontsize=7, alpha=0.6)
    ax2.set_title("🟢 Dopo l’allineamento tipi")

    plt.tight_layout()
    plt.savefig(output_img, dpi=300)
    plt.show()