docker compose up
docker compose è il nome della sottofunzionalità, app crea i nostri container e li
attiva in automatico

non ho singoli container con questo tool ma un intero progetto
un compose è una collezione di container che partono assieme

scarica immagini se non sono scaricate
crea e fa partire i container
se è già stato creato il progetto fa solo partire

yml è come un file json, è un file di struttura
è una sintassi più simile a python

i services sono ogni nostra app

image è la stessa cosa di import in python per docker
from python import...
mysql e basta è come scrivere latest

environment, elenco variabili d'ambiente
perché mysql la password d'amministratore
viene scritta in una variabile d'ambiente

ogni coppia chiave valore è una stringa

3307 come port perché da per scontato che ci sia 
già un sql sul mio computer alla 3306

devo mappare le porte in uscita

restart always funziona in caso di crash ma
se stoppi compose si ferma il container, è normale

posso fare un compose sulla base di un dockerfile anche

nome backend totalemnte indipendente dal nome della cartella,
posso chiamarlo come voglio

COPY . . = cartella corrente progetto / cartella corrente docker, cioè /app

COPY ./backend/requirements.txt /app
copio il filre requirements nella root dell'app

le immagini le crea a livelli come matrioska
per ottimizzare la costruzione delle immagini
è meglio copiare i requirements e installarli