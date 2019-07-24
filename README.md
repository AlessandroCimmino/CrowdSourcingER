# CrowdSourcingER

Implementazione di una pipeline iterativa con lo scopo di espandare la ground truth di un dataset di fotocamere
riconoscendo quali istanze del dataset rappresentano la stessa entità del mondo reale.

Di seguito sono riportate due metodi di esecuzione del progetto.
Il primo si basa su un esecuzione in locale e quindi prevede l'installazione di tutte le componenti descritte nei pre-requisiti.
Il secondo descrive un'esecuzione in remoto utilizzando gli ambienti già configurati all'interno dei server Enit e Tesla messi a disposizione dall'Università degli Studi Roma Tre e quindi necessita di password.

## Esecuzione in locale

### Pre-requisiti

- Python 3.6
- Spark (consigliato 2.3.3)
- MongoDB (consigliato 4.0.10)
- pymongo
- pymongo_spark
- py_entitymatching
- deepmatcher

Configurare Spark in modo tale che possa eseguire Python 3.6.

Effettuare la connessione di Spark a MongoDB.

### Start
Effetuare l'edit del file config.py andando a specificare nelle variabili sotto riportate l'host e la porta
sulla quale il demone di MongoDB è in esecuzione
```
MONGO_HOST = "enit.inf.uniroma3.it"
MONGO_PORT = "8080"
```
#### Prima esecuzione
Posizionarsi all'interno della cartella principale ed eseguire il comando
```
sh initialize.sh
```

Per verificare la corretta creazione del database contenente la ground truth eseguire i comandi seguenti
andando a specificare il corretto uri per la connessione a MongoDB. Il comando dovrebbe mostrare la creazione
di un database "ground_truth"
```
python3

from pymongo import MongoClient
c = MongoClient("mongodb://enit.inf.uniroma3.it:8080")
c.list_database_names()
```

#### Esecuzione di un ciclo
All'interno della cartella principale eseguire il comando
```
sh start.sh
```
**Il processo di predizione può richiedere fino a 2h se non si ha a disposizione una GPU potente.**

Le predizioni effettuate possono essere trovate all'interno della cartella
```
./classifiers/<blackbox>/prediction_files
```
Un file per ogni blackbox

#### Oracolo
Per etichettare le predizioni eseguire il comando
```
sh start_oracolo.sh
```
Verrà aperto un notebook jupyter nel quale dovrà essere eseguito Oracolo.ipynb.

Una volta etichettate tutte le predizioni cliccare il pulsante save per salvare il file
```
./oracolo/true_preditioncs.csv
```
**Nota bene: il file può essere salvato solo se vengono etichettate tutte le coppie di istanze**

#### Espandere la ground truth
Per espandere la ground truth a partire dal file in uscita dall'oracolo eseguire
```
sh expand_gt.sh
```
Per verificare la corretta esecuzione
```
python3

from pymongo import MongoClient
c = MongoClient("mongodb://enit.inf.uniroma3.it:8080")
c.list_database_names()
```
Verificare che ci siano i database ground_truth e ground_false(contenente le predizioni negative dell'oracolo).
Per controllare i nomi delle collezioni eseguire il comando
```
c.*nome_database*.list_collection_names()
```
Per visualizzare gli elementi delle collezioni eseguire
```
import pprint
for e in c.*nome_database*.*nome_collezione*.find():
    pprint.pprint(e)
```



## Quick-start Tesla

Connettersi alla Tesla tramite il comando
```
ssh nvidia@tesla.inf.uniroma3.it
```
Attivare l'environment di anaconda
```
conda activate testenv
```
Posizionarsi all'interno della cartella del progetto
```
cd workspace/dbgroup/benchmark/CrowdSourcingER
```

### Prima esecuzione

Per la prima esecuzione eseguire
```
sh initialize.sh
```
 
Per verificare la corretta creazione del database contenente la ground truth eseguire
```
python3

from pymongo import MongoClient
c = MongoClient("mongodb://enit.inf.uniroma3.it:8080")
c.list_database_names()
```

### Esecuzione di un ciclo

Controllare lo stato delle GPU
```
nvidia-smi
```
Eseguire un ciclo della pipeline utilizzando le GPU libere specificandone l'id
```
CUDA_VISIBLE_DEVICE = 0,1 sh start.sh
```
Il processo può richiede fino a 20 minuti, dipende dal numero di GPU utilizzate


Le predizioni possono essere trovate all'interno della cartella
```
./classifiers/<blackbox>/prediction_files
```
Un file per ogni blackbox

### Oracolo
Per etichettare le predizioni eseguire il comando
```
sh start_oracolo.sh
```
Verrà avviato un notebook di jupyter con associato un link che apparirà sulla shell.
```
http://localhost:8989/?token=0a8aa13f83e307310006721ad0ffe0b44e90d65465206b37
```
Aprire una nuova shell ed effettuare un port tunneling tramite il seguente comando,
andando a sostituire il numero delle porte con quello specificato nel link.
```
ssh -N -f -L 8888:localhost:8888 nvidia@tesla.inf.uniroma3.it
```
Copiare il link del notebook nel browser, aprire il file Oracolo.ipynb ed eseguire il run.
Una volta etichettate tutte le predizioni cliccare il pulsante save per salvare il file
```
./oracolo/true_preditioncs.csv
```
**Nota bene: il file può essere salvato solo se vengono etichettate tutte le coppie di istanze**

Terminare il processo del notebook sulla Tesla


### Espandere la ground truth
Per espandere la ground truth a partire dal file in uscita dall'oracolo eseguire
```
sh expand_gt.sh
```
Per verificare la corretta esecuzione
```
python3

from pymongo import MongoClient
c = MongoClient("mongodb://enit.inf.uniroma3.it:8080")
c.list_database_names()
```
Verificare che ci siano i database ground_truth e ground_false(contenente le predizioni negative dell'oracolo).
Per controllare i nomi delle collezioni eseguire il comando
```
c.*nome_database*.list_collection_names()
```
Per visualizzare gli elementi delle collezioni eseguire
```
import pprint
for e in c.*nome_database*.*nome_collezione*.find():
    pprint.pprint(e)
```



