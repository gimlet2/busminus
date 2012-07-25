#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
import os

import dao.user_dao

from google.appengine.api import users
from dao.user_dao import User

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        username = None
        if not user:
            login = users.create_login_url(self.request.uri)
        else:
            if User.find(user) is None:
                User.create(user)

            username = user.nickname()
            login = users.create_logout_url(self.request.uri)
        params = {
            'title': 'Main Page',
            'text': 'BusMinus',
            'login': login,
            'username': username
        }
        template = jinja_environment.get_template('templates/index.html')
        self.response.out.write(template.render(params))

app = webapp2.WSGIApplication([('/', MainHandler)],
    debug=True)
