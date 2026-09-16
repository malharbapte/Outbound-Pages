#!/usr/bin/env python3
"""Fetch the latest posts from Outbound RVs' Instagram and save them into the site.

Run by .github/workflows/instagram.yml on a schedule. Needs one environment variable:

    IG_TOKEN   a long-lived Instagram access token for a Professional (Business or Creator) account

It writes:
    assets/instagram/<id>.jpg   the thumbnail of each post
    instagram.json              what the page reads: image, link, caption and date

If the token is missing or Instagram refuses the request, nothing is written and the page keeps
whatever it had (or its placeholder tiles), so a failed run can never empty the strip.
"""
import json
import os
import pathlib
import sys
import urllib.parse
import urllib.request

COUNT = 12                     # posts to show in the strip
ROOT = pathlib.Path(__file__).resolve().parent.parent
IMAGES = ROOT / "assets" / "instagram"
FEED = ROOT / "instagram.json"
FIELDS = "id,caption,media_type,media_url,thumbnail_url,permalink,timestamp"


def get(url, **params):
    query = urllib.parse.urlencode(params)
    with urllib.request.urlopen(f"{url}?{query}", timeout=30) as response:
        return json.load(response)


def main():
    token = os.environ.get("IG_TOKEN", "").strip()
    if not token:
        sys.exit("IG_TOKEN is not set: add it as a repository secret.")

    posts = get("https://graph.instagram.com/me/media", fields=FIELDS, limit=COUNT, access_token=token)
    items = []
    IMAGES.mkdir(parents=True, exist_ok=True)
    for post in posts.get("data", [])[:COUNT]:
        # Videos and reels carry a still in thumbnail_url; photos use media_url.
        source = post.get("thumbnail_url") or post.get("media_url")
        if not source:
            continue
        name = f"{post['id']}.jpg"
        path = IMAGES / name
        if not path.exists():
            urllib.request.urlretrieve(source, path)
        caption = (post.get("caption") or "").strip().splitlines()
        items.append({
            "image": f"assets/instagram/{name}",
            "link": post.get("permalink", "https://www.instagram.com/"),
            "caption": caption[0][:120] if caption else "Instagram post",
            "date": post.get("timestamp", ""),
        })

    if not items:
        sys.exit("Instagram returned no posts; leaving the last feed in place.")

    FEED.write_text(json.dumps({"posts": items}, indent=2) + "\n")

    # Drop thumbnails that are no longer in the feed, so the folder does not grow for ever.
    keep = {pathlib.Path(item["image"]).name for item in items}
    for old in IMAGES.glob("*.jpg"):
        if old.name not in keep:
            old.unlink()

    print(f"Saved {len(items)} posts to {FEED.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
