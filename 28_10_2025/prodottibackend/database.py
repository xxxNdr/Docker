import mysql.connector as db


def connect():
    conn = db.connect(
        host="db",
        port=3306,
        user="root",
        password="database",
        database="negozio")
    return conn


def get_all(query):
    conn = connect()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def execute(query):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()
    return True
