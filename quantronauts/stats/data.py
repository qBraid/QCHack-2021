import os
import requests


def stats(winner: str):
    """Gen stats to GitHub Actions
    Args:
        winner: winner of the game
    """
    TOKEN = os.environ.get("GITHUB_TOKEN")

    if TOKEN is not None:
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {TOKEN}",
        }

        data = {
            "event_type": "games-stats",
            "client_payload": {
                "game": "qnim",
                "winner": f"{winner}"
            }
        }

        r = requests.post(
            url="https://api.github.com/repos/mickahell/robots-data/dispatches",
            headers=headers,
            json=data
        )

    else:
        print("Your token is empty ! The stats aren't updated.")
