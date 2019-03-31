import os
from os.path import abspath

from peewee import Model
from peewee import PostgresqlDatabase
from peewee import SqliteDatabase

db =  None

if os.getenv('ENV_MODE') == 'PROD':
    db = PostgresqlDatabase('botdb', host=os.getenv('DATABASE_URL'))
else:
    db_path = abspath('../bot.db')
    db = SqliteDatabase(db_path)


class BaseModel(Model):
    class Meta:
        database = db