import os
import requests
import time

WEBHOOK = os.environ.get("DISCORD_WEBHOOK")
SEEN_FILE = "seen_posts.txt"

def load_seen():
    if not os.path.exists(SEEN_FILE):
        return set()

    with open(SEEN_FILE, "r", encoding="utf-8") as file:
        return set(line.strip() for line in file if line.strip())

def save_seen(seen):
    with open(SEEN_FILE, "w", encoding="utf-8") as file:
        for post_id in seen:
            file.write(post_id + "\n")

def send_discord(message):
    if not WEBHOOK:
        print("DISCORD_WEBHOOK manquant")
        return

    response = requests.post(
        WEBHOOK,
        json={"content": message},
        timeout=10
    )

    print("Discord :", response.status_code)

seen = load_seen()

URLS = [
    "https://www.reddit.com/r/RocketLeague/search.json?q=%22dev%20boost%22&restrict_sr=1&sort=new&limit=10",
    "https://www.reddit.com/r/RocketLeague/search.json?q=developer&restrict_sr=1&sort=new&limit=10"
]

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
        post_id = data["id"]

        if post_id in seen:
            continue

        seen.add(post_id)

        title = data["title"]
        permalink = "https://reddit.com" + data["permalink"]

        message = (
            "🚨 **RL DEV SIGNALÉ**\n"
            f"📝 {title}\n"
            "🔎 Source : Reddit\n"
            f"🔗 {permalink}"
        )

        send_discord(message)
        time.sleep(1)

save_seen(seen)
