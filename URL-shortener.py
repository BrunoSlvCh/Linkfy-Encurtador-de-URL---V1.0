from flask import Flask, request, redirect, render_template
import sqlite3
import random
import string

conn = sqlite3.connect("urls.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS urls (
id INTEGER PRIMARY KEY AUTOINCREMENT,
original_url TEXT NOT NULL,
short_code TEXT UNIQUE NOT NULL
)
""")

conn.commit()
conn.close()

app = Flask(__name__)

def gerar_codigo(tamanho=6):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(tamanho))

def salvar_url(original, codigo):
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO urls (original_url, short_code) VALUES (?, ?)",
        (original, codigo)
    )

    conn.commit()
    conn.close()

def buscar_url(codigo):

    with sqlite3.connect("urls.db") as conn:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT original_url FROM urls WHERE short_code=?",
                (codigo,)
    )

    resultado = cursor.fetchone()

    conn.close()

    return resultado
    
@app.route("/")
def home():
    return render_template("shortener.html")

@app.route("/encurtar", methods=["POST"])
def encurtar():

    original = request.form["url"]
    codigo = gerar_codigo()

    while buscar_url(codigo):
        codigo = gerar_codigo()

    salvar_url(original, codigo)

    short_url = f"http://localhost:5000/{codigo}"

    return render_template("shortener.html", short_url=short_url)


@app.route("/<codigo>")
def redirecionar(codigo):

    resultado = buscar_url(codigo)

    if resultado:
        return redirect(resultado[0])
    else:
        return "URL não encontrada."
    
if __name__ == "__main__":
    app.run(debug=True)

    