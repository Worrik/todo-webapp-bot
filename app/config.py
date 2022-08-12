from environs import Env

env = Env()
env.read_env()

TOKEN = env.str("TOKEN")
DATABASE_URL = env.str("DATABASE_URL")
WEB_APP_URL = env.str("WEB_APP_URL")
ADMIN_ID = env.str("ADMIN_ID")
