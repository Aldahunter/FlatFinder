from unittest import TestCase, main
from unittest.mock import MagicMock, patch, Mock
from src.APIGateway import APIGateway
from requests import Response
from functools import partial, wraps

from tests.MockingDecorators import mock_fn, mock_response, mock_open

# def mock_request_get(code, content):

#     def wrapped(f):

#         @patch('requests.get', new_callable=mock_response, code=code, content=content)
#         def add_response(mock_get, *args, **kwargs):
#             return f(mock_get, *args, **kwargs)
#         return add_response
#     return lambda fn: wrapped(fn)



# def mock_open(content):
#     return unittest_mock_open(read_data=content)


class APIGatewayTests(TestCase):
    
    @mock_fn('builtins.open', lambda: mock_open('{"API_KEY": "abcedfghijklmnopqrstuv"}'))
    @mock_fn('requests.get', lambda: mock_response(200, 'sjdgsg'))
    def test_add_location_bias(self, mock_get: MagicMock, mock_open: MagicMock) -> None:
        gw = APIGateway('credentials.json')
        print(mock_get.call_args)
        print(mock_open.call_args)
        self.assertEqual('foo'.upper(), 'jjjyf')