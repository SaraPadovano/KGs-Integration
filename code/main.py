import sys
import os
import warnings
import importlib.util

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