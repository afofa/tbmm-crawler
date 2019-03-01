import json
import os
from typing import List

def load_json(path:str="creds/twitter_credentials.json"):
    # Load credentials from json file
    with open(path, "r") as file:  
        creds = json.load(file)

    return creds

def save_json(data, path:str, **kwargs):
    if "makedirs" in kwargs.keys():
        dirrs = kwargs["makedirs"]
        for dirr in dirrs:
            os.makedirs(dirr, exist_ok=True)
    with open(path, 'w') as outfile:
        json.dump(data, outfile)