from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

# Dictionnaire pour stocker la dernière commande par appareil
commandes = {}

@app.route("/")
def home():
    return "Serveur relais ESP32 opérationnel."

@app.route("/set", methods=["GET", "POST"])
def set_cmd():
    """Reçoit une commande depuis Automate"""
    device = request.args.get("device", "default")
    cmd = request.args.get("cmd", "")
    if not cmd:
        return "Aucune commande fournie."
    commandes[device] = {"cmd": cmd, "time": datetime.now()}
    return f"Commande '{cmd}' enregistrée pour {device}"

@app.route("/get")
def get_cmd():
    """Renvoie la commande au bon ESP32"""
    device = request.args.get("device", "default")
    if device in commandes:
        cmd = commandes[device]["cmd"]
        commandes.pop(device)  # efface après lecture
        return cmd
    return ""  # pas de commande à exécuter

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

