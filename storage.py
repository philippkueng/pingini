from google.appengine.ext import db

class USER(db.Model):
  google_username = db.StringProperty()
  twitter_oauth_key = db.StringProperty()
  twitter_oauth_secret = db.StringProperty()