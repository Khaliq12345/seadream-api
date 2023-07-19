from voyage_scraper import main
import json
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def scrape():
    main()
    # Opening JSON file
    with open('voyages.json') as json_file:
        data = json.load(json_file)
    return data
