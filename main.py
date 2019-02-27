import requests
from bs4 import BeautifulSoup
import re

MP_LIST_URL = "https://www.tbmm.gov.tr/develop/owa/milletvekillerimiz_sd.liste"

def get_mp_list_response(is_verify:bool=False):
    response = requests.get(MP_LIST_URL, verify=False)
    return response

def create_parser(response):
    bs = BeautifulSoup(response.text, 'html.parser')
    return bs

def get_title(bs) -> str:
    title = bs.find('span', {'class':'AltKonuBaslikB16Gri'}).text.strip()
    return title

def get_cities(bs):
    rows = bs.find('table')
    cities = []
    for i, row in enumerate(rows):
        if i >= 2000:
            break
    #     print(i)
    #     print(row)
        
        is_city = row.find('span')
    #     print('is city', is_city)
        if is_city is not None and is_city != -1:
            city = is_city.text
            print("CITY: {}".format(city))
            city_dict = {'city': city, 'city_mps': []}
            cities.append(city_dict)
        
        else:
            is_mp = row.find('a')
            
    #         print('is_mp', is_mp)
            if is_mp is not None and is_mp != -1:
                mp_name = is_mp.text
                mp_url = is_mp.attrs['href']
                mp_party = row.findAll('td')[-1].text
                print("MP: {}".format(mp_name))
    #             print(mp_url)
                m = re.match("https://www.tbmm.gov.tr/develop/owa/milletvekillerimiz_sd.bilgi\?p_donem=(\d+)&p_sicil=(\d+)", mp_url)
                mp_term = m.group(1) # p_donem
                mp_registery = m.group(2) # p_sicil
                mp_dict = {
                            'name': mp_name,
                            'term': mp_term,
                            'party': mp_party,
                            'registery': mp_registery,
                            'url': mp_url,
                        }
                cities[-1]['city_mps'].append(mp_dict)

    return cities

if __name__ == '__main__':
    r = get_mp_list_response()
    parser = create_parser(r)
    title = get_title(parser)
    cities = get_cities(parser)

    print("Title: {}".format(title))
    # print(cities)
