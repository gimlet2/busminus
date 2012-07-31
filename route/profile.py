import urllib

__author__ = 'gimlet'

import webapp2
import logging

from google.appengine.api import users
from dao.user_dao import User
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from render import Render


class ProfileHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            user_db = User.find(user)
            blob_key = user_db.car_photo_blob_id
            if blob_key is not None:
                car_url = '/serve/%s' % blob_key.key()
            else:
                car_url = '/img/car.jpg'
            params = {
                'title': 'Main Page',
                'upload_url': blobstore.create_upload_url('/upload'),
                'nick': user_db.nick,
                'car_number': user_db.car_number,
                'car_url': car_url,
                'login': users.create_logout_url(self.request.uri),
                'username': user.nickname()
            }
            self.response.out.write(Render.render('profile.html', params))
        else:
            self.redirect('/')

    def post(self):
        user = users.get_current_user()
        user_db = User.find(user)
        logging.info(self.request.get('display_name'))
        user_db.nick = self.request.get('display_name')
        user_db.car_number = self.request.get('car_number')
        user_db.put()
        self.redirect('/profile')


class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        upload_files = self.get_uploads('car_photo')
        logging.info(upload_files.__len__())
        blob_info = upload_files[0]
        user = users.get_current_user()
        user_db = User.find(user)
        user_db.car_photo_blob_id = blob_info.key()
        user_db.put()
        self.redirect('/profile')


class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, resource):
        resource = str(urllib.unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        self.send_blob(blob_info)
