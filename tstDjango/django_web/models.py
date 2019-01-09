from django.db import models

# Create your models here.
from mongoengine import Document
from django.db import models
from mongoengine import *
from mongoengine import connect

connect('weather', host='127.0.0.1', port=27017)

# Create your models here.

class ItemInfo(Document):
    city = StringField()
    aqi = IntField()
    pm25 = IntField()
    no2 = IntField()
    meta = {'collection': 'data_mainCity'}


