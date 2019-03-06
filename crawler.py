import re
from collections import Counter
import requests
from requests import Response
from bs4 import BeautifulSoup
from utils import save_json
import typing as t

JSON = t.Union[str, int, float, bool, None, t.Mapping[str, 'JSON'], t.List['JSON']]

def get_mp_list_response(is_verify:bool=False) -> Response:
    # TODO: Solve SSL warning (InsecureRequestWarning: Unverified HTTPS request is being made. 
    # Adding certificate verification is strongly advised. 
    # See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings InsecureRequestWarning))
    MP_LIST_URL : str = "https://www.tbmm.gov.tr/develop/owa/milletvekillerimiz_sd.liste"
    response = requests.get(MP_LIST_URL, verify=is_verify)
    return response

def get_mp_page_response(url:str, is_verify:bool=False) -> Response:
    # TODO: Solve SSL warning (InsecureRequestWarning: Unverified HTTPS request is being made. 
    # Adding certificate verification is strongly advised. 
    # See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings InsecureRequestWarning))
    response = requests.get(url, verify=is_verify)
    return response

def create_parser(response:Response) -> BeautifulSoup:
    bs = BeautifulSoup(response.text, 'html.parser')
    return bs

def parse_title(bs:BeautifulSoup) -> str:
    title = bs.find('span', {'class':'AltKonuBaslikB16Gri'}).text.strip()
    return title

def parse_tbmm_page(bs:BeautifulSoup, is_verbose:bool=False) -> JSON:
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

def parse_mp_page(bs:BeautifulSoup) -> t.Dict[str, str]:
    # TODO: Parse tasks better (currently list. Can be empty, singleten or multiple elements)
    # TODO: Parse contact better (currently list. Inconsistencies)
    # TODO: Parse CV better (currently response do not capture CV at all)
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
        'cv': mp_cv,
    }
    return mp_dict

def get_mp_list() -> t.Tuple[str, JSON]:
    r = get_mp_list_response()
    parser = create_parser(r)
    title = parse_title(parser)
    tbmm_json = parse_tbmm_page(parser)
    return title, tbmm_json

def get_mp_page(url:str) -> t.Dict[str, str]:
    mp_page_response = get_mp_page_response(url)
    parser = create_parser(mp_page_response)
    mp_dict = parse_mp_page(parser)
    return mp_dict 