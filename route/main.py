__author__ = 'gimlet'

import webapp2

from google.appengine.api import users
from dao.user_dao import User
from render import Render

class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        username = None
        if not user:
            login = users.create_login_url(self.request.uri)
        else:
            if User.find(user) is None:
                User.create(user)
                self.redirect('/profile')
            username = user.nickname()
            login = users.create_logout_url(self.request.uri)
        params = {
            'title': 'Main Page',
            'login': login,
            'username': username
        }
        self.response.out.write(Render.render('index.html', params))

