# STRUTTURA GENERALE
# 4 SERVIZI DOCKER

LOGIN FRONT-END → REACT APP LOGIN E VISUALIZZAZIONE PRODOTTI
LOGIN BACK-END → FASTAPI CHE GESTISCE LOGIN
PRODOTTI BACK-END → FASTAPI CHE GESTISCE PRODOTTI E CARRELLO
DB → MYSQL, TABELLE prodotti, carrello, users


# FLUSSO DELL'APP

1. Login
L'utente apre loginfrontend attraverso React
compila utente e passowrd
React invia una richiesta POST a http://127.0.0.1:8001/api/login
loginbackend verifica chi può passare solo con credenziali: admin, admin
if user.username == 'admin... else: ...

Se il login ha successo React mostra ProductPage


2. Visualizzazione Prodotti
ProductPage chiama 127.0.0.1:8002/api/prodotti
prodottibackend risponde con i dati dal DB (tabella prodotti)
Python: SELECT * FROM prodotti
React mostra i prodotti in lista con un bottone 'acquista'


3. Aggiunta al Carrello
Quando clicchi acquista React invia una richiesta PUT a
http://127.0.0.1:8002/api/aggiungiProdotto
prodottibackend controlla se il prodotto è già nel carrello
se sì → aggiorna quantità
se no → inserisce una nuova riga
Python: UPDATE carrello SET quantita = quantita + 1 WHERE idp = prodotto.id
    oppure
INSERT INTO carrello (idp, quantita) VALUES (prodotto.id, 1)


4. Database
CREATE TABLE users (...);
CREATE TABLE prodotti (...);
CREATE TABLE carrello (...);

Popolato con:
INSERT INTO prodotti VALUES
(default,'cotoletta','buonissima',4.12),
(default,'tofu','molto umami',5.61);


# FILE PRINCIPALI

- loginbackend/app.py
Gestisce il login con FastAPI
- prodottibackend/app.py
Gestisce i prodotti, carrello e connessione al DB
- prodottibackend/database.py
Connessione a MySQL usando mysql-connector-python
- loginfrontend/App.jsx
Gestisce form di login e visualizza la pagina prodotti
se login riuscito
- loginfrontend/components/ProductPage.jsx
Mostra lista prodotti + pulsante acquisto


# DOCKER

docker-compose.yml
Crea e collega 4 servizi
```yml
services:
  loginfrontend: ...
  loginbackend: ...
  prodottibackend: ...
  db: ...
```
Dockerfile loginbackend/prodottibackend
Basati su python:3.14-alpine
 - Installano FastAPIe uvicorn
 - Espongono porta 8000

 Dockerfile loginfrontend
 Basato su node:25-alpine
 - Installa dipendenze
 - Lancia npm run dev -- --host
 per rendere React accessibile da altri container


###### ###########
## PER RIFARLO ###
# ################

1. Crea le cartelle:
- loginfrontend/
- loginbackend/
- prodottibackend/

2. In ognuna metti:
- Dockerfile
- file app.py (o codice React in caso front-end)
- requirements.txt per backend

3. Scrivi docker-compose.yml alla radice

4. Crea lo script SQL (es. init.sql)
e importalo nel DB MySQL:
```sql
-- Cancella e ricrea il database
DROP DATABASE IF EXISTS negozio;
CREATE DATABASE negozio;
USE negozio;

-- Tabella utenti
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(100) NOT NULL,
  password VARCHAR(100) NOT NULL
);

-- Tabella prodotti
CREATE TABLE prodotti (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(50) NOT NULL,
  descrizione VARCHAR(255),
  prezzo DECIMAL(7,2)
);

-- Tabella carrello
CREATE TABLE carrello (
  id INT AUTO_INCREMENT PRIMARY KEY,
  idp INT NOT NULL,
  quantita INT,
  FOREIGN KEY (idp) REFERENCES prodotti(id)
);

-- Dati iniziali
INSERT INTO prodotti VALUES
(default, 'cotoletta', 'buonissima e croccantissima', 4.12),
(default, 'tofu', 'molto umami', 5.61),
(default, 'acqua', 'sottomarca', 0.17),
(default, 'padella', 'antiaderente', 12.99);

-- (Facoltativo) Un utente di test
INSERT INTO users VALUES (default, 'admin', 'admin');
```

Nel tuo docker-compose.yml, aggiungi questo volume
sotto il servizio db:
```yml
db:
  image: mysql
  ports:
    - 3308:3306
  environment:
    MYSQL_ROOT_PASSWORD: database
  volumes:
    - db_data:/var/lib/mysql
    - ./init.sql:/docker-entrypoint-initdb.d/init.sql
```

Così facendo quando Docker crea il container MySQL
per la prima volta esegue automaticamente init.sql
Quando lanci docker compose up --build
il database 'negozio' sarà già pronto con tabelle e dati


5. Avvia tutto
docker compose up --build

6. Apri React su http://localhost:8501
Login: admin, admin

7. Vedi i prodotti e puoi aggiungerli al carrello


# RIASSUNTO CONCETTUALE

Componente	        Linguaggio	    Porta	    Funzione
loginfrontend	    React	        8501	    UI + chiamate API
loginbackend	    FastAPI	        8001	    Autenticazione
prodottibackend	    FastAPI	        8002	    Prodotti + carrello
db	                MySQL	        3308	    Dati persistenti


# ##################################################################
# ####### 1. COS'È UN DOCKERFILE ###################################
# ##################################################################
Il Dockerfile è la ricetta per costruire un'immagine
Serve per dire a Docker:
    - da dove partire a costruire l'immagine
    - costa installare
    - quali file copiare
    - quale comando eseguire all'avvio


# ##################################################################
# ####### 2. DOCKERFILE BACKEND (FastAPI) ##########################
# ##################################################################
Esempio:
```Dockerfile
FROM python:3.14-alpine3.21
WORKDIR /app
COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
EXPOSE 8000
```

Spiegazione:
Riga	                                                        Significato
FROM python:3.14-alpine3.21	                                    Usa come base un’immagine Python leggera (Alpine = più piccola).
WORKDIR /app	                                                Imposta la cartella di lavoro interna (tutti i comandi successivi si eseguono lì).
COPY ./requirements.txt .	                                    Copia il file dei requisiti Python.
RUN pip install --no-cache-dir --upgrade -r requirements.txt	Installa i pacchetti necessari (FastAPI, uvicorn, mysql-connector, ecc.).
COPY . .	                                                    Copia tutto il codice sorgente nel container.
EXPOSE 8000	                                                    Indica che il container userà la porta 8000 (per Uvicorn).

<Il comando d’avvio non è nel Dockerfile,
ma nel docker-compose.yml>

Extra-spiegazione:
# /app è un percorso dentro il file system del container, non sul tuo PC.
# È simile a una directory Linux: / è la root del container, e /app è una cartella lì dentro.
# Se /app non esiste, Docker la crea automaticamente.


# ##################################################################
# ####### 3. DOCKERFILE FRONTEND (React) ###########################
# ##################################################################
```Dockerfile
FROM node:25-alpine3.21
WORKDIR /app
COPY . .
RUN npm install
EXPOSE 5173
```

Spiegazione:
# Riga	                                    Significato
FROM node:25-alpine3.21	                    Immagine Node.js leggera per eseguire React/Vite.
WORKDIR /app	                            Imposta la cartella di lavoro interna.
COPY . .	                                Copia tutto il progetto React nel container.
RUN npm install	                            Installa le dipendenze (react, vite, ecc.).
EXPOSE 5173	                                React/Vite usa la porta 5173 per lo sviluppo.

<Anche qui, l’avvio del server (npm run dev -- --host)
è deciso nel docker-compose.yml>

Extra-spiegazione:
💡 Quindi se hai:

```Dockerfile
WORKDIR /app
COPY . .
```

e nel docker-compose.yml:
```yaml
build:
  context: ./loginfrontend
```

👉 Docker farà questo:
```bash
[HOST PC] ./loginfrontend/*  --->  [CONTAINER] /app/*
```

Cioè:
- prende tutti i file e cartelle del progetto React sul tuo computer
- e li copia dentro la directory /app del container.


# ##################################################################
# ################ 4. DOCKER COMPOSE YAML ##########################
# ##################################################################
Il docker-compose.yml serve per orchestrare più container insieme
Li costruisce, li collega in rete e gestisce le dipendenze

```yml
services:
  loginfrontend:
    build:
      context: loginfrontend       # dove si trova il Dockerfile
      dockerfile: Dockerfile
    ports:
      - 8501:5173                  # esterno:interno → React visibile su localhost:8501
    volumes:
      - ./loginfrontend:/app       # sincronizza il codice host ↔ container
      - /app/node_modules          # evita conflitti dei moduli locali
    command: npm run dev -- --host # avvia il server React accessibile da rete

  loginbackend:
    build:
      context: ./loginbackend
      dockerfile: Dockerfile
    ports:
      - 8001:8000                  # backend login su porta 8001
    volumes:
      - ./loginbackend:/app        # modifica codice senza rebuild
    command: python app.py
    depends_on:
      - db                         # aspetta che MySQL sia pronto

  prodottibackend:
    build:
      context: ./prodottibackend
      dockerfile: Dockerfile
    ports:
      - 8002:8000                  # backend prodotti su porta 8002
    volumes:
      - ./prodottibackend:/app
    command: python app.py
    depends_on:
      - db

  db:
    image: mysql                   # usa immagine MySQL ufficiale
    ports:
      - 3308:3306                  # DB accessibile da host
    environment:
      MYSQL_ROOT_PASSWORD: database # password del root
    volumes:
      - db_data:/var/lib/mysql     # volume persistente per i dati

volumes:
  db_data:                         # definisce il volume per il DB
```

🔄 5️⃣ COME FUNZIONA IL FLUSSO DOCKER COMPOSE

1️⃣ docker compose up --build
👉 crea le immagini da ogni Dockerfile
👉 avvia tutti i container insieme

2️⃣ Tutti i servizi stanno nella stessa rete virtuale
React chiama http://127.0.0.1:8001 → va al login backend
Prodotti backend parla con db (il nome del servizio è il nome host Docker)

3️⃣ volumes:
permettono di modificare il codice sul PC
e vedere subito i cambiamenti nel container (utile in sviluppo)

4️⃣ depends_on:
assicura che db parta prima dei backend, così non falliscono la connessione

5️⃣ ports:
collegano le porte interne (container) a quelle esterne (host)


🧠 RIASSUNTO CONCETTUALE
# File	                Scopo	                                    Dove agisce
Dockerfile	            Costruisce un’immagine singola	            Dentro ogni servizio
docker-compose.yml	    Lancia e collega più container	            Radice del progetto
volumes	                Sincronizzano file e salvano dati	        Tra host e container
ports	                Espongono servizi al browser o a Postman	Host ↔ container
depends_on	            Gestisce l’ordine d’avvio	                Tra container