from flask import Flask, request
from datetime import datetime
import os

app = Flask(__name__)

# --- stockage des commandes en attente ---
commandes = {}
# --- journal des dernières actions ---
logs = []

def log(message):
    """Enregistre et affiche un message horodaté"""
    horodatage = datetime.now().strftime("%H:%M:%S")
    ligne = f"[{horodatage}] {message}"
    logs.append(ligne)
    # garde seulement les 30 dernières lignes
    if len(logs) > 30:
        logs.pop(0)
    print(ligne, flush=True)

@app.route("/")
def home():
    return "Serveur relais ESP32 opérationnel."

@app.route("/set", methods=["GET", "POST"])
def set_cmd():
    """Automate envoie une commande"""
    device = request.args.get("device", "default")
    cmd = request.args.get("cmd", "")
    if not cmd:
        return "Aucune commande fournie."
    commandes[device] = {"cmd": cmd, "time": datetime.now()}
    log(f"Commande reçue pour {device}: {cmd}")
    return f"Commande '{cmd}' enregistrée pour {device}"

@app.route("/get")
def get_cmd():
    """L’ESP32 récupère la commande"""
    device = request.args.get("device", "default")
    if device in commandes:
        cmd = commandes[device]["cmd"]
        log(f"Commande envoyée à {device}: {cmd}")
        commandes.pop(device)
        return cmd
    log(f"Aucune commande en attente pour {device}")
    return ""

@app.route("/status")
def status():
    """Page Web de supervision"""
    html = "<h2>Serveur relais ESP32</h2>"
    html += "<h3>Commandes en attente :</h3><ul>"
    if commandes:
        for dev, info in commandes.items():
            t = info['time'].strftime('%H:%M:%S')
            html += f"<li><b>{dev}</b> → {info['cmd']} (ajoutée à {t})</li>"
    else:
        html += "<li>Aucune commande en attente</li>"
    html += "</ul><h3>Derniers logs :</h3><pre>"
    html += "\n".join(logs)
    html += "</pre>"
    return html

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    log(f"Serveur démarré sur le port {port}")
    app.run(host="0.0.0.0", port=port)



