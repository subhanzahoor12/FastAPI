from environs import env

env.read_env()

EVENTBRITE_TOKEN = env("EVENTBRITE_TOKEN")
EVENTBRITE_URL = env("EVENTBRITE_URL")
DB_URL = env("DB_URL")
SECRET_KEY = env("SECRET_KEY")
