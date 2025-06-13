import pickle
import numpy as np
from sklearn.manifold import TSNE
import os
from sentence_transformers import SentenceTransformer
from collections import defaultdict
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

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

def load_triples_from_txt(filepath):
    triples = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) == 3:
                triples.append(parts)
    return triples

def create_contextual_sentences_and_preds(triples):
    sentences = []
    clean_predicates = []
    for s_type, predicate, o_type in triples:
        s_type_clean = s_type.split('/')[-1].replace('>', '').replace('#', '')
        o_type_clean = o_type.split('/')[-1].replace('>', '').replace('#', '')
        predicate_clean = predicate.split('/')[-1].replace('>', '').replace('#', '').replace(':', '')

        sentence = f"The {s_type_clean} has a relationship {predicate_clean} with the {o_type_clean}."
        sentences.append(sentence)
        clean_predicates.append(predicate_clean)

    return sentences, clean_predicates

def aggregate_embeddings_by_predicate(embeddings_list, preds_list):
    aggregated_embeddings = defaultdict(list)
    for i, pred in enumerate(preds_list):
        aggregated_embeddings[pred].append(embeddings_list[i])

    # Calcoliamo la media per ogni predicato
    final_embeddings = {}
    for pred, emb_list in aggregated_embeddings.items():
        final_embeddings[pred] = np.mean(emb_list, axis=0)
    return final_embeddings

def embedding_predicate():
    before_path = r'C:\Users\acer\KGs-Integration\files\pred_prox_graph_merge_before_align.txt'
    after_path = r'C:\Users\acer\KGs-Integration\files\KGs_merged_pred_prox_graph.txt'
    result_path = r'C:\Users\acer\KGs-Integration\files\embedding_analysis_results.txt'
    image_path = r'C:\Users\acer\KGs-Integration\files\embedding_tsne_comparison.png'

    print("Inizio analisi embedding contestuali dei predicati.")

    # Carichiamo le triple da entrambi i file
    triples_before = load_triples_from_txt(before_path)
    triples_after = load_triples_from_txt(after_path)

    if not triples_before and not triples_after:
        print("⚠️ Nessuna tripla trovata nei file specificati.")
        return

    # Creiamo frasi contestuali e raccogli i predicati puliti
    sentences_before, clean_preds_list_before = create_contextual_sentences_and_preds(triples_before)
    sentences_after, clean_preds_list_after = create_contextual_sentences_and_preds(triples_after)

    model = SentenceTransformer('all-MiniLM-L6-v2')

    embeddings_raw_before = model.encode(sentences_before, convert_to_tensor=False)
    embeddings_raw_after = model.encode(sentences_after, convert_to_tensor=False)

    # Aggreghiamo gli embeddings per predicato unico (calcoliamo la media)
    print("Aggregazione degli embeddings per predicato unico (media)...")
    final_emb_before_dict = aggregate_embeddings_by_predicate(embeddings_raw_before, clean_preds_list_before)
    final_emb_after_dict = aggregate_embeddings_by_predicate(embeddings_raw_after, clean_preds_list_after)

    # Prepariamo i dati per t-SNE: solo i predicati comuni per un confronto diretto
    common_preds = sorted(list(set(final_emb_before_dict.keys()) & set(final_emb_after_dict.keys())))

    if not common_preds:
        print("⚠️ Nessun predicato comune trovato nei set aggregati. Impossibile generare il grafico comparativo.")
        # Utilizza result_path qui
        with open(result_path, 'w', encoding='utf-8') as f:
            f.write("=== Analisi Embedding Contestuali Aggregati ===\n")
            f.write(f"Numero di triple 'prima dell'allineamento': {len(triples_before)}\n")
            f.write(f"Numero di triple 'dopo l'allineamento': {len(triples_after)}\n")
            f.write("Nessun predicato comune trovato per la visualizzazione.\n")
            f.write("===============================================\n")
        print(f"Risultati base in: {result_path}")
        return

    preds_labels = []
    embeddings_for_tsne_before = []
    embeddings_for_tsne_after = []

    for pred in common_preds:
        preds_labels.append(pred)
        embeddings_for_tsne_before.append(final_emb_before_dict[pred])
        embeddings_for_tsne_after.append(final_emb_after_dict[pred])

    embeddings_for_tsne_before = np.array(embeddings_for_tsne_before)
    embeddings_for_tsne_after = np.array(embeddings_for_tsne_after)

    # Applichiamo t-SNE per ridurre la dimensionalità sugli embedding aggregati
    print(f"Applicazione t-SNE su {len(preds_labels)} predicati unici...")
    perplexity_val = min(len(preds_labels) - 1, 30) if len(preds_labels) > 1 else 1
    if perplexity_val <= 0:
        print("Meno di 2 predicati comuni, t-SNE non applicabile. Non verrà generato il grafico.")
        with open(result_path, 'w', encoding='utf-8') as f:
            f.write("=== Analisi Embedding Contestuali Aggregati ===\n")
            f.write(f"Numero di triple 'prima dell'allineamento': {len(triples_before)}\n")
            f.write(f"Numero di triple 'dopo l'allineamento': {len(triples_after)}\n")
            f.write("Meno di 2 predicati comuni, t-SNE non applicabile.\n")
            f.write("===============================================\n")
        print(f"Risultati base in: {result_path}")
        return

    tsne_before = TSNE(n_components=2, random_state=42, perplexity=perplexity_val, init="pca", learning_rate="auto")
    X_b_2d = tsne_before.fit_transform(embeddings_for_tsne_before)

    tsne_after = TSNE(n_components=2, random_state=42, perplexity=perplexity_val, init="pca", learning_rate="auto")
    X_a_2d = tsne_after.fit_transform(embeddings_for_tsne_after)

    # Generiamo il grafico di visualizzazione
    print("Generazione del grafico...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))

    ax1.scatter(X_b_2d[:, 0], X_b_2d[:, 1], alpha=0.8, s=50)
    for i, label in enumerate(preds_labels):
        ax1.annotate(label, (X_b_2d[i, 0], X_b_2d[i, 1]), fontsize=8, alpha=0.7, weight='bold')
    ax1.set_title("Contesto Predicati Aggregati - Prima dell’allineamento tipi")
    ax1.grid(True, linestyle='--', alpha=0.6)

    ax2.scatter(X_a_2d[:, 0], X_a_2d[:, 1], alpha=0.8, s=50)
    for i, label in enumerate(preds_labels):
        ax2.annotate(label, (X_a_2d[i, 0], X_a_2d[i, 1]), fontsize=8, alpha=0.7, weight='bold')
    ax2.set_title("Contesto Predicati Aggregati - Dopo l’allineamento tipi")
    ax2.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()
    plt.savefig(image_path)
    plt.close()
    print(f"Grafico salvato in: {image_path}")

    with open(result_path, 'w', encoding='utf-8') as f:
        f.write("=== Analisi Embedding Contestuali Aggregati dei Predicati ===\n")
        f.write(f"Numero di triple 'prima dell'allineamento': {len(triples_before)}\n")
        f.write(f"Numero di triple 'dopo l'allineamento': {len(triples_after)}\n")
        f.write(f"Numero di predicati unici comuni analizzati: {len(preds_labels)}\n")
        f.write("Predicati unici comuni:\n")
        for p in preds_labels:
            f.write(f"- {p}\n")
        f.write(f"\nGrafico di t-SNE salvato in: {image_path}\n")
        f.write("===============================================\n")

    print(f"✅ Completato. Risultati in:\n- {result_path}\n- {image_path}")