
import os

# default config
class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = 'ZN\x86\xb9\xa5\x8c\x83\t *\x8eD\x89\xc1\x8a\t\x90\xd4\r\xb2\xb3\xe6\x8bU'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False

API_TOKEN="a4a380cb766a10362b072fc3b973ca2fc714725a"