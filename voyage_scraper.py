from cloudscraper import create_scraper
from bs4 import BeautifulSoup
import json
import pandas as pd
from cleantext import clean
from datetime import datetime

def main():
    session = create_scraper()
    res = session.get('https://seadream.com/voyages/')
    soup = BeautifulSoup(res.text, 'lxml')
    voyages = soup.select('.hover-me.voyage.large-3')
    p = 0
    voyage_item_list = []
    for voyage in voyages:
        p = p + 1
        print(f'Voyage: {p}')
        v_link = 'https://seadream.com' + voyage.select_one('a')['href']
        thumbnail = 'https://seadream.com' + voyage.select_one('img')['data-src']
        hero = 'https://seadream.com' + voyage.select_one('img')['data-src'].split('?')[0]
        item = get_data(v_link, thumbnail, hero)
        voyage_item_list.append(item)

    with open('voyages.json', 'w') as f:
        jsonString = json.dumps(voyage_item_list)
        f.write(jsonString)

def get_port(soup, table):
    data_list = []
    for port in get_port_data(soup):
        dt = table[table['Ports of Call'].str.contains(port['port name'].split('(')[0])].index.to_list()
        for d in dt:
            p = json.loads(table.iloc[d].to_json())
            p['port text'] = port['port text']
            p['port image'] = port['port image']
            data_list.append(p)
    sorted_json = sorted(data_list, key=lambda x: datetime.strptime(x['Date'], "%b %d, %Y"))
    return sorted_json

def get_port_data(soup):
    port_item_list = []
    section_port = soup.select_one('.ports.row')
    ports = section_port.select('.accordion-navigation')
    for port in ports:
        port_name = port.select_one('a.text-center').text.strip()
        try:
            port_image = port.select_one('div.content img.border')['data-cfsrc']
            if 'https://seadream.com' not in port_image:
                port_image = 'https://seadream.com' + port_image
        except:
            try:
                port_image = port.select_one('div.content img.border')['src']
                if 'https://seadream.com' not in port_image:
                    port_image = 'https://seadream.com' + port_image
            except:
                port_image = None
        port_text = str(port.select_one('div.content p').text.strip())
        try:
            port_text = clean(port_text, lowercase=False)
        except:
            port_text = None
        port_item = {
            'port name': port_name,
            'port text': port_text,
            'port image': port_image
        }
        port_item_list.append(port_item)
    return port_item_list

def get_data(link, thumbnail, hero):
    session = create_scraper()
    res = session.get(link)
    soup = BeautifulSoup(res.text, 'lxml')
    tables = pd.read_html(res.text)
    table = tables[0]
    name = soup.select_one('h2').text
    date = soup.select_one('.upcoming-date').text
    yatch = soup.select_one('.yacht').text
    number = soup.select_one('.voyage-number').text
    voyage_map = f'https://seadream.com/images/maps/{number}.jpg'
    port_data = get_port(soup, table)
    voyage_item = {
        'Name of Voyage': name.strip(),
        'Date': date.strip(),
        'SeaDream type': yatch.strip(),
        'Voyage number': number,
        'Thumbnail': thumbnail,
        'Image': hero,
        'Map': voyage_map,
        'Ports': port_data
    }
    return voyage_item





