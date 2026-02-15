from flask import Flask, request, jsonify
import random, string, time

app = Flask(__name__)

keys_db = {}

def generate_key():
    chars = string.ascii_uppercase + string.digits
    return "XIT-" + "-".join(''.join(random.choice(chars) for _ in range(4)) for _ in range(3))

@app.route("/")
def home():
    return "Key System Online"

@app.route("/getkey")
def get_key():
    key = generate_key()
    expire = time.time() + 86400
    keys_db[key] = expire
    return f"YOUR KEY: {key}"

@app.route("/verify")
def verify():
    key = request.args.get("key")
    if key in keys_db:
        if time.time() < keys_db[key]:
            return jsonify({"status":"valid"})
        else:
            return jsonify({"status":"expired"})
    return jsonify({"status":"invalid"})

app.run(host="0.0.0.0", port=10000)
