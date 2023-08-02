from datetime import datetime
import logging


def get_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""
    logging.basicConfig(level=level)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler = logging.FileHandler(log_file, mode='w')
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger


# create a singleton logger class
class Logger:
    instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super(Logger, cls).__new__(cls)
            cls.initialized = False
        return cls.instance

    def __init__(self, **kwargs):
        if self.initialized:
            return
        self.def_logger_file_path = None
        self.init_logger_config(**kwargs)
        self.initialized = True

    def init_logger_config(self, **kwargs):
        start_time_str = datetime.now().strftime("%H_%M_%S__%d_%b_%Y")
        self.def_logger_file_path = kwargs.get('log_file_path',
                                               f'test_logs/{start_time_str}.log')

    def get_logger(self, name: str) -> logging.Logger:
        logger = get_logger(name, self.def_logger_file_path)
        return logger
