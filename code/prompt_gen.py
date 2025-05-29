from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from sentence_transformers import SentenceTransformer, util
import logging

def union_typeset(file1, file2, fileUnion):
    seen = set()
    combined = []

    # Leggiamo entrambi i file e uniamo i contenuti separati da virgole
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        tokens = (f1.read() + ',' + f2.read()).split(',')
        for token in tokens:
            token = token.strip()
            if token and token not in seen:
                seen.add(token)
                combined.append(token)

    with open(fileUnion, 'w') as f_un:
        f_un.write(','.join(combined))


def list_to_str(lst):
    return ", ".join(x for x in lst)

def prompt(file1, file2, prompt_file):
    with open(file1, "r", encoding="utf-8") as f:
        # leggi il contenuto, poi split su ','
        typeset1 = f.read().strip().split(",")
        typeset1 = [x.strip() for x in typeset1]  # pulizia spazi

    with open(file2, "r", encoding="utf-8") as f:
        typeset2 = f.read().strip().split(",")
        typeset2 = [x.strip() for x in typeset2]

    promt_template = f"""Now you are an expert in linguistics and knowledge graphs. I will give you two sets of words, indicating the entity types from two knowledge graphs. You need to identify all the word pairs from the two sets that are synonyms. For example, if the first set has the word ‘people’ and the second set has the word 'person', you need to identify the two words being synonyms and return me the pair (people, person).
Now the following are the two sets:
Set 1: {list_to_str(typeset1)}
Set 2: {list_to_str(typeset2)}
Please return all the pairs that are synonyms from the two sets regarding entity types. Do not output the pairs if they are exactly the same. Each pair in one line. Each pair contains two types, one from Set 1 and another from Set 2.
"""

    with open(prompt_file, "w", encoding="utf-8") as f:
        f.write(promt_template)

def call_llm_without_api(prompt_file, match_file):
    # model_name = "tiiuae/falcon-7b-instruct" sarebbe ottimo con 16 GB di RAM ma io ne ho 8
    logging.getLogger("transformers.generation.utils").setLevel(logging.ERROR)

    model_name = "google/flan-t5-small"

    # Carica tokenizer e modello
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    # Legge il prompt dal file
    with open(prompt_file, "r", encoding="utf-8") as f:
        prompt = f.read()

    # Tokenizza con truncation
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
    prompt_truncated = tokenizer.decode(inputs.input_ids[0], skip_special_tokens=True)

    # Prepara la pipeline
    generator = pipeline("text2text-generation", model=model, tokenizer=tokenizer)

    # Genera la risposta
    response = generator(
        prompt_truncated,
        max_new_tokens=256,
        temperature=0.2,
        do_sample=True
    )

    # Salva il testo generato
    output = response[0]["generated_text"]
    with open(match_file, "w", encoding="utf-8") as f:
        f.write(output)

def load_words_from_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        line = f.readline()
        words = [w.strip() for w in line.split(',') if w.strip()]
    return words

def call_for_sim(match_file, file1, file2):
    model = SentenceTransformer('all-MiniLM-L6-v2')  # modello embedding leggero e veloce
    set1 = load_words_from_file(file1)
    set2 = load_words_from_file(file2)
    threshold = 0.4

    embeddings1 = model.encode(set1, convert_to_tensor=True)
    embeddings2 = model.encode(set2, convert_to_tensor=True)

    cos_scores = util.cos_sim(embeddings1, embeddings2)

    synonyms = []
    for i, word1 in enumerate(set1):
        for j, word2 in enumerate(set2):
            score = cos_scores[i][j].item()
            if score > threshold and word1 != word2:
                synonyms.append((word1, word2))

    with open(match_file, "w") as f:
        for w1, w2 in synonyms:
            f.write(f"({w1}, {w2})\n")

def another_try(prompt_file, match_file):
    model_name = "google/flan-t5-large"

    # Carica tokenizer e modello
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    #with open(prompt_file, "r", encoding="utf-8") as f:
        #prompt = f.read()

    prompt = "Find synonyms between these two sets: 1) word, people, cake e 2) persons, sweet, clown, candy. Give the output in pairs of synonyms"

    # Tokenizzazione con max 2048 token
    inputs = tokenizer(prompt, return_tensors="pt", max_length=600, truncation=True)

    # Genera output
    outputs = model.generate(**inputs, max_new_tokens=100)

    # Decodifica e stampa il risultato
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    with open(match_file, "w", encoding="utf-8") as f:
        f.write(result)
