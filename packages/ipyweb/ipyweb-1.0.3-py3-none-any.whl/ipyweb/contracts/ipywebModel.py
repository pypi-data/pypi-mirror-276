from peewee import Model
from ipyweb.db import db as db


class ipywebModel(Model):
    class Meta:
        database = db('sqlite.default').open()
