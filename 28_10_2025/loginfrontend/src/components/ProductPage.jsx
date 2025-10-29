import { useEffect, useState } from "react";

function ProductPage() {
  const [prodotti, setProdotti] = useState([]);
  async function getData() {
    let response = await fetch("http://127.0.0.1:8002/api/prodotti");
    let data = await response.json();
    setProdotti(data);
  }

  useEffect(() => {
    getData();
  }, []);

  return (
    <>
      <ul>
        {prodotti.map((prodotto) => (
          <Prodotto key={prodotto.id} prodotto={prodotto} />
        ))}
      </ul>
    </>
  );
}

function Prodotto({ prodotto }) {
  async function handleClick() {
    let response = await fetch("http://127.0.0.1:8002/api/aggiungiProdotto", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(prodotto),
    });
    let data = await response.json();
    alert(data.message)
  }

  return (
    <>
      <div>
        <h1>{prodotto.nome}</h1>
        <p>{prodotto.descrizione}</p>
        <h2>{prodotto.prezzo}</h2>
        <button onClick={handleClick}>Acquista</button>
      </div>
    </>
  );
}

export default ProductPage;
