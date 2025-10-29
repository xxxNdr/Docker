import { use, useState } from "react";
import "./App.css";
import ProductPage from "./components/ProductPage";

function App() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [response, setResponse] = useState(undefined);

  async function handleSubmit(e) {
    e.preventDefault();
    let response = await fetch("http://127.0.0.1:8001/api/login", {
      method: "POST",
      body: JSON.stringify({ username, password }),
      headers: {
        "Content-Type": "application/json",
      },
    });
    let data = await response.json();
    setResponse(data);
  }
  return (
    <>
      {(!response || !response.success) && (
        <form onSubmit={handleSubmit}>
          <input
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <input
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button>Login</button>
        </form>
      )}
      {response && (
        <>
          <h1>{response.message}</h1>
          {response.success && <ProductPage />}
        </>
      )}
    </>
  );
}

export default App;
