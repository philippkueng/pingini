from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp import RequestHandler, template
from google.appengine.ext import db

class Show(webapp.RequestHandler):
  def get(self):
    self.response.out.write('hi there from show')