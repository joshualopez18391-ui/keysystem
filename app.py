from flask import Flask, request
import random, string, time

app = Flask(__name__)

# Base temporal
keys_db = {}

# Generar key aleatoria
def generate_key():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))

# Página principal
@app.route("/")
def home():
    return "KEY SYSTEM ONLINE"

# ESTA ES LA IMPORTANTE (cuando vuelven de linkvertise)
@app.route("/getkey")
def getkey():

    # Linkvertise siempre manda parámetros en la URL
    if "r" not in request.args:
        return "Access Denied (No Linkvertise)"

    # crear key
    key = generate_key()

    # guardar por 24 horas
    keys_db[key] = time.time() + 86400

    return f"""
    <h2>TU KEY ES:</h2>
    <h1>{key}</h1>
    <p>Duración: 24 horas</p>
    """

# Verificar key (Roblox usa esto)
@app.route("/verify")
def verify():
    user_key = request.args.get("key")

    if user_key in keys_db:
        if time.time() < keys_db[user_key]:
            return "VALID"
        else:
            del keys_db[user_key]
            return "EXPIRED"

    return "INVALID"

app.run(host="0.0.0.0", port=5000)
