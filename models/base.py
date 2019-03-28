from os.path import abspath

from peewee import Model
from peewee import SqliteDatabase

db_path = abspath('../bot.db')
db = SqliteDatabase(db_path)

class BaseModel(Model):
    class Meta:
        database = db