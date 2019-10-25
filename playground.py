from db.db import get_db
from time import sleep
get_db()

from models.User import Users
import bcrypt

# try:
#   mike_user = Users(mail="mongo44_testing@gmail.com", password="newThing23d", name="PHN_myname")
#   mike_user.save()
#   # mike_user = Users.find_user_by_credentials("mongo4_testing@gmail.com", "newThing23d")
#   print(mike_user.to_json())
# except Exception as e: 
#   print("Should work 2", e)

try:
  Users.objects(mail="mongoengine@gmail.com").delete()
  mike_user = Users(mail="mongoengine@gmail.com", password="newThing23d", name="PHN_mongonengine")
  print(mike_user.to_json())
  # import pdb; pdb.set_trace()
  # print(Users.objects(id=mike_user.id))
  mike_user.save(signal_kwargs={"changed_fields":["password"]})
  print("user Created")
except Exception as e:
  print("Should have Created user", str(e))

try:
  mike_user = Users.find_user_by_credentials("mongoengine@gmail.com", "newThing23d")
  mike_user.remove_all_auth_token()
  print(mike_user.to_json())
  mike_user.generate_auth_token()
  sleep(1)
  mike_user.generate_auth_token()
  # sleep(1)
  # mike_user.generate_auth_token()
  # sleep(1)
  # mike_user.generate_auth_token()
  print(mike_user.to_json())
  token = mike_user.tokens[0]
  mike_user.remove_auth_token(token)
  print(mike_user.to_json())
except Exception as e: 
  print("Should workd", e)

# try:
#   mike_user = Users.find_user_by_credentials("mongotesting@gmail.com", "newThing2333dd")
#   print(mike_user)
# except Exception as e: 
#   print("Should not work 1", e)

# try:
#   mike_user = Users.find_user_by_credentials("mongo4_testing@gmail.com", "newThing23d")
#   print(mike_user)
# except Exception as e: 
#   print("Should work 2", e)
# mike_user = Users.objects(name="Mongo5").as_pymongo().first()
# print(mike_user["password"])
# print(bcrypt.checkpw("123".encode('utf-8'), mike_user['password'].encode('utf-8')))
# print(bcrypt.checkpw("somestuff123".encode('utf-8'), mike_user['password'].encode('utf-8')))


# modify_data = {"password": "newThing2333dd", "name": "Mongo5"}
# mike_user = Users.objects(name="Mongo5").first()
# print(mike_user["password"])
# changed_fields = [i for i in modify_data if modify_data[i] != mike_user[i]]
# mike_user.modify(**modify_data)
# mike_user.save(signal_kwargs={"changed_fields":changed_fields})
# print(mike_user.to_json())

# mike_user = Users.objects(name="Mongo4 ").as_pymongo().first()
# print(mike_user["password"])