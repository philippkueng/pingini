import pickle
from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp import RequestHandler, template
from google.appengine.ext import db
import tweepy

from datetime import datetime
from datetime import timedelta

import config
import helper
from storage import USER

class Tweet(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if user:
      # get token and secret from db      
      p_users = db.GqlQuery("SELECT * FROM USER WHERE google_username = :gu LIMIT 1", gu = user.nickname())
      
      if p_users.count() >= 1:
        for p_user in p_users:
          if p_user:
            self.response.out.write(p_user.google_username)
            
            auth = tweepy.OAuthHandler(config.twitter_consumer_token(), config.twitter_consumer_secret())
            #auth.set_request_token(dbauth.token_key, dbauth.token_secret)
            auth.set_access_token(p_user.twitter_oauth_key, p_user.twitter_oauth_secret)

            auth_api = tweepy.API(auth)
            
            auth_api.update_status("Hello World from the GTUG Zurich Hackathon.")
            
            self.response.out.write('tweet send successfully')
            
          else:
            self.response.out.write("user empty")
      else:
          self.response.out.write("no users found")
    else:
      self.response.out.write("Error while sending tweet")