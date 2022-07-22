import logging
from environs import Env

env = Env()
env.read_env()

TOKEN = env.str("TOKEN")
DATABASE_URL = env.str("DATABASE_URL")

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)
