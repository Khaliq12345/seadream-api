import json
from fastapi import FastAPI
from dropbox import Dropbox
import config


def download_file(file):
    dbx = Dropbox(oauth2_refresh_token=config.refresh_token,
              app_key=config.app_key, app_secret=config.app_secret)
    # read a file
    with open(file, 'wb') as f:
        metadata, result = dbx.files_download(path='/Voyage/silverSea_voyages.json')
        f.write(result.content)

app = FastAPI()

@app.get('/')
async def scrape():
    download_file('silverSea_voyages.json')
    # Opening JSON file
    with open('silverSea_voyages.json') as json_file:
        data = json.load(json_file)
    return data
