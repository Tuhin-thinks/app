from datetime import datetime
from typing import Dict

from m_logging import get_logger

TEST_DATA_DIR = "test_data"
TEST_RUN = False
shared_instance = None
logger = get_logger(__name__)


class GlobalConfig:
    @classmethod
    def set_test_run(cls, test_run: bool):
        global TEST_RUN
        TEST_RUN = test_run
    
    @classmethod
    def get_test_run(cls):
        return TEST_RUN
    
    @classmethod
    def get_data_sharing_instance_obj(cls) -> 'SharedInstance':
        global shared_instance
        if shared_instance is None:
            shared_instance = SharedInstance()
        return shared_instance
        

class SharedInstance:
    """
    Class to handle data between multiple files in the application.
    Mainly to communicate between windows, for notification purpose.
    """
    
    def __init__(self):
        self.time_book: Dict[str, datetime] = {}
        logger.info("Data sharing instance created...")
    
    def add_to_wait_queue(self, job_name: str):
        """
        Function takes in an information about some job records the time.
        When the job is popped from the queue, the time is compared to the current time and time taken is printed.
        """
        self.time_book[job_name] = datetime.now()
        logger.debug(f"Added {job_name} to wait queue.")
    
    def pop_from_wait_queue(self, job_name: str):
        """
        Function takes in an information about some job and prints the time taken to complete the job.
        """
        if job_name in self.time_book:
            time_taken = datetime.now() - self.time_book[job_name]
            logger.info(f"Time taken for \"{job_name}\": {time_taken}")
            del self.time_book[job_name]
            logger.debug(f"Removed \"{job_name}\" from wait queue.")
        else:
            logger.warning(f"Job \"{job_name}\" not found in queue.")
