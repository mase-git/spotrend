
from dotenv import load_dotenv
import logging
from spotrend.exceptions import SpotrendsInputException

# load dotenv
load_dotenv()

# setup logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s: %(message)s')


class Spotrend():
    pass
