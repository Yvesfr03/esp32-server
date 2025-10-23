from flask import Flask, request
from datetime import datetime
import os

app = Flask(__name__)

# Dictionnaire pour stocker les commandes
commandes = {}

def log(message):
    """Affiche un log horodaté dans la console Render"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}", flush=True)

@app.route("/")
def home():
    return "Serveur relais ESP32 opérationnel."

@app.route("/set", methods=["GET", "POST"])
def set_cmd():
    """Enregistrement d'une commande"""
    device = request.args.get("device", "default")
    cmd = request.args.get("cmd", "")
    if not cmd:
        return "Aucune commande fournie."
    commandes[device] = {"cmd": cmd, "time": datetime.now()}
    log(f"Commande reçue pour {device}: {cmd}")
    return f"Commande '{cmd}' enregistrée pour {device}"

@app.route("/get")
def get_cmd():
    """Lecture de commande par l'ESP32"""
    device = request.args.get("device", "default")
    if device in commandes:
        cmd = commandes[device]["cmd"]
        log(f"Commande envoyée à {device}: {cmd}")
        commandes.pop(device)
        return cmd
    log(f"Aucune commande en attente pour {device}")
    return ""

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    log(f"Serveur démarré sur le port {port}")
    app.run(host="0.0.0.0", port=port)


