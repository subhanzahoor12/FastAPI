from environs import env

env.read_env()

EVENTBRITE_TOKEN = env("EVENTBRITE_TOKEN")
EVENTBRITE_URL = env("EVENTBRITE_URL")
db_url = env("db_url")