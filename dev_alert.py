import os
import requests

WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

def send_alert(message):
    if not WEBHOOK:
        print("DISCORD_WEBHOOK manquant")
        return

    response = requests.post(
        WEBHOOK,
        json={"content": message},
        timeout=10
    )

    print("Discord:", response.status_code)

send_alert(
    "🟢 **RL Dev Alert**\n"
    "Le détecteur fonctionne correctement.\n"
    "Source : signalement public à vérifier."
)
