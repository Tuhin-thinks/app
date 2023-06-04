from datetime import datetime
import logging

LOGGER = None
logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - [%(levelname)s #L%(lineno)d] - %(message)s')
today_date_str = datetime.today().strftime('%Y%m%d')


def get_logger(logger_name: str):
    
    fh = logging.FileHandler(f'log_{today_date_str}.log')
    fh.setLevel(logging.DEBUG)
    
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    return logger
