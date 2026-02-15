from flask import Flask, request, jsonify
import random, string, time

app = Flask(__name__)

# Base de datos temporal
keys_db = {}

# Generar key
def generate_key():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))

# Página principal
@app.route("/")
def home():
    return "KEY SYSTEM ONLINE"

# Obtener key
@app.route("/get_key")
def get_key():
    ip = request.remote_addr

    new_key = generate_key()
    expire = time.time() + 86400  # 24 horas

    keys_db[new_key] = expire

    return jsonify({
        "key": new_key,
        "expires_in_hours": 24
    })

# Verificar key
@app.route("/verify")
def verify():
    key = request.args.get("key")

    if key in keys_db:
        if time.time() < keys_db[key]:
            return jsonify({"status":"valid"})
        else:
            return jsonify({"status":"expired"})
    else:
        return jsonify({"status":"invalid"})

app.run(host="0.0.0.0", port=3000)
