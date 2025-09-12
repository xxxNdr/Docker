FROM python:3.13.4-slim
# versione ridotta dell'immagine, tolte dipendenze non necessarie
# diminuendo così la dimensione dell'immagine
# ultima versione ufficiale di python
WORKDIR /app
# directory interna al container, se non esiste viene creata
COPY basic02.py .
# copia il file dalla cartella in cui c'è Dockerfile alla directory
# di lavoro /app all'interno del container
#  COPY richiede sorgente e destinazione
# . indica di copiare il file nella cartella corrente del container
CMD [ "python", "basic02.py" ]
# definisce il comando che sarà eseguito all'avvio del container
# Python esegue basic02.py


#####################################################
#   AVVIA DOCKER DESKTOP                            #
#####################################################
#   APRI CMD NELLA CARTELLA DOVE C'É Dockerfile     #
#####################################################


# docker build -t (nome immagine) . #
# dice a Docker di costruire un'immagine
# basata sul Dockerfile nella cartella corrente (.)
# assegna un tag, un nome all'immagine risultante
# così da identificarla facilmente
# se hai modificato il file da eseguire
# questo comando è utile per aggiornare l'immagine


# docker run (nome immagine) #
# crea ed esegue un container dall'immagine indicata
# ma il container non viene eliminato automaticamente
# dopo l'esecuzione
# rimane nello stato Exited dopo che il processo
# è terminato


######################################################
#   COMANDI VARI                                     #
######################################################


# docker images #
# elenca tutte le immagini Docker presenti localmente
# sul tuo sistema 


# docker ps -a #
# mostra tutti i container Docker presenti
# indipendentemente dal loro stato


# docker ps #
# mostra solo i container attualmente in esecuzione


# docker run --name (nome container) (nome immagine) #
# crea un container con un nome specifico
# e non casuale


# docker run -d (nome immagine) #
# esegue un container in modalità detached (secondo piano)
# il container continua l'esecuzione anche se chiudi
# il terminale
# utile per eseguire app che devono restare attive
# tipo server web


# docker run --rm (nome immagine) #
# esegue un container e lo elimina automaticamente
# quando termina
# utile per test o quando non ti interessa mantenere
#  lo stato del container dopo la fine


# docker rename (vecchio nome) (nuovo nome) #
# rinomina un container generato con nome casuale


# docker start (nome container) #
# avvia un container fermo senza collegare il terminale
# all'input/output del container
# non potrai interagire con quello che esegue il file


# docker start -ai (nome container) #
# vieni collegato al terminale del container
# puoi vedere l'output in tempo reale
# e inviare input al container (digiare comandi)


# docker stop (nome o id container) #
# ferma un container


# docker rm (nome o id container) #
# elimina il container MA PRIMA
# lo devi fermalre


# docker rm -f (nome o id container) #
# elimina forzatamente un container
# anche se è in esecuzione