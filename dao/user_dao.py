from google.appengine.api import users
from google.appengine.ext.blobstore import blobstore

__author__ = 'gimlet'

from google.appengine.ext import db

class User(db.Model):
    name = db.StringProperty()
    user = users.User()
    nick = db.StringProperty()
    car_number = db.StringProperty()
    car_photo_blob_id = blobstore.BlobReferenceProperty()

    @staticmethod
    def find(username):
        return db.get(db.Key.from_path('User', username.email()))

    @staticmethod
    def create(a_user):
        user = User(key_name=a_user.email())
        user.name = a_user.email()
        user.user = a_user
        user.put()
