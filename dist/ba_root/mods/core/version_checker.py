
import _ba
import json
import urllib.request
import asyncio

update_file = _ba.env["python_directory_user"], "updates.json"

async def main():
    with open(update_file, "r") as f:
        prev = json.load(f)
    URL = "https://raw.githubusercontent.com/itsre3/bombsquad-server/main/dist/ba_root/mods/core/updates.json"
    resp = urllib.request.urlopen(URL)
    data = json.load(resp)
    assert data is not None
    if data == prev:
        print("Running on latest version")
    else:
        update = data["updates_info"][0]
        print(f"New Updates detected: {update}\n Run git pull to update")

def run():
    asyncio.run(main())