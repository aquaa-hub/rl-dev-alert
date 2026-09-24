import os
import requests
import time

WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

URLS = [
    "https://www.reddit.com/r/RocketLeague/search.json?q=%22dev%20boost%22&restrict_sr=1&sort=new&limit=10",
    "https://www.reddit.com/r/RocketLeague/search.json?q=developer&restrict_sr=1&sort=new&limit=10"
]

def send_discord(message):
    requests.post(
        WEBHOOK,
        json={"content": message},
        timeout=10
    )

for url in URLS:
    response = requests.get(
        url,
        headers={"User-Agent": "RL-Dev-Alert/1.0"},
        timeout=10
    )

    if response.status_code != 200:
        print("Erreur Reddit :", response.status_code)
        continue

    posts = response.json()["data"]["children"]

    for post in posts:
        data = post["data"]

        title = data["title"]
        permalink = "https://reddit.com" + data["permalink"]

        message = (
            "🚨 **RL DEV SIGNALÉ**\n"
            f"📝 {title}\n"
            f"🔎 Source : Reddit\n"
            f"🔗 {permalink}"
        )

        send_discord(message)

        time.sleep(1)
