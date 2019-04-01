import os
from os.path import abspath
from urllib.parse import urlparse

from peewee import Model
from peewee import PostgresqlDatabase
from peewee import SqliteDatabase

db =  None

if os.getenv('ENV_MODE') == 'PROD':
    url = urlparse(os.getenv('DATABASE_URL'))
    db = PostgresqlDatabase(url.path[1:], user=url.username, host=url.hostname, password=url.password, port=url.port)
else:
    db_path = abspath('../bot.db')
    db = SqliteDatabase(db_path)


class BaseModel(Model):
    class Meta:
        database = db