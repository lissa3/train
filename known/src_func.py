from urllib.error import HTTPError
import requests
import json
import logging

def call_api(url,data):
    try:
        resp = requests.post(url=url,data=data)
        result =json.loads(resp.json())
    except (ConnectionError,HTTPError):
        logging.warn("Fetched nothing")
        result = {}
    return result    

