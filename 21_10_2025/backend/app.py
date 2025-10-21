import mysql.connector as db
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def leggi():
    conn = db.connect(
        host="127.0.0.1",
        port=3307,
        user="root",
        password="database",
        database="21_10_2025",
    )

    print("Connessione avvenuta al DB: " + conn.database)

    cursor = conn.cursor(dictionary=True)
    cursor.execute("select * from users")
    rows = cursor.fetchall()

    tutte = ' | '.join(str(v) for row in rows for v in row.values())
    print(tutte)
    return tutte

import uvicorn
uvicorn.run(app, host='0.0.0.0', port=8000)