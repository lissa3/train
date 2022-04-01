import requests

from .models import Config


class ConfigClient:
    def __init__(self):
        self.config = Config.get_solo()
        self.headers = {
            "content-type": "application/json",
            "authorization": f"Token {self.config.api_key}",
        }
    def import_data(self, data):       

        try:
            resp = requests.get(self.config.api_endpoint, data, headers=self.headers)
            if resp.status_code == 200:
                print("import successful")       
        except requests.exceptions.ConnectionError as err:
            print("Error Connecting:", err)
        except requests.exceptions.Timeout:
            print("Timeout Error. Try again?")
        except requests.exceptions.HTTPError as err:
            print("HTTP greet : Something Else", err)
        except requests.exceptions.RequestException as err:
            print("Url does not exist", err)
            return {}
    

    
    