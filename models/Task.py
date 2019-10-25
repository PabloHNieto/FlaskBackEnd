from mongoengine import Document, StringField, BooleanField

class Tasks(Document):
  completed = BooleanField(required=True, default=False)
  description = StringField(min_length=7, required=True)
    