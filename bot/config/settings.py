from decouple import config, Csv


class Settings:
    BOT_TOKEN = config("BOT_TOKEN", cast=str)
    ADMIN_IDS = config("ADMIN_IDS", cast=Csv())


settings = Settings()
