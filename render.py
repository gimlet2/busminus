__author__ = 'gimlet'

import jinja2
import os

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Render:
    @staticmethod
    def render(template, params):
        template = jinja_environment.get_template('templates/' + template)
        return template.render(params)
