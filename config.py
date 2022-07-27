from environs import Env

env = Env()
env.read_env()

TOKEN = env.str("TOKEN")
DATABASE_URL = env.str("DATABASE_URL")
