import re
from collections import Counter
import requests
from bs4 import BeautifulSoup
from utils import save_json

MP_LIST_URL = "https://www.tbmm.gov.tr/develop/owa/milletvekillerimiz_sd.liste"

def get_mp_list_response(is_verify:bool=False):
    response = requests.get(MP_LIST_URL, verify=is_verify)
    return response

def get_mp_page_response(url:str, is_verify:bool=False):
    response = requests.get(url, verify=is_verify)
    return response

def create_parser(response):
    bs = BeautifulSoup(response.text, 'html.parser')
    return bs

def get_title(bs) -> str:
    title = bs.find('span', {'class':'AltKonuBaslikB16Gri'}).text.strip()
    return title

def parse_mp_list_old(bs, is_verbose:bool=False):
    rows = bs.find('table')
    cities = []
    for i, row in enumerate(rows):

        if is_verbose:
            print(i)
            print(row)
        
        is_city = row.find('span')

        if is_verbose:
            print('is city', is_city)

        if is_city is not None and is_city != -1:
            city = is_city.text
            city_dict = {'city': city, 'city_mps': []}
            cities.append(city_dict)

            if is_verbose:
                print("CITY: {}".format(city))

        else:
            is_mp = row.find('a')
            
            if is_verbose:
                print('is_mp', is_mp)

            if is_mp is not None and is_mp != -1:
                mp_name = is_mp.text
                mp_url = is_mp.attrs['href']
                mp_party = row.findAll('td')[-1].text
                mp_city = city

                if is_verbose:
                    print("MP: {}, Party: {}".format(mp_name, mp_party))
                    print(mp_url)

                m = re.match("https://www.tbmm.gov.tr/develop/owa/milletvekillerimiz_sd.bilgi\?p_donem=(\d+)&p_sicil=(\d+)", mp_url)
                mp_term = m.group(1) # p_donem
                mp_registery = m.group(2) # p_sicil
                mp_dict = {
                            'name': mp_name,
                            'city': mp_city,
                            'term': mp_term,
                            'party': mp_party,
                            'registery': mp_registery,
                            'url': mp_url,
                        }
                cities[-1]['city_mps'].append(mp_dict)

    return cities

def parse_mp_list(bs, is_verbose:bool=False):
    rows = bs.find('table')
    cities = []
    mps = []
    for i, row in enumerate(rows):

        if is_verbose:
            print(i)
            print(row)
        
        is_city = row.find('span')

        if is_verbose:
            print('is city', is_city)

        if is_city is not None and is_city != -1:
            city = is_city.text
            city_dict = {'name': city, 'num_of_mps': 0}
            cities.append(city_dict)

            if is_verbose:
                print("CITY: {}".format(city))

        else:
            is_mp = row.find('a')
            
            if is_verbose:
                print('is_mp', is_mp)

            if is_mp is not None and is_mp != -1:
                mp_name = is_mp.text
                mp_url = is_mp.attrs['href']
                mp_party = row.findAll('td')[-1].text
                mp_city = city

                if is_verbose:
                    print("MP: {}, Party: {}".format(mp_name, mp_party))
                    print(mp_url)

                m = re.match("https://www.tbmm.gov.tr/develop/owa/milletvekillerimiz_sd.bilgi\?p_donem=(\d+)&p_sicil=(\d+)", mp_url)
                mp_term = m.group(1) # p_donem
                mp_registery = m.group(2) # p_sicil
                mp_dict = {
                            'name': mp_name,
                            'city': mp_city,
                            'term': mp_term,
                            'party': mp_party,
                            'registery': mp_registery,
                            'url': mp_url,
                        }
                mps.append(mp_dict)
                cities[-1]['num_of_mps'] += 1

    parties = [{'name':k, 'num_of_mps':v} for k, v in Counter(map(lambda x: x["party"], mps)).items()]
    tbmm_json = {'cities':cities, 'mps':mps, 'parties':parties}
    
    return tbmm_json

def parse_mp_page(bs):
    mp_name = bs.find('div', {'id': 'mv_isim'}).text.strip()
    mp_term = bs.find('div', {'id': 'mv_ili'}).text.strip().split(' ')[0][:-1]
    mp_city = bs.find('div', {'id': 'mv_ili'}).text.strip().split(' ')[2]
    mp_task = bs.find('div', {'id': 'mv_gorev'}).text.strip().split('\xa0')
    mp_photo_url = bs.find('div', {'id': 'fotograf_alani'}).find('img')['src']
    mp_party_logo_url = bs.find('div', {'id': 'parti_logo'}).find('img')['src']
    mp_contact = [m.text.strip() for m in bs.find('div', {'id': 'iletisim_bilgi'}).findAll('tr') if len(m.text.strip()) > 0]
    mp_cv = bs.find('div', {'id': 'ozgecmis_icerik'})
    mp_dict = {
        'name': mp_name,
        'term': mp_term,
        'city': mp_city,
        'tasks': mp_task,
        'photo_url': mp_photo_url,
        'party_logo_url': mp_party_logo_url,
        'contact': mp_contact,
        # 'mp_cv': mp_cv,
    }
    return mp_dict

def get_mp_list():
    r = get_mp_list_response()
    parser = create_parser(r)
    title = get_title(parser)
    cities = parse_mp_list(parser)
    return title, cities

def get_mp_page(url:str):
    mp_page_response = get_mp_page_response(url)
    parser = create_parser(mp_page_response)
    mp_dict = parse_mp_page(parser)
    return mp_dict

def get_city_name_list(cities):
    return list(map(lambda x: x['city'], cities))

def get_city_num_of_mps_list(cities):
    return list(map(lambda x: len(x['city_mps']), cities))

def get_city_json(cities):
    name_list = get_city_name_list(cities)
    num_of_mps_list = get_city_num_of_mps_list(cities)

    city_json = []
    for name, num_of_mps in zip(name_list, num_of_mps_list):
        city_json.append({"name":name, "num_of_mps":num_of_mps})

    return city_json

def get_mp_json(cities):
    mp_json = []

    for city in cities:
        mp_json += city["city_mps"]

    return mp_json

def get_party_json(cities):
    cntr = Counter([item for lst in list(map(lambda x: list(map(lambda y: y['party'], x['city_mps'])), cities)) for item in lst])

    party_json = []
    for k, v in cntr.items():
        party_json.append({"name":k, "num_of_mps":v})

    return party_json

def get_party_list(cities):
    return list(set([item for lst in list(map(lambda x: list(set(map(lambda y: y['party'], x['city_mps']))), cities)) for item in lst]))

if __name__ == '__main__':
    # Return title and cities
    title, tbmm = get_mp_list()
    save_json(tbmm, "tbmm.json")

    # # Get mp page
    # url = "https://www.tbmm.gov.tr/develop/owa/milletvekillerimiz_sd.bilgi?p_donem=27&p_sicil=7542"
    # print(get_mp_page(url))

    # # Get city list
    # print(get_city_list(cities))

    # # Get party list
    # print(get_party_list(cities))