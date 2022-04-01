mport unittest
from unittest.mock import patch
import requests
from .src_func import call_api
from utils_obj import ConfigClient


# unittest.mock vs requests-mock
# requests-mock to decorate the whole class
# @requests_mock.Mocker()


class TestAPIWithPath(unittest.TestCse):  
    def setUp(self):
        self.url = "http://some-path.com"
        self.data = {"foo":"bar"}

    def test_call_api_ok(self):
        with patch("...?") as mock_request:
            # mock_request == mock instance
            ConfigClient.import_data(self.data)        
        mock_request.return_value = {"data":[1,2,3]}

    
