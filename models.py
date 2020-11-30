import datetime

from peewee import *

DATABASE = SqliteDatabase('journal.db')

class Entry(Model):
  id = IntegerField(primary_key=True, unique=True)
  title = CharField()
  date = DateTimeField(default=datetime.datetime.now())
  time_spent = IntegerField()
  what_you_learned = TextField()
  resources_to_remember = TextField()

  class Meta:
    database = DATABASE
    order_by=('-date',)
    

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Entry], safe=True)
    DATABASE.close()
    
