# KGs-Alignment
Tesi di Laurea per il corso di Laurea in Informatica dell'Università di Bari Aldo Moro. L'argomento è l'integrazione dei due Knowledge Graphs in ambito giuridico creati dalle sentenze della Corte Europea sulla violenza sulle donne. Per l'integrazione si applicherà il sistema di AutoAlign studiato da Zhang, Su, Trisedya, Zhao, Yang, Cheng e Qi nell'articolo "AutoAlign: Fully Automatic and Effective Knowledge Graph Alignment Enabled by Large Language Model". La generazione dei due Knowledge Graphs è stata descritta nell'articolo "Automated Legal Knowledge Graph Generation Addressing Legislation on Violence Against Women". I due KGs generati devono essere integrati poichè costruiti con due metodologie diverse, con bottom-up e LLM, che hanno portato alla generazione di due ontologie e Knowlege Graphs diversi che vanno quindi integrati.

**NOTE BASE**
1) Utilizzo di python 3.6.13 (si può anche usare 3.7 ma poi bisogna usare versione di ternsorflow 1.15.0);
2) CUDA version 9.0;
3) CUDNN version 7.6.5;
4) Tensorflow versione 1.12.0

**INTEGRAZIONE CONDA CON PYCHARM PER INSTALLAZIONE SEMPLICE DI CUDA E CUDNN**
1) *CREA AMBIENTE CON ANACONDA*
   - conda create -n [nome_ambiente] python=[versione python];
   - conda activate [nome_ambiente];
   - conda installa cudatoolkit==[versione cuda] cudnn==[versione cudnn];
   - pip install [requirements] (se ci sono, in questo caso i requirements del progetto di AutoAlign]

3) *COLLEGA CONDA A PYCHARM*
   - apri progetto in pycharm;
   - vai su file > settings;
   - vai su project: [nome_progetto] > python interpreter (si può già trovare giù in basso a destra eventualmente);
   - vai su add interpreter;
   - vai su conda environment;
   - vai su existing environment;
   - seleziona l'environment già creato;
   - applica il tutto


**CONSIDERAZIONI**
- vuole il richiamo ad AutoAlign.py in una cartella per questione dei file (probabilmente questo non serve perchè dovremmo modificare il codice per mettere i nostri knowledge graphs);
- dà il superamento del 10% della memoria;
- bisognerebbe aggiungere qualcosa per capire dove ci si trova dopo l'ultimo print di test;
- si può verificare un problema pickle da crlf a lf perchè passaggio da linux a windows;
- problema di writer risolto;
- lento ma penso sia normale
