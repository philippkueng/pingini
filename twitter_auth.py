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

class Authenticate_for_Twitter(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if user:
      #self.response.out.write(user.nickname())
      
      consumer_token = config.twitter_consumer_token()
      
      consumer_secret = config.twitter_consumer_secret()
      
      callback_url = helper.get_application_base_url(self.request.uri) + '/twitter/callback'
      auth = tweepy.OAuthHandler(consumer_token, consumer_secret, str(callback_url))
      try:
        redirect_url = auth.get_authorization_url()
        
        # REMOVE COOKIES FOR TWITTER
        expires = datetime.now() + timedelta(weeks=2)
        expires_rfc822 = expires.strftime('%a, %d %b %Y %H:%M:%S GMT')
        cookie = "pingini_twitter_token_key=" + str(auth.request_token.key.encode()) + ";expires=" + str(expires_rfc822) + ";path=/"
        self.response.headers.add_header('Set-Cookie',cookie)
        
        expires = datetime.now() + timedelta(weeks=2)
        expires_rfc822 = expires.strftime('%a, %d %b %Y %H:%M:%S GMT')
        cookie = 'pingini_twitter_token_secret='+str(auth.request_token.secret.encode())+';expires=' + str(expires_rfc822) + ';path=/'
        self.response.headers.add_header('Set-Cookie',cookie)
        
        self.redirect(redirect_url)
        
      except tweepy.TweepError, e:
        self.response.out.write('Error! Failed to get request token.')
        self.response.out.write(e)
      
    else:
      self.redirect(users.create_login_url(self.request.uri))
      
class Authenticate_for_Twitter_Callback(webapp.RequestHandler):
  def get(self):
    consumer_token = config.twitter_consumer_token()
    consumer_secret = config.twitter_consumer_secret()
    verifier = self.request.GET.get('oauth_verifier')
    
    auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
    token = (self.request.cookies.get('pingini_twitter_token_key'), self.request.cookies.get('pingini_twitter_token_secret'))
    auth.set_request_token(token[0], token[1])
    
    try:
      auth.get_access_token(verifier)
      auth.set_access_token(auth.access_token.key, auth.access_token.secret)
      
      api = tweepy.API(auth)
      
      api.update_status("Yay, I just signed up for pinginiapp")
      
      user_fullname = api.me().name
      user_username = api.me().screen_name
      
      user = USER(google_username = users.get_current_user().nickname(), twitter_oauth_key = auth.access_token.key, twitter_oauth_secret = auth.access_token.secret)
      user.put()
      
      self.response.out.write('Your twitter account was successfully connected to pingini. Head over to http://localhost:8085/show to send out another tweet with the credentials just saved.')
      
    except tweepy.TweepError, e:
      self.response.out.write('Sorry, there occurred an error during the authorization process with twitter. Please clear your browser cache and try again.<br/>')
      self.response.out.write(e)
    
    # REMOVE COOKIES FOR TWITTER
    expires = datetime.now() - timedelta(weeks=2)
    expires_rfc822 = expires.strftime('%a, %d %b %Y %H:%M:%S GMT')
    cookie = "pingini_twitter_token_key=" + str(auth.request_token.key.encode()) + ";expires=" + str(expires_rfc822) + ";path=/"
    self.response.headers.add_header('Set-Cookie',cookie)
  
    expires = datetime.now() - timedelta(weeks=2)
    expires_rfc822 = expires.strftime('%a, %d %b %Y %H:%M:%S GMT')
    cookie = 'pingini_twitter_token_secret='+str(auth.request_token.secret.encode())+';expires=' + str(expires_rfc822) + ';path=/'
    self.response.headers.add_header('Set-Cookie',cookie)