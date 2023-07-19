from voyage_scraper import main
import json
from fastapi import FastAPI
from dropbox import Dropbox
import os
import config


def download_file(file):
    token = config.key
    dbx = Dropbox(token)
    # read a file
    with open(file, 'wb') as f:
        metadata, result = dbx.files_download(path='/Voyage/voyages.json')
        f.write(result.content)

app = FastAPI()

@app.get('/')
async def scrape():
    download_file('voyages.json')
    # Opening JSON file
    with open('voyages.json') as json_file:
        data = json.load(json_file)
    return data