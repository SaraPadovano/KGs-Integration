# KGs-Alignment
Tesi di Laurea per il corso di Laurea in Informatica dell'Università di Bari Aldo Moro. L'argomento è l'integrazione dei due Knowledge Graphs in ambito giuridico creati dalle sentenze della Corte Europea sulla violenza sulle donne. Per l'integrazione si applicherà il sistema di AutoAlign studiato da Zhang, Su, Trisedya, Zhao, Yang, Cheng e Qi nell'articolo "AutoAlign: Fully Automatic and Effective Knowledge Graph Alignment Enabled by Large Language Model". La generazione dei due Knowledge Graphs è stata descritta nell'articolo "Automated Legal Knowledge Graph Generation Addressing Legislation on Violence Against Women". I due KGs generati devono essere integrati poichè costruiti con due metodologie diverse, con bottom-up e LLM, che hanno portato alla generazione di due ontologie e Knowlege Graphs diversi che vanno quindi integrati.

**NOTE BASE**
1) Utilizzo di python 3.6.13 (si può anche usare 3.7 ma poi bisogna usare versione di ternsorflow 1.15.0)---- meglio usare python 3.7 per aggiornare versione rdflib;
2) CUDA version 9.0;
3) CUDNN version 7.6.5;
4) Tensorflow versione 1.12.0;
5) Scaricare il progetto di AutoAlign dal repsository indicato nell'articolo prima di far andare tutto perchè serve per il path del richiamo di AutoAlign.py (che poi nel codice va modificato in base a dove viene scaricato il progetto);
6) avere installato anaconda;
7) aver scaricato il progetto del collega Rubini "EVA-KG" (ricordarsi di modificare il path per la lettura del file dell'ontologia nel codice in base a dove si è scaricato il progetto)

**INTEGRAZIONE CONDA CON PYCHARM PER INSTALLAZIONE SEMPLICE DI CUDA E CUDNN**
1) *CREA AMBIENTE CON ANACONDA*
   - conda create -n [nome_ambiente] python=[versione python];
   - conda activate [nome_ambiente];
   - conda installa cudatoolkit==[versione cuda] cudnn==[versione cudnn];
   - pip install [requirements] (se ci sono, in questo caso i requirements del progetto di AutoAlign + requests + transformers==4.28.1 + torch==1.13.1 + sentence_transformers + dotenv + matplotlib)

3) *COLLEGA CONDA A PYCHARM*
   - apri progetto in pycharm;
   - vai su file > settings;
   - vai su project: [nome_progetto] > python interpreter (si può già trovare giù in basso a destra eventualmente);
   - vai su add interpreter;
   - vai su conda environment;
   - vai su existing environment;
   - seleziona l'environment già creato;
   - applica il tutto

**PASSAGGI EFFETTUATI NEL CODICE**
   - integrato nel codice il file Jupiter per la creazione del grafo di prossimità e per ottenere gli insiemi dei tipi di entità (nome file: *KB_entity_type*). Per consentirne la modifica (perchè serve sostituire il path dello script con i path dei due grafi) è stato trasformato da file Jupiter a file .py con il comando : jupyter nbconvert --to script KB_entity_type.ipynb. Eseguito dal terminale anaconda nella cartella in cui è presente il file (si vedrà nella stessa cartella lo script con lo stesso nome in formato .py);
