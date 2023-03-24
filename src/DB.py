from peewee import *
import datetime

db = MySQLDatabase('myapp', user='ibrahim', password='!brahim',
                   host='localhost', port=3306)


class Persons(Model):
    #id = IntegerField PrimaryKeyField(null=False)
    id_person = IntegerField(null = False)
    name = CharField()
    lName = CharField()
    birthdate = DateTimeField(null=True)
    phone = IntegerField(null=True)
    mail = CharField(null=True, unique=True)
    image = CharField(null=True)
    finger = CharField(null=True)
    
    class Meta:
        database = db

db.connect()
db.create_tables([Persons])

