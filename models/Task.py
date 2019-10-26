from mongoengine import Document, StringField, BooleanField, ReferenceField
from models.User import Users
import json

class Tasks(Document):
  completed = BooleanField(required=True, default=False)
  description = StringField(min_length=7, required=True)
  owner = ReferenceField(Users, reverse_delete_rule=2, required=True)
