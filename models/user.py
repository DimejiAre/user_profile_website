import pyrebase
import uuid
from werkzeug.security import generate_password_hash

config = {
    "apiKey": "AIzaSyD1yZZjaVLM249P1VPO3qmmIzGXQJJ5iLo",
    "authDomain": "flask-firebase-d4384.firebaseapp.com",
    "databaseURL": "https://flask-firebase-d4384.firebaseio.com",
    "projectId": "flask-firebase-d4384",
    "storageBucket": "flask-firebase-d4384.appspot.com",
    "messagingSenderId": "138802909035"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()


class User(object):
    def __init__(self, name, password, description, address, email, phone, skills, interests, id=None):
        self.name = name
        self.password = generate_password_hash(password, method="sha1")
        self.description = description
        self.address = address
        self.email = email
        self.phone = phone
        self.skills = skills
        self.interests = interests
        if id is None:
            self.id = uuid.uuid4().hex
        else:
            self.id = id

    def get_json(self):
        return {
            "name": self.name,
            "password": self.password,
            "description": self.description,
            "address": self.address,
            "email": self.email,
            "phone": self.phone,
            "skills": self.skills,
            "interests": self.interests
        }

    def create_user(self):
        db.child("users").child(self.id).set(self.get_json())

    @staticmethod
    def get_user():
        user = db.child("users").get()
        user_dict = user.val()
        return user_dict
