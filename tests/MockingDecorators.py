from unittest.mock import MagicMock, mock_open as unittest_mock_open, patch

from requests.models import Response


def mock_fn(fn_name, mock_builder, **builder_kwargs):

    def wrapper(f):
        @patch(fn_name, new_callable=mock_builder, **builder_kwargs)
        def inject_mock(mock, *args, **kwargs):
            return f(mock, *args, **kwargs)
        return inject_mock
    
    return lambda fn: wrapper(fn)

def _create_response(code, content):
    response = Response()
    response.status_code = code
    response._content = content
    return response

def mock_response(code, content):
    mock_obj = MagicMock(name='requests.get', spec=__import__('requests').get)
    mock_obj.return_value = _create_response(code, content)
    return mock_obj

def mock_open(content):
    return unittest_mock_open(read_data=content)