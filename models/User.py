import bcrypt
import jwt
import json
from mongoengine import Document, ListField, EmbeddedDocument, EmbeddedDocumentField, DateTimeField, ObjectIdField, UUIDField, StringField, EmailField, IntField, signals
from datetime import datetime as dt
from bson.objectid import ObjectId

class Token(EmbeddedDocument):
  oid = ObjectIdField(required=True, default=ObjectId)
  token = StringField(required=True)

class Users(Document):
  oid = ObjectIdField(required=True, default=ObjectId, primary_key=True, unique=True)
  name = StringField(required=True)
  mail = EmailField(required=True, unique=True)
  age = IntField(required=True, default=0)
  password = StringField(min_length=7, required=True)
  tokens = ListField(EmbeddedDocumentField(Token))
  createdAt = DateTimeField(default=dt.now())
  updatedAt = DateTimeField(default=dt.now())

  def clean(self):
    self.name = self.name.strip()

  @staticmethod
  def find_user_by_credentials(mail, password):
    user = Users.objects(mail= mail).first()
    
    if not user: raise Exception("User not found")

    if not bcrypt.checkpw(password.encode("utf8"), user.password.encode("utf8")):
      raise Exception("Invalid Password")
    return user
  
  def generate_auth_token(self):
    encoded = jwt.encode({"_id": str(self.id), 
      "timestamp": int(dt.timestamp(dt.now()))}, 'secret', algorithm='HS256').decode("utf8")
    new_token = Token(token=encoded)
    self.tokens.append(new_token)
    self.save()
    return encoded

  def remove_auth_token(self, token):
    self.tokens = list(filter(lambda x: x.token != token, self.tokens))
    self.save()

  def remove_all_auth_token(self):
    self.tokens = []
    self.save()

  def to_json(self):
    from models.Task import Tasks
    tasks = Tasks.objects(owner=self.pk)
    user_dict = json.loads(super(Users, self).to_json())
    user_dict["tasks"] = json.loads(tasks.to_json())
    return json.dumps(user_dict)

  @classmethod
  def pre_save(cls, sender, document, changed_fields=[]):
    document.updatedAt = dt.now()
    if "password" in changed_fields:
      document.password = bcrypt.hashpw(document.password.encode('utf8'), bcrypt.gensalt()).decode('utf-8')


signals.pre_save.connect(Users.pre_save, sender=Users)