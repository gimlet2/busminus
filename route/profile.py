__author__ = 'gimlet'

import webapp2

from google.appengine.api import users
from dao.user_dao import User
from render import Render


class ProfileHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        params = {
            'title': 'Main Page',
            }
        self.response.out.write(Render.render('profile.html', params))

