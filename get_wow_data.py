import requests
from settings import WOW_API_KEY, LOCALE, REGION
from constants import *
import json

def get_data(name, realm):
    path = 'https://%s.api.battle.net/wow/character/%s/%s?locale=%s&apikey=%s' % (
        REGION, realm, name, LOCALE, WOW_API_KEY)
    try:
        request = requests.get(path)
        request.raise_for_status()
        request_json = request.json()
    except requests.exceptions.RequestException as error:
        request_json = ''
        print(error)
    return request_json

def get_json_info(path):
    try:
        request = requests.get(path)
        request.raise_for_status()
        request_json = request.json()
    except requests.exceptions.RequestException as error:
        request_json = ''
        print(error)
    return request_json
