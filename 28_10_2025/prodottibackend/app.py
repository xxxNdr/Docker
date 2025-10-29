from decimal import Decimal
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
import database as db


class Prodotto(BaseModel):
    id: int
    nome: str
    descrizione: str
    prezzo: Decimal


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/prodotti")
def get_prodotti():
    return db.get_all("select * from prodotti")


@app.put("/api/aggiungiProdotto")
def aggiungi_prodotto(prodotto: Prodotto):
    exist = db.get_all(f"SELECT * FROM carrello WHERE idp = {prodotto.id}")

    if exist:
        db.execute(
            f"UPDATE carrello SET quantita = quantita + 1 WHERE idp = {prodotto.id}"
        )
    else:
        db.execute(
            f"INSERT INTO carrello (idp, quantita) VALUES ({prodotto.id}, 1)"
        )
    return {"success": True, "message": f"+1 {prodotto.nome}"}


@app.get("/api/carrello")
def get_carrello():
    query = "SELECT c.quantita, p.nome, p.prezzo FROM carrello c JOIN prodotti p ON c.idp = p.id"
    return db.get_all(query)


uvicorn.run(app, host="0.0.0.0", port=8000)
