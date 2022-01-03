from unittest import TestCase
from unittest.mock import MagicMock
from src.APIGateway import APIGateway

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
    def test_pass_add_location_bias(self, mock_open: MagicMock, mock_get: MagicMock) -> None:
        inputs = [(-89.9, -179.9), (0.1, 0.9), (90, 180)]
        expecteds = ["-89.9,-179.9", "0.1,0.9", "90,180"]
        for input, expected in zip(inputs, expecteds):
            with self.subTest():
                gw = APIGateway('credentials.json')
                gw.add_location_bias(input)
                self.assertEqual(expected, gw._LOCATION_BIAS)
    
    @mock_fn('builtins.open', lambda: mock_open('{"API_KEY": "abcedfghijklmnopqrstuv"}'))
    @mock_fn('requests.get', lambda: mock_response(200, 'sjdgsg'))
    def test_fail_add_location_bias(self, mock_open: MagicMock, mock_get: MagicMock) -> None:
        inputs = [(-180, 0), (95, 10), (5, -200), (10, 181)]
        for input in inputs:
            with self.subTest(f"Failed with input {input}"):
                gw = APIGateway('credentials.json')
                self.assertRaises(ValueError, lambda: gw.add_location_bias(input))