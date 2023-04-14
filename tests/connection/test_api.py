import pytest
from src.connection.api import API

import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


class TestApi:
    
    @pytest.fixture(autouse=True, scope='class')
    def setup_api(self):
        # --- API connection settings ---
        host = 'xmr.poker'
        port = 443
        connect_ssl = True
        socks_ip = "127.0.0.1"
        socks_port = 9050
        socks5 = False
        # -------------------------------
        
        self.api = API(
            RUNTIME_COOKIE='',
            host=host,
            port=port,
            tls=connect_ssl,
            socks5_ip=socks_ip,
            socks5_port=socks_port,
            socks5=socks5
        )
        return self.api
    
    def test_set_cookie(self, setup_api):
        api_obj = setup_api
        
        params = ('GET /json/tables', None, None)
        api_obj.api_call(*params)
        
        logger.info(f'Cookie: {api_obj.RUNTIME_COOKIE}')
        assert api_obj.RUNTIME_COOKIE != 'test_cookie'
    
    def test_get_cookie(self):
        assert False
    
    def test_make_request(self):
        assert False
    
    def test_api_call(self):
        assert False
