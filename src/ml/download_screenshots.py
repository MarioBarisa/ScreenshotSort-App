import os
from asyncio import timeout
from io import  BytesIO
from pathlib import Path
from time import sleep
import requests
from dotenv import load_dotenv
from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
SAMPLES = Path(__file__).resolve().parent/"samples"
LIMIT_PER_GAME = 50

GAMES = {
    "genshin": "genshin-impact",
    "gta": "grand-theft-auto-iv",
    "zelda": "the-legend-of-zelda-breath-of-the-wild",
    "kena": "kena-bridge-of-spirits",
    "cyberpunk": "cyberpunk-2077",
    "tlou": "the-last-of-us",
    "pokemon": "pokemon-legends-z-a"
}

def get_credentials():
    load_dotenv(ROOT/".env")
    client_id=os.getenv("SCREENSHOTSORT_IGDB_CLIENT_ID", "").strip()
    client_secret=os.getenv("SCREENSHOTSORT_IGDB_CLIENT_SECRET", "").strip()
    if not client_id or not client_secret:
        raise  SystemExit(f"Set api keys in .env file ( root )")
    return client_id, client_secret

def get_token(session, client_id, client_secret):
    response = session.post(
        "https://id.twitch.tv/oauth2/token",
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials",
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["access_token"]

def get_game(session, head, slug):
    sleep(0.3)
    response=session.post(
        "https://api.igdb.com/v4/games",
        headers=head,
        data=f'fields name, screenshots.image_id; where slug="{slug}"; limit 1;',
        timeout=30
    )

    response.raise_for_status()
    games=response.json()
    if not games:
        raise  RuntimeError(f"IGDB did not find a game: {slug}")
    return games[0]


def download_image(session, image_id, destination):
    url=f"https://images.igdb.com/igdb/image/upload/t_1080p/{image_id}.jpg"
    response = session.get(url, timeout=30)
    response.raise_for_status()
    with Image.open(BytesIO(response.content)) as image:
        image.verify()
    temp = destination.with_suffix(".part")
    try:
        temp.write_bytes(response.content)
        temp.replace(destination)
    finally:
        temp.unlink(missing_ok=True)

def main():
        client_id, client_secret=get_credentials()
        with requests.Session() as session:
            token = get_token(session, client_id, client_secret)
            headers = {
                "Client-ID": client_id,
                "Authorization": f"Bearer {token}"
            }

            for label, slug in GAMES.items():
                game= get_game(session,headers, slug)
                screenshots = game.get("screenshots", [])
                folder = SAMPLES / label
                folder.mkdir(parents=True, exist_ok=True)
                print(f"\n{game['name']}: available {len(screenshots)}\n")


                for screenshot in screenshots[:LIMIT_PER_GAME]:
                    image_id=screenshot["image_id"]
                    if not image_id or any(
                            character not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-"
                            for character in image_id
                    ):
                        raise ValueError("IGDB returned invalid image_id.")
                    destination = folder / f"{image_id}.jpg"
                    if destination.is_file() and destination.stat().st_size > 0:
                        print(f"Skipped: {destination.name}")
                        continue
                    download_image(session, image_id, destination)
                    print(f"Saved: {destination.name}")

                print(f"\nDone, saved in: {SAMPLES}")


if __name__ == '__main__':
    main()
