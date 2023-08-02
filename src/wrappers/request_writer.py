from datetime import datetime
import uuid
from pathlib import Path
from typing import Callable
from functools import wraps

from src.m_logging import Logger

TEST_DATA_DIR = Path('../test_data')
TEST_DATA_DIR.mkdir(exist_ok=True)

start_time_str = datetime.now().strftime("%H_%M_%S__%d_%b_%Y")
logger_inst = Logger(log_file_path=Path(f'../test_logs/{start_time_str}.log'))
logger = logger_inst.get_logger(__name__)


def log_connections(make_request: Callable):
    """

    :param make_request: The make_request function from the API class.
    This function receives the request bytes and returns:
        1. The header part
        2. Response bytes
    Note: Don't return the header part if the return_header argument is set to False.

    :type make_request: Callable


    :return:
    """

    def transform_response(response_val):
        """
        This function transforms the response as needed.
        :param response_val: The response value returned by the make_request function.
        :return: A dict with the following keys:
            1. type: The type of the response. Can be one of the following:
                1. image: The response is an image. The path to the image is stored in the path key.
                2. text: The response is a text. The text is stored in the val key.
                3. json: The response is a json. The json is stored in the val key.
                4. none: The response is None. The value is stored in the val key.
                5. unknown: The response is of unknown type. The value is stored in the val key.
            2. val: The value of the response. Or, the path to the image if the type is image.
        """
        _resp = {}
        # convert the response as needed.
        if isinstance(response_val, bytes):
            fname = uuid.uuid4().hex + '.png'
            fpath = TEST_DATA_DIR / fname
            fpath.write_bytes(response_val)
            _resp = {
                'type': 'image',
                'val': str(fpath)
            }
        elif isinstance(response_val, str):
            _resp = {
                'type': 'text',
                'val': response_val
            }
        elif isinstance(response_val, dict):
            _resp = {
                'type': 'json',
                'val': response_val
            }
        elif not response_val:
            _resp = {
                'type': 'none',
                'val': response_val
            }
        else:
            _resp = {
                'type': 'unknown',
                'val': str(response_val)
            }
        return _resp

    @wraps(make_request)
    def make_request_wrapper(*args, **kwargs):
        """
        This function wraps the make_request function from the API class.

        :param args:
        :param kwargs:
        :return:
        """
        return_header = kwargs.get('return_header', False)
        # args[0] is the self argument.
        request_bytes = args[1]
        return_vals = make_request(*args, **kwargs)
        header_string, response_val = return_vals

        _resp = transform_response(response_val)

        connection_log = {
            'request': request_bytes.decode('utf-8'),
            'response': _resp,
            'header': header_string
        }
        logger.info(connection_log)

        if return_header:
            return header_string, response_val

        return response_val

    return make_request_wrapper
