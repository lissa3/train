import unittest
from unittest.mock import patch
import requests
from .src_func import call_api



class TestAPIWithPath(unittest.TestCse):  
    def setUp(self):
        self.url = "http://some-path.com"
        self.data = {"foo":"bar"}

    def test_call_api_ok(self):
        with patch("src.requests") as mock_request:
            # mock_request == mock instance
            call_api(self.url,self.data)        
        mock_request.return_value = {"data":[1,2,3]}

    def test_call_api_exeption_context(self):
        with patch("src.requests") as mock_request:   
            mock_request.get.side_effect = requests.HTTPError         
            result = call_api(self.url,self.data )      
            self.assertEqual(result,{}) 


    @patch("src.requests", side_effect=HTTPError)
    def test_call_api_exeption_decor(self):
        with patch("src.requests") as mock_request:   
            result = call_api(self.url,self.data )      
            self.assertEqual(result,{})         


