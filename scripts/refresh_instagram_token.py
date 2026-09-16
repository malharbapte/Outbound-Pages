#!/usr/bin/env python3
"""Refresh the long-lived Instagram token (they last about 60 days).

Prints the new token so the workflow can store it back as a repository secret.
"""
import json
import os
import sys
import urllib.parse
import urllib.request

token = os.environ.get("IG_TOKEN", "").strip()
if not token:
    sys.exit("IG_TOKEN is not set.")

query = urllib.parse.urlencode({"grant_type": "ig_refresh_token", "access_token": token})
with urllib.request.urlopen(f"https://graph.instagram.com/refresh_access_token?{query}", timeout=30) as response:
    data = json.load(response)

print(data["access_token"])
