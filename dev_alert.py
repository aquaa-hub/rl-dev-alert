import os
import requests

webhook = os.environ.get("DISCORD_WEBHOOK")

if webhook:
    requests.post(
        webhook,
        json={"content": "🟢 RL Dev Alert est connecté !"}
    )
