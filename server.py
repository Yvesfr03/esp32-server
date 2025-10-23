from flask import Flask, request
from datetime import datetime
import os

app = Flask(__name__)

commandes = {}

@app.route("/")
def home():
    return "Serveur relais ESP32 opérationnel."

@app.route("/set", methods=["GET", "POST"])
def set_cmd():
    device = request.args.get("device", "default")
    cmd = request.args.get("cmd", "")
    if not cmd:
        return "Aucune commande fournie."
    commandes[device] = {"cmd": cmd, "time": datetime.now()}
    return f"Commande '{cmd}' enregistrée pour {device}"

@app.route("/get")
def get_cmd():
    device = request.args.get("device", "default")
    if device in commandes:
        cmd = commandes[device]["cmd"]
        commandes.pop(device)
        return cmd
    return ""

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render fournit le port ici
    app.run(host="0.0.0.0", port=port)


